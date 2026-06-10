# Entry And Target

## 什么算“旧写法”

这个 skill 只关注 Vue 框架层面的旧写法迁移。

它处理的是两大类旧写法：

- 所有 Options API 及其变种
- 所有非 `script setup` 的简化 Composition API 业务组件

下面几类都属于迁移范围。

### 1. 所有 Options API 及其变种

- `export default { data, computed, methods, watch, mounted }`
- `defineComponent({ data, computed, methods, watch, mounted })`
- `defineComponent({ mixins, data, methods })`
- `defineComponent({ render() {} })`，但本质仍然是普通业务页面或普通业务组件
- Options API 与 `setup()` 混写，导致状态分散、数据流不清晰的组件

### 2. 所有非 `script setup` 的简化 Composition API 业务组件

- `defineComponent({ setup() { return { ... } } })`
- `defineComponent({ setup() { return () => ... } })`
- 用 `h()` / `render()` 承载普通列表、表单、详情、弹窗的业务组件
- 只是换成 `setup()`，但结构仍然是旧时代单文件大页的组件

判断标准不是“有没有 `defineComponent`”，而是它是不是仍然以非 `script setup` 的旧组织方式承载普通业务页面或普通业务组件。

## 现代目标基线

默认目标不是“把 Options API 改成另一种对象写法”，而是下面这套基线：

- 普通页面和普通业务组件优先使用 `script setup`
- 非特殊场景默认不用 `reactive()` 聚合整页或整块业务状态
- 页面先按职责拆分，再决定哪些逻辑保留在页面、哪些抽到子组件、哪些抽到 composable
- 默认保持 SFC 内聚，单页私有逻辑不为了整洁感默认外流成 `helpers.js`
- 状态和副作用改成显式依赖，不再依赖 `this`
- 场景状态、加载状态、提交状态分别建模，不继续混成一个大对象
- 非特殊场景不继续保留 `h()` / `render()`

如果目标仍然属于当前仓库已经存在的现代页面家族，迁移后的承载方式也要优先贴近该家族，而不是顺手重写成一套更通用、但和仓库现状脱节的 Vue 实现。

普通页面的目标通常类似这样：

```vue
<script setup>
import { onMounted, ref } from 'vue'
import FormDialog from './components/FormDialog.vue'

const loading = ref(false)
const list = ref([])
const dialogRef = ref(null)

const selectList = async () => {
  loading.value = true
  try {
    // await request
  } finally {
    loading.value = false
  }
}

const handleOpenDialog = (payload) => {
  dialogRef.value.init(payload)
}

onMounted(() => {
  selectList()
})
</script>
```

## 先定“迁移目标”再开工

推荐顺序：

1. 盘点旧页面承担了哪些职责
2. 先判断它应该迁成一个更清晰的单文件组件，还是拆成多个承载面
3. 再开始做语法层迁移
4. 最后删除旧壳和遗留中间状态

如果第二步没做，最终结果通常只是“旧页面换了个语法”，不会真正变清晰。

## 先看的三个问题

开始迁移前先回答：

1. 这个页面是不是把搜索、表格、弹窗、独立操作、图表或详情区全塞在一起了？
2. 哪些交互应该留在当前页面组合层，哪些应该拆成独立组件？
3. 迁移后的目标是不是仍然属于 CRUD 列表页 + 弹窗页？

第三个问题如果答案是“是”，语法迁移完成后再按对应 CRUD 规范收敛结构。

这里的职责分界要保持清楚：

- 当前 skill 负责 Vue 写法迁移、状态和副作用收口、必要拆分
- CRUD 场景本身的页面结构、弹窗边界、列表页职责和场景规范，不在当前 skill 内定义

这里还要补一层判断：

- 如果迁移目标仍然属于仓库现有 CRUD 家族，后续要优先贴近那套承载方式
- 如果只是单页私有的表单工厂、转换函数、payload 拼装，不要默认抽成独立 `helpers.js`
- 如果子组件本身依赖组合式函数，如 `useDict()`、路由、store、权限能力，优先在组件内部按需获取，不要父层聚合后再透传

## 何时不是本 skill 的主战场

下面几种情况不要强行套这个 skill：

- 需求本来就是新页面落地
- 组件已经是 `script setup`，只是局部逻辑要微调
- 组件本质上是渲染桥接器、函数组件或 provider 类组件

这些场景的例外细节，读 `05-special-cases-and-exceptions.md`。
