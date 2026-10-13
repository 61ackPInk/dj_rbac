## `products` App 目录职责

```
apps/products/
├── adapters/                # 对接不同 ERP
│   ├── yuancang/            # 元仓具体实现
│   │   ├── config.py        # 读取元仓配置
│   │   ├── client.py        # 鉴权和 HTTP 请求
│   │   ├── mappers.py       # 元仓字段转统一字段
│   │   ├── products.py      # 元仓商品接口
│   │   └── stocks.py        # 元仓库存接口
│   ├── base.py              # 所有 ERP 必须遵守的协议
│   ├── exceptions.py        # ERP 相关异常
│   └── factory.py           # 选择当前 ERP
│
├── serializers/
│   └── products.py          # 请求参数和响应结构校验
│
├── services/
│   ├── products.py          # 商品与库存业务编排
│   └── bundles.py           # 组合商品业务编排
│
├── views/
│   └── products.py          # 接收商品 HTTP 请求
│
├── tests/                   # 商品系统测试
├── urls.py                  # 商品 App 内部路由
├── apps.py                  # Django App 配置
├── models.py                # 当前暂不使用
├── admin.py                 # 当前暂不使用
└── .env                     # 商品 App 的本地 ERP 配置
```

## 商品列表在 App 内部的工作流程

```
urls.py
  ↓
views/products.py
  ↓
serializers/products.py
  ↓
services/products.py
  ↓
adapters/factory.py
  ├─→ adapters/yuancang/products.py
  └─→ adapters/yuancang/stocks.py
             ↓
       adapters/yuancang/client.py
             ↓
       adapters/yuancang/mappers.py
  ↓
services/products.py 合并商品和库存
  ↓
serializers/products.py 校验响应
  ↓
views/products.py 返回 Response
```

### 1. `urls.py`：找到对应 View

商品 App 收到列表请求后，由：

```
apps/products/urls.py
```

匹配到：

```
ProductListAPIView
```

`urls.py` 只负责“这个地址交给哪个 View”，不处理任何业务。

### 2. `views/products.py`：接收并编排请求

`ProductListAPIView` 负责：

1. 检查 `PRODUCT_LIST` 权限；
2. 获取 URL 查询参数；
3. 调用查询序列化器；
4. 创建 `ProductService`；
5. 调用商品服务；
6. 校验最终响应；
7. 返回 `Response`。

View 不负责调用元仓，也不负责合并库存。

### 3. `serializers/products.py`：校验输入

查询序列化器接收：

```
page
page_size
customer_sku
category_id
created_at_from
created_at_to
```

例如传入：

```
page_size=500
```

序列化器会直接拒绝，因为元仓每页最多100条。

验证成功后产生干净的服务层参数：

```
{
    "page": 1,
    "page_size": 20,
    "customer_sku": "SET-001",
}
```

### 4. `services/products.py`：商品业务总调度

这是商品列表流程的核心。

`ProductService` 将负责：

```
调用商品 Provider
  ↓
获得当前页商品
  ↓
按 main_warehouse.code 分组
  ↓
调用库存 Provider
  ↓
按 customer_sku 合并库存
  ↓
返回统一结果
```

服务层不知道元仓接口地址，也不处理 Token。

它只认识两个协议：

```
BaseProductProvider
BaseStockProvider
```

### 5. `adapters/factory.py`：决定使用哪个 ERP

工厂读取：

```
PRODUCT_ERP_PROVIDER=yuancang
```

然后返回：

```
YuanCangProductProvider
YuanCangStockProvider
```

以后换 ERP 时，Service 仍然调用相同方法，只是工厂返回其他实现。

### 6. `adapters/yuancang/products.py`：读取元仓商品

负责调用元仓：

```
/api/openPlatform/product/list
/api/openPlatform/product/detail
```

它把内部统一查询参数转换成元仓参数：

```
page_size → prePage
customer_sku → customerSku
```

再将元仓响应交给 Mapper。

### 7. `adapters/yuancang/stocks.py`：读取元仓库存

负责调用：

```
/api/openPlatform/stock/list
```

它接收：

```
warehouse_code = "001"

customer_skus = [
    "SET-001",
    "ARO-001",
]
```

然后返回：

```
{
    "SET-001": {
        "found": True,
        "available": 75,
    },
    "ARO-001": {
        "found": True,
        "available": 80,
    },
}
```

库存结果以 SKU 为键，方便 Service 直接匹配。

### 8. `adapters/yuancang/client.py`：处理元仓通信

商品 Provider 和库存 Provider 都通过同一个 Client 请求元仓。

Client 负责：

```
读取配置
获取Token
缓存Token
添加Authorization
发送POST请求
处理超时
处理元仓state
Token失效后重新授权
```

Provider 不重复实现这些逻辑。

### 9. `adapters/yuancang/config.py`：读取元仓配置

负责读取：

```
apps/products/.env
```

生成：

```
YuanCangConfig(
    base_url=...,
    app_key=...,
    app_secret=...,
    token_cache_seconds=43200,
    timeout_seconds=15,
)
```

只有 Client 使用这些连接配置。

### 10. `adapters/yuancang/mappers.py`：转换字段

Mapper 将元仓字段：

```
customerSku
productCnName
mainWarehouseCode
waitShelf
inventory
available
```

转换为 App 内部统一字段：

```
customer_sku
name
main_warehouse
waiting_for_shelf
total
available
```

Service 和 View 不再看到元仓原始字段。

### 11. `services/products.py`：合并最终结果

Service 根据商品的：

```
product["customer_sku"]
```

寻找库存映射：

```
stock_map[customer_sku]
```

找到时：

```
{
  "inventory": {
    "found": true,
    "available": 75
  }
}
```

没有找到时：

```
{
  "inventory": {
    "found": false,
    "available": null
  }
}
```

不会把“没有库存记录”错误地表示成库存为零。

### 12. 响应序列化器再次校验

Service 完成合并后，结果回到：

```
serializers/products.py
```

响应序列化器确认：

- `items` 是数组；
- 分页字段存在；
- 商品字段类型正确；
- 库存结构正确。

确认后才由 View 返回。

## 组合商品流程

以后组合商品走一条平行流程：

```
views/bundles.py
  ↓
serializers/bundles.py
  ↓
services/bundles.py
  ↓
BaseBundleProvider
  ↓
adapters/yuancang/bundles.py
```

组合服务还会根据组成 SKU 和数量计算：

```
组合库存 =
min(
  floor(组成商品可用库存 ÷ 所需数量)
)
```

目前没有元仓组合 API，所以这条流程暂时只保留服务和抽象接口，不继续实现。

## 当前暂不使用的文件

```
models.py
migrations/
admin.py
```

因为当前商品和库存都实时读取元仓，不保存本地商品数据。

一句话概括 Products App：

```
View 接收请求
→ Serializer 校验
→ Service 编排业务
→ Factory 选择 ERP
→ Adapter 调用并转换元仓数据
→ Service 合并商品和库存
→ Serializer 校验结果
→ View 返回
```

17:47