# List Page Structure

## 职责边界

列表页默认负责：

- 查询条件
- 列表数据
- 分页数据
- 主操作入口
- 删除操作
- 打开弹窗的入口

列表数据属于主页面，不属于弹窗页。

## 推荐组织

- 查询参数集中放在一个对象里
- 分页参数集中放在一个对象里
- 列表查询单独成一个异步函数
- 查询与重置行为显式区分
- 如果页面仍属于当前仓库的 CRUD 家族，列表区默认优先沿用 `DynamicTable + tableConfig`

参考片段：

```js
const loading = ref(false)
const list = ref([])
const pagination = ref({
  current: 1,
  pageSize: 10,
  total: 0,
})
const selectParams = ref({
  keyword: '',
  status: '',
})

const selectList = async () => {
  loading.value = true
  try {
    const res = await List(selectParams.value, pagination.value)
    list.value = res.result.list
    pagination.value = res.result.pagination
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}
```

当前仓库内更推荐的列表承载方式类似这样：

```vue
<script setup>
import { ref } from 'vue'

const loading = ref(false)
const list = ref([])
const tableConfig = ref({
  table: { border: true, stripe: true },
  column: [
    { prop: 'index', type: 'index', label: '序号', align: 'center', width: 60 },
    { prop: 'name', label: '名称', align: 'center', minWidth: 180 },
    { prop: 'operation', label: '操作', align: 'center', width: 220, hasSlot: true },
  ],
})
</script>

<template>
  <DynamicTable v-loading="loading" :list="list" :config="tableConfig">
    <template #operation="{ row }">
      <el-button size="small" type="warning">修改</el-button>
      <el-button size="small" type="danger">删除</el-button>
    </template>
  </DynamicTable>
</template>
```

这里强调的是“当前家族的推荐基线”，不是说原生 `el-table` 技术上不能用。只有当 `DynamicTable` 明显不适配当前需求时，才考虑退回原生表格。

## 查询与重置

查询和重置都是列表页职责。重置时默认回到第一页。

```js
const handleSelect = () => {
  pagination.value.current = 1
  selectList()
}

const handleReset = () => {
  formRef.value.resetFields()
  pagination.value.current = 1
  selectList()
}
```

## 与弹窗页的边界

列表页只负责“打开哪个场景”，不负责维护弹窗内部表单状态。

```js
const dialogRef = ref(null)

const handleOpenDialog = (type, id) => {
  dialogRef.value.init({ type, id })
}
```
