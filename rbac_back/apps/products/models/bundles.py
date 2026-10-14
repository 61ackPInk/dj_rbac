"""
-*- coding: utf-8 -*-
@File  : bundles.py
@Author: 61ackPink
@Time : 2026/10/14 17:50
@Desc : 组合商品及组成明细模型
"""

from django.db import models


# ==================== 组合商品 ====================


class ProductBundle(models.Model):
    """
    组合商品。

    保存从外部数据源采集并标准化后的组合商品资料。

    组合映射由所有仓库共用，因此模型不保存仓库编码。
    不保存组合实时库存，实时库存由 BundleService
    根据子 SKU 库存动态计算。
    """

    provider_code = models.CharField(
        max_length=50,
        verbose_name="数据来源编码",
        help_text=(
            "组合映射的数据来源，"
            "例如 yuancang"
        ),
    )

    external_id = models.CharField(
        max_length=100,
        verbose_name="外部记录ID",
        help_text=(
            "第三方系统中的组合映射记录ID"
        ),
    )

    bundle_sku = models.CharField(
        max_length=100,
        verbose_name="组合SKU",
    )

    name = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="组合商品名称",
    )

    image_url = models.URLField(
        max_length=1000,
        blank=True,
        default="",
        verbose_name="组合商品图片",
    )

    source_status = models.CharField(
        max_length=50,
        blank=True,
        default="",
        verbose_name="来源状态编码",
        help_text=(
            "第三方系统返回的原始状态编码"
        ),
    )

    source_status_name = models.CharField(
        max_length=100,
        blank=True,
        default="",
        verbose_name="来源状态名称",
    )

    source_created_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="来源创建时间",
    )

    source_updated_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="来源更新时间",
    )

    collected_at = models.DateTimeField(
        verbose_name="最后采集时间",
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name="是否有效",
        help_text=(
            "完整采集后来源中不再存在的组合"
            "会被标记为无效"
        ),
    )

    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name="创建时间",
    )

    update_time = models.DateTimeField(
        auto_now=True,
        verbose_name="更新时间",
    )

    class Meta:
        db_table = "product_bundles"
        verbose_name = "组合商品"
        verbose_name_plural = "组合商品"

        ordering = [
            "bundle_sku",
            "id",
        ]

        constraints = [
            # 同一个数据来源中的外部记录 ID 唯一
            models.UniqueConstraint(
                fields=[
                    "provider_code",
                    "external_id",
                ],
                name=(
                    "unique_bundle_provider_external"
                ),
            ),

            # 同一个数据来源中的组合 SKU 唯一
            models.UniqueConstraint(
                fields=[
                    "provider_code",
                    "bundle_sku",
                ],
                name=(
                    "unique_bundle_provider_sku"
                ),
            ),
        ]

        indexes = [
            # 组合列表通常按来源和有效状态查询
            models.Index(
                fields=[
                    "provider_code",
                    "is_active",
                ],
                name="idx_bundle_provider_active",
            ),

            # 组合详情需要根据组合 SKU 查询
            models.Index(
                fields=[
                    "bundle_sku",
                ],
                name="idx_bundle_sku",
            ),
        ]

    def __str__(self):
        """返回组合商品的可读名称。"""

        return (
            f"{self.bundle_sku}"
            f"（{self.name or '未命名'}）"
        )


# ==================== 组合商品明细 ====================


class ProductBundleItem(models.Model):
    """
    组合商品中的子 SKU。

    同一个组合下，相同 customer_sku 的元仓明细
    会在采集转换时合并，并把 quantity 累加到
    required_quantity。
    """

    bundle = models.ForeignKey(
        ProductBundle,

        # 删除组合商品时同时删除组成明细
        on_delete=models.CASCADE,

        # 可以通过 bundle.items.all()
        # 查询组合中的全部子 SKU
        related_name="items",

        verbose_name="所属组合商品",
    )

    provider_sku = models.CharField(
        max_length=100,
        blank=True,
        default="",
        verbose_name="来源商品SKU",
        help_text=(
            "第三方系统内部使用的商品SKU"
        ),
    )

    customer_sku = models.CharField(
        max_length=100,
        verbose_name="客户SKU",
        help_text=(
            "用于调用库存接口查询实时库存"
        ),
    )

    name = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="子商品名称",
    )

    image_url = models.URLField(
        max_length=1000,
        blank=True,
        default="",
        verbose_name="子商品图片",
    )

    required_quantity = models.PositiveIntegerField(
        verbose_name="所需数量",
        help_text=(
            "组成一个组合商品所需的子商品数量"
        ),
    )

    source_status = models.CharField(
        max_length=50,
        blank=True,
        default="",
        verbose_name="来源商品状态编码",
    )

    source_status_name = models.CharField(
        max_length=100,
        blank=True,
        default="",
        verbose_name="来源商品状态名称",
    )

    sort_order = models.PositiveIntegerField(
        default=0,
        db_index=True,
        verbose_name="排序",
    )

    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name="创建时间",
    )

    update_time = models.DateTimeField(
        auto_now=True,
        verbose_name="更新时间",
    )

    class Meta:
        db_table = "product_bundle_items"
        verbose_name = "组合商品明细"
        verbose_name_plural = "组合商品明细"

        ordering = [
            "sort_order",
            "id",
        ]

        constraints = [
            # Mapper 已经合并重复 SKU，
            # 同一个组合中只能保留一条相同子 SKU
            models.UniqueConstraint(
                fields=[
                    "bundle",
                    "customer_sku",
                ],
                name=(
                    "unique_bundle_customer_sku"
                ),
            ),

            # 组成数量必须大于或等于 1
            models.CheckConstraint(
                condition=models.Q(
                    required_quantity__gte=1,
                ),
                name=(
                    "bundle_item_quantity_gte_1"
                ),
            ),
        ]

        indexes = [
            # 组合库存计算时需要按客户 SKU
            # 汇总并批量查询实时库存
            models.Index(
                fields=[
                    "customer_sku",
                ],
                name="idx_bundle_item_customer_sku",
            ),
        ]

    def __str__(self):
        """返回组合明细的可读名称。"""

        return (
            f"{self.bundle.bundle_sku}"
            f" → {self.customer_sku}"
            f" × {self.required_quantity}"
        )