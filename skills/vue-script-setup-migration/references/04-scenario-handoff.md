# Scenario Handoff

## 这个文件解决什么问题

很多旧页面不是纯列表，也不是纯表单，而是：

- 查询
- 表格
- 新增 / 详情 / 修改弹窗
- 行状态开关
- 其他独立弹窗或独立操作

这类页面迁移时，最容易犯的错误是把所有东西继续塞回一个页面，或者反过来把所有东西都塞进同一个 CRUD 弹窗。

这里要先分清职责：

- 当前 skill 负责把旧页面从旧 Vue 写法迁到现代 `script setup`，并把承载面拆清
- CRUD 页面后续怎么规范落点，不在当前 skill 内展开

## 先分三类操作

先把页面里的按钮和入口分成三类：

- 当前记录本身的查看或编辑
- 只需确认或轻量切换的直接行操作
- 独立配置、独立流程、独立弹窗

这一步做完后，才能决定哪些属于 CRUD，哪些不属于。

## 典型落点

第一类通常进入 CRUD 弹窗：

```js
const handleOpenForm = (type, id) => {
  formDialogRef.value.init({ type, id })
}
```

第二类通常直接留在列表页：

```js
const handleStateBeforeChange = (row) => {
  return ElMessageBox.confirm(`确认切换 ${row.name} 的状态吗？`, '提示', { type: 'warning' })
}

const handleStateChange = async (row, value) => {
  // await update state
}
```

第三类通常做成同页独立组件：

```js
const handleOpenBindDialog = (row) => {
  bindDialogRef.value.open({ id: row.id })
}
```

## 页面组合层示例

```vue
<script setup>
import { ref } from 'vue'
import FormDialog from './components/FormDialog.vue'
import BindDialog from './components/BindDialog.vue'

const formDialogRef = ref(null)
const bindDialogRef = ref(null)

const handleOpenForm = (type, id) => {
  formDialogRef.value.init({ type, id })
}

const handleOpenBindDialog = (row) => {
  bindDialogRef.value.open({ id: row.id })
}
</script>
```

这里有两个独立承载面：

- `FormDialog` 负责当前记录的新增 / 详情 / 修改
- `BindDialog` 负责独立绑定流程

不要因为它们都和同一行数据有关，就硬塞进同一个表单弹窗。

如果这些子组件本身依赖字典、路由、store 或权限能力，优先让它们在组件内部按需获取，不要为了“父层统一管理”把组合式函数结果再当 props 透传。

## 什么时候继续进入 CRUD 规范

满足下面条件时，迁移完结构和语法后，再继续进入 CRUD 规范：

- 目标页面明确仍是“列表页 + 单记录弹窗伪页面”
- 核心问题已经不是旧语法，而是 CRUD 状态、命名、loading、提交和弹窗边界
- 你正在整理 `index.vue + add-or-update.vue` 这种承载方式

## 什么时候不要继续走 CRUD 规范

下面情况继续由当前 skill 处理：

- 页面不再是 CRUD 形态，而是多区域组合页
- 操作已经被拆成多个兄弟组件或独立页面
- 主要问题仍然是拆分和迁移，而不是 CRUD 结构收敛

## 迁移时的关键提醒

- 不要为了“统一”把所有操作都迁成 `dialogRef.init(...)`
- 不要为了“收敛”把所有弹窗都变成 `add-or-update.vue`
- 不要让旧页面历史结构决定新页面边界
- 不要因为页面要拆分，就默认把局部逻辑拆成 `helpers.js`；先问它是不是仍然属于当前 SFC 的私有职责
