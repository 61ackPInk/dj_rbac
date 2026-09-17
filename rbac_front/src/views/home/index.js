import { defineComponent } from 'vue'
import { ElMessage } from 'element-plus'

export default defineComponent({
  name: 'HomeView',

  setup() {
    const handleTest = () => {
      ElMessage.success('前端基础配置成功')
    }

    // 返回模板中调用的方法
    return {
      handleTest,
    }
  },
})