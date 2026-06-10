# Review Checklist

## 新页面落地复查

- 列表页和弹窗页职责是否清晰
- 查询、列表、分页是否仍留在列表页
- 弹窗是否只负责单条记录相关操作
- 是否已经拆出 `dialogType`、`recordLoading`、`submitLoading`
- 查询、提交、记录加载是否都能稳定收口
- 如果页面仍属于当前 CRUD 家族，列表区是否优先沿用了 `DynamicTable + tableConfig`
- 业务子组件依赖的 `useDict()`、路由、store 等组合式能力是否仍然在使用处按需获取，而不是父层先组装后透传
- 单页私有逻辑是否仍然留在所属 SFC，未为了整洁感默认拆成 `helpers.js`
- 是否引入了没有明显收益的抽象
- 是否已经先判断哪些操作适用当前 CRUD 弹窗，哪些需要单独承载
- 非 CRUD 操作是否已经明确落在“直接行操作 / 同页独立弹窗 / 独立页面”之一

## 旧页面重构复查

- 原有业务行为是否保持不变
- 是否先完成了承载面分类
- 是否消除了“标题驱动业务判断”
- 是否消除了“一个 loading 覆盖全部流程”
- 是否统一了主要异步链路的写法
- 如果页面仍属于当前 CRUD 家族，是否已经回到仓库默认接受的列表和弹窗承载方式
- 是否消除了“父层聚合组合式函数结果，再通过 props 下传”的新型耦合
- 是否消除了“为了整理代码默认拆 `helpers.js`”但没有实际复用价值的外流
- 是否把明显独立的流程从当前弹窗中识别出来
- 是否已经为不适用 CRUD 弹窗的流程补上独立组件或独立页面
- 轻量状态动作是否已经回到列表页直接处理，而不是被并进 CRUD 表单

## 常见坏味道

```js
// 坏味道 1：标题驱动业务
if (dialogTitle.value === '详情') {
  return
}

// 坏味道 2：一个 loading 覆盖所有流程
const dialogLoading = ref(false)

// 坏味道 3：查询、加载、提交风格割裂
List(params).then(...)
Get(id).then(...)
await Update(data)

// 坏味道 4：把独立流程继续塞进 CRUD 弹窗
if (type === 'approve') {
  openApproveDialog(id)
}

// 坏味道 5：把组合式函数结果从父层透传
<FormDialog :dict="dict" />

// 坏味道 6：单页私有逻辑默认拆 helpers
import { createDialogForm, buildPayload } from './helpers.js'
```

## 目标状态参考

```js
const dialogType = ref('insert')
const recordLoading = ref(false)
const submitLoading = ref(false)
const readonlyMode = computed(() => dialogType.value === 'detail')

const selectList = async () => {
  loading.value = true
  try {
    ...
  } finally {
    loading.value = false
  }
}
```

```js
const handleOpenApprove = (row) => {
  approveDialogRef.value.open({ id: row.id })
}
```

```js
const handleStateChange = async (row, value) => {
  try {
    await BindAndStatus({ deviceId: row.id, regionId: row.regionId, deptId: row.deptId, state: value })
    selectList()
  } catch (error) {
    console.error(error)
  }
}
```
