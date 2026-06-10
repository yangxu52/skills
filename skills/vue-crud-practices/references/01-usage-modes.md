# Usage Modes

## 适用前提

这个技能默认处理两类任务：

- 新 CRUD 页面落地：字段、接口、字典、操作场景已知，但页面还没组织好
- 旧 CRUD 页面重构：页面能用，但结构、状态或异步流程已经变得混乱

如果需求已经不是“列表页 + 单记录弹窗伪页面”，不要强行套用这套参考。

## 先做适用性判断

优先判断当前操作是不是“查看或编辑当前单条记录本身”。

通常适用当前 CRUD 弹窗的场景：

- 新增
- 详情
- 修改
- 复制

通常不适用当前 CRUD 弹窗的场景：

- 审核
- 归档
- 独立子配置维护
- 多步骤流程
- 强状态流转操作

如果不适用，默认改成下面三种落地方式之一：

- 直接行操作：用户确认后直接请求，不引入新表单
- 同页独立操作：仍挂在当前列表页下，但拥有自己的弹窗和状态
- 独立页面：流程明显变重，需要自己的路由和页面结构

## 新页面落地

推荐顺序：

1. 先搭列表页职责和查询、分页、主操作入口
2. 再搭弹窗页场景和记录加载流程
3. 再补状态拆分、表单校验、提交
4. 最后判断是否有操作应拆出当前 CRUD

最小落点通常长这样：

```vue
<script setup>
import FormDialog from './add-or-update.vue'
import { ref } from 'vue'

const dialogRef = ref(null)

const handleOpenDialog = (type, id) => {
  dialogRef.value.init({ type, id })
}
</script>

<template>
  <el-button type="success" @click="handleOpenDialog('insert')">新增</el-button>
  <FormDialog ref="dialogRef" @refresh-list="selectList" />
</template>
```

如果发现某个操作已经不是单条记录的轻量查看或编辑，不要继续往 `add-or-update.vue` 增加新分支。

轻量状态操作，优先直接写成列表页行操作：

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

如果它需要自己的表单和提交链路，再单独起同页独立组件：

```vue
<script setup>
import FormDialog from './add-or-update.vue'
import ArchiveDialog from './components/archive-dialog.vue'
import { ref } from 'vue'

const dialogRef = ref(null)
const archiveDialogRef = ref(null)

const handleOpenDialog = (type, id) => {
  dialogRef.value.init({ type, id })
}

const handleOpenArchive = (row) => {
  archiveDialogRef.value.open({ id: row.id })
}
</script>

<template>
  <FormDialog ref="dialogRef" @refresh-list="selectList" />
  <ArchiveDialog ref="archiveDialogRef" @success="selectList" />
</template>
```

## 旧页面重构

推荐顺序：

1. 先保住现有业务行为
2. 先按交互形态划分承载面
3. 再收敛场景状态，不再依赖标题或隐式标记
4. 再拆分 loading 和异步收口
5. 再整理表单初始化、校验、提交
6. 最后判断是否要拆出独立组件或独立页面

先按下面顺序重构：

1. 盘点当前页面所有操作按钮和打开入口
2. 把操作分成三类：
   - 仍属于当前记录查看或编辑的，留在 `add-or-update.vue`
   - 只需要确认或轻量状态切换的，改成列表页直接行操作
   - 已经是独立流程或独立配置面的，抽到同页独立组件或独立页面
3. 先统一入口，再收敛状态、loading、校验和提交
4. 最后清理已经不该留在 CRUD 弹窗里的旧分支

如果旧代码已经混用了多个打开入口，先统一到一个入口，再做细节收敛：

```js
const init = ({ type, id }) => {
  if (type === 'insert') {
    openInsertDialog()
  } else if (type === 'detail') {
    openDetailDialog(id)
  } else if (type === 'update') {
    openUpdateDialog(id)
  }
}
```

如果旧代码里已经把独立流程塞进了同一个 `init`，重构时先把入口拆开：

```js
const handleOpenDialog = (type, id) => {
  dialogRef.value.init({ type, id })
}

const handleOpenApprove = (row) => {
  approveDialogRef.value.open({ id: row.id })
}
```

重构的目标是让每种操作回到合适的承载面。

如果重构目标还包含“老旧 Options API 单文件页面迁移到多文件拆分、Composition API、功能内聚”，那已经超出当前 skill 范围，先完成 Vue 写法迁移，再回到当前 CRUD 规范。

## 读取顺序

- 先看 `02-list-page-structure.md`
- 再看 `03-dialog-page-structure.md`
- 然后看 `04-state-naming-and-loading.md`
- 如果问题集中在表单，补读 `05-form-validation-and-submit.md`
- 如果不确定某个操作是否还应留在当前弹窗，读 `06-operation-boundaries.md`
