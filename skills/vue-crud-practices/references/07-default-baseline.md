# Default Baseline

## 当前默认接受的实现基线

- 列表页在当前仓库里默认优先沿用 `DynamicTable + tableConfig`
- CRUD 路由页默认优先沿用 `index.vue + add-or-update.vue`
- 列表页使用 `async / await` 查询，并在 `finally` 中回收 `loading`
- 重置查询时回到第一页
- 删除操作走异步流程，不保留旧式链式写法
- 弹窗入口使用 `init({ type, id })`
- 弹窗内用 `dialogType` 表达场景，不通过标题倒推业务
- 详情与修改共用记录装载流程
- 弹窗先打开，再加载记录；加载失败则关闭
- `add-or-update.vue` 命名当前继续接受，不强行改名
- 业务子组件内部按需调用 `useDict()`、路由、store 等组合式函数，不把这些结果从父组件组装后再透传
- 单页私有的表单工厂、列表归一化、payload 拼装默认留在所属 SFC；页面过重先拆组件，复用闭包再抽 composable

## 最小页面骨架参考

```vue
<script setup>
import { onMounted, ref } from 'vue'
import FormDialog from './add-or-update.vue'

const loading = ref(false)
const list = ref([])
const dialogRef = ref(null)
const tableConfig = ref({
  table: { border: true, stripe: true },
  column: [
    { prop: 'index', type: 'index', label: '序号', align: 'center', width: 60 },
    { prop: 'name', label: '名称', align: 'center', minWidth: 180 },
    { prop: 'operation', label: '操作', align: 'center', width: 180, hasSlot: true, hasHeader: true },
  ],
})

const selectList = async () => {
  loading.value = true
  try {
    // await List(...)
  } finally {
    loading.value = false
  }
}

const handleOpenDialog = (type, id) => {
  dialogRef.value.init({ type, id })
}

onMounted(() => {
  selectList()
})
</script>

<template>
  <div class="base-container mt-20">
    <DynamicTable v-loading="loading" :list="list" :config="tableConfig">
      <template #operation_header>
        <el-button type="success" size="small" @click="handleOpenDialog('insert')">新增</el-button>
      </template>
      <template #operation="{ row }">
        <el-button size="small" type="warning" @click="handleOpenDialog('update', row.id)">修改</el-button>
        <el-button size="small" type="danger">删除</el-button>
      </template>
    </DynamicTable>
  </div>
  <FormDialog ref="dialogRef" @refresh-list="selectList" />
</template>
```

## 完整参考资产

如果任务需要直接参照一套更完整的列表页与弹窗页骨架，可继续查看：

- `assets/index.reference.vue`
- `assets/add-or-update.reference.vue`

这两份文件的作用是提供“当前 CRUD 家族常见承载方式”的纯参考成品，方便复用页面组织、状态命名、表单布局和 `DynamicTable + tableConfig` 的落点。

注意：

- 它们不是字段驱动模板
- 它们不是要求原样复制到业务代码中的固定答案

其中字段故意收敛为稳定模拟集：

- `name`
- `type`
- `status`
- `remark`
- `createTime`

使用它们时，应参考承载方式和结构边界，再按真实业务字段替换，而不是把它们当作占位替换模板继续二次模板化。

## API 组织参考

当前 CRUD API 默认保持五段式，统一走 `@/utils/request`：

```js
export const List = (params, pagination) =>
  request({
    baseURL: '/api',
    url: '/module/function/',
    method: 'GET',
    params: { ...params, ...pagination },
  })

export const Get = (id) =>
  request({
    baseURL: '/api',
    url: '/module/function/' + id,
    method: 'GET',
  })

export const Insert = (data) =>
  request({
    baseURL: '/api',
    url: '/module/function',
    method: 'POST',
    data,
  })

export const Update = (data) =>
  request({
    baseURL: '/api',
    url: '/module/function/' + data.id,
    method: 'PUT',
    data,
  })

export const Delete = (id) =>
  request({
    baseURL: '/api',
    url: '/module/function/' + id,
    method: 'DELETE',
  })
```

## 这里的作用

这个文件只回答“当前默认先贴近什么样的实现”。如果某个页面确实存在例外需求，应在对应任务里单独说明，不要把例外写回默认基线。
