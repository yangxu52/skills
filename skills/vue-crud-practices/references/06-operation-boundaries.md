# Operation Boundaries

## 可以继续留在当前页或当前弹窗的操作

- 新增
- 详情
- 修改
- 复制

这些场景本质上仍然是在查看或编辑当前单条记录本身。

参考片段：

```vue
<template #operation="{ row }">
  <el-button size="small" @click="handleOpenDialog('detail', row.id)">详情</el-button>
  <el-button type="warning" size="small" @click="handleOpenDialog('update', row.id)">修改</el-button>
</template>
```

## 更适合独立处理的操作

- 归档
- 审核
- 独立子配置维护
- 跨子域、跨流程、强状态流转的操作

这些场景通常已经不再是单条记录的轻量查看或编辑。

## 判断标准

优先问两个问题：

1. 这个操作本质上还是在编辑或查看当前记录吗？
2. 这个操作是否已经形成了独立的业务流程或配置面？

如果第二个问题的答案是“是”，默认不要继续塞进当前 CRUD 弹窗。

接口是否来自同一个 API 文件，不是判断依据。判断依据始终是交互形态和业务边界。

即使多个操作围绕同一类实体、甚至复用同一组接口，它们也不一定属于同一种 UI 承载面：

- 状态切换是直接行操作
- 区域绑定是同页独立弹窗
- 新增 / 修改才属于 CRUD 表单

## 不适用时怎么做

不适用当前 CRUD 弹窗时，默认有三种落地方式：

### 方式一：列表页直接行操作

适用于：

- 没有独立表单
- 只有确认、开关、单次状态变更
- 完成后只需要提示并刷新列表

设备状态切换通常就是这类模式：

```js
const handleStateBeforeChange = (row) => {
  return ElMessageBox.confirm(`确认要${row.state === 1 ? '关闭' : '开启'}该设备吗?`, '提示', { type: 'warning' })
}

const handleStateChange = async (row, value) => {
  try {
    const res = await BindAndStatus({ deviceId: row.id, regionId: row.regionId, deptId: row.deptId, state: value })
    responseHandler(res, '操作成功', () => {
      selectList()
    })
  } catch (error) {
    console.error(error)
  }
}
```

这种情况不要为了统一，把开关状态也包进 `add-or-update.vue`。

### 方式二：列表页保留触发，另起同页独立组件或独立弹窗

适用于：

- 仍然从当前列表进入
- 需要自己的状态、表单或接口
- 完成后只需要回刷当前列表

```vue
<script setup>
import ApproveDialog from './components/approve-dialog.vue'
import { ref } from 'vue'

const approveDialogRef = ref(null)

const handleOpenApprove = (row) => {
  approveDialogRef.value.open({ id: row.id, status: row.status })
}
</script>

<template>
  <el-button size="small" @click="handleOpenApprove(row)">审核</el-button>
  <ApproveDialog ref="approveDialogRef" @success="selectList" />
</template>
```

这种情况下，列表页只负责触发，审核逻辑、审核表单、审核提交都在 `ApproveDialog` 内部闭合。

如果这个独立操作非常轻，也可以先放在当前列表页里，但要保持一套独立状态，不与 CRUD 表单混用：

```js
const dialogVisible = ref(false)
const dialogForm = ref({})
const dialogFormRules = ref({
  regionId: [{ required: true, message: '必填项不能为空', trigger: 'change' }],
})

const handleBindRegion = (row) => {
  dialogForm.value = {
    deviceId: row.id,
    regionId: '',
    deptId: '',
    state: 1,
  }
  dialogVisible.value = true
}
```

这里的关键不是“必须拆成单文件组件”，而是“不能并回 CRUD 弹窗状态和表单里”。

### 方式三：直接做成独立页面

适用于：

- 流程步骤多
- 页面信息密度高
- 需要独立路由、返回链路或权限边界

```js
const handleOpenChildConfig = (row) => {
  router.push({
    path: '/module/function/child-config',
    query: { id: row.id },
  })
}
```

这类场景不要继续挂在 `add-or-update.vue` 里，也不要为了维持“看起来统一”再套一层大弹窗。

## 反例

下面这种把明显独立流程继续塞进当前弹窗的做法，后续通常会快速失控：

```js
const init = ({ type, id }) => {
  if (type === 'insert') {
    openInsertDialog()
  } else if (type === 'detail') {
    openDetailDialog(id)
  } else if (type === 'update') {
    openUpdateDialog(id)
  } else if (type === 'approve') {
    openApproveDialog(id)
  } else if (type === 'archive') {
    openArchiveDialog(id)
  }
}
```

## 重构时的处理顺序

如果旧代码已经出现上面的反例，按这个顺序拆：

1. 保留 `insert / detail / update` 在当前 CRUD 弹窗
2. 把 `approve / archive / child-config` 之类入口从 `init` 中拿出来
3. 如果只是轻量状态动作，改成列表页直接行操作
4. 如果需要单独表单，补自己的组件或独立弹窗
5. 如果已经形成完整流程，补独立页面或路由承载面
6. 最后清理旧弹窗里的遗留状态和分支
