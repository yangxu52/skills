# Splitting And Target Structure

## 先按承载面拆，不要先按语法拆

单文件大页面最常见的问题不是“用了 Options API”，而是把太多交互承载面糊在一起。

优先按下面顺序拆：

- 页面组合层：路由页、数据入口、全局刷新入口、少量跨区域编排
- 独立交互组件：查询表单、表格区、详情区、表单弹窗、独立操作弹窗
- 复用逻辑：列表加载、表单初始化、复杂副作用、跨组件共享的状态逻辑

先拆承载面，再决定每个承载面内部是单文件还是 composable。

## 常见拆分信号

满足任意一条，就不该继续维持单文件大页：

- 一个页面同时包含查询、表格、弹窗、独立状态操作和次级弹窗
- 页面里存在两个以上互不从属的提交流程
- 模板里已经自然分成多个视觉和交互区块
- 某段状态和函数只服务于一个局部交互，但仍然挂在整个页面根部

## 目标结构示例

旧页面如果同时有查询、列表、编辑弹窗和独立绑定弹窗，目标结构更接近这样：

```text
feature/
  index.vue
  components/
    SearchForm.vue
    DataTable.vue
    FormDialog.vue
    BindDialog.vue
  composables/
    useListState.js
```

不是每次都要把 `composables/` 建出来。只有列表状态明显复杂、会复用，或页面组合层已经过重时再抽。普通业务组件的默认目标仍然是 `script setup` 模板，不是把页面拆完后继续保留 `render()` 壳。

## 页面组合层示例

```vue
<script setup>
import { ref } from 'vue'
import SearchForm from './components/SearchForm.vue'
import DataTable from './components/DataTable.vue'
import FormDialog from './components/FormDialog.vue'
import BindDialog from './components/BindDialog.vue'

const list = ref([])
const loading = ref(false)
const formDialogRef = ref(null)
const bindDialogRef = ref(null)

const selectList = async () => {
  // load list
}

const handleOpenForm = (payload) => {
  formDialogRef.value.init(payload)
}

const handleOpenBind = (row) => {
  bindDialogRef.value.open({ id: row.id })
}
</script>
```

这里的页面只负责组合，不再承担每个局部弹窗的全部内部状态。

## 什么时候抽子组件

优先抽成子组件的情况：

- 它有自己的显式输入和输出
- 它有自己的提交、关闭、初始化或局部加载链路
- 它本身就是一个独立交互面

可以先留在页面里的情况：

- 只是一两个很薄的格式化函数
- 只服务于当前页面、不会形成独立交互面的微小区块
- 抽出去反而让数据流更绕

## 什么时候抽 composable

只有在下面情况才建议抽 composable：

- 同一套逻辑会被两个组件复用
- 某段逻辑以状态 + 请求 + 副作用为中心，已经天然像一个闭包
- 页面组合层已经因为列表状态或表单编排过重

不要把“任何函数都抽成 composable”当作现代化本身。

## 默认不要先拆 `helpers.js`

页面迁移时，默认优先顺序是：

1. 保持所属 SFC 内聚
2. 页面过重时先拆子组件
3. 逻辑具备复用闭包特征时再抽 composable
4. 纯通用能力再抽共享工具

不要把单页私有的表单工厂、列表归一化、payload 拼装、局部格式化默认拆成 `helpers.js`。这类拆法常见后果不是更清晰，而是把一个还能在 SFC 内完整阅读的业务场景拆成多个没有复用价值的小文件。

## 不要把组合式能力做成父传上下文

如果子组件本身就依赖：

- `useDict()`
- 路由能力
- store
- 权限、字典、当前模块上下文

优先让子组件在内部按需获取。

不要为了“统一入口”或“减少重复调用”，把这些组合式函数的结果先集中到父层，再通过 props 一层层传下去。这种做法会把 Composition API 再退回成上层聚合、下层透传的耦合结构。

## 不要把结构拆分误导成 CRUD 强塞

如果旧页面里有多个弹窗或多个提交流程，不代表它们都该变成同一个 `add-or-update.vue`。

拆分时优先问：

- 它是不是当前记录本身的查看或编辑？
- 它是不是一个直接确认即可完成的行操作？
- 它是不是独立配置或独立流程？

如果答案不同，承载面也应该不同。涉及场景分流和承载面交接，读 `04-scenario-handoff.md`。
