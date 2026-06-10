# Non Script Setup To Script Setup Mapping

## 迁移原则

不要机械做一一翻译。先保住行为，再把状态、依赖和副作用改成显式模型。

## 常见映射

- `data()` -> 优先拆成多个 `ref()` / 工厂函数，非特殊场景不用 `reactive()`
- `computed` -> `computed()`
- `methods` -> 普通函数
- `watch` -> `watch()` / `watchEffect()`，只用于副作用
- `created` / `mounted` / `activated` -> 显式加载函数 + 对应生命周期
- `this.$refs` -> 模板 `ref`
- `this.$emit` -> `defineEmits()`
- `this.$route` / `this.$router` -> 路由 composable
- `mixins` -> composable 或普通工具函数
- 过滤器式写法 -> `computed`、局部函数或工具函数
- `defineComponent({ setup() { return { ... } } })` -> 直接平铺到 `script setup`
- `defineComponent({ render() {} })` / 业务型 `h()` 组件 -> 普通场景改回模板；特殊场景才保留纯 Composition API render 形态

## `data()` 不要原样搬家

旧代码：

```js
data() {
  return {
    loading: false,
    dialogVisible: false,
    dialogForm: {},
  }
}
```

目标不是把它改成一个更大的 `reactive({ ... })`，而是按职责拆开：

```js
const loading = ref(false)
const dialogVisible = ref(false)
const dialogForm = ref(createDialogForm())

const createDialogForm = () => ({
  name: '',
  state: 1,
})
```

这样表单初始化、重置和场景切换才容易控制。

## 非特殊场景默认不用 `reactive()`

不要把“迁移后少写 `.value`”当成设计目标。

下面这种写法默认不接受：

```js
const state = reactive({
  loading: false,
  list: [],
  dialogVisible: false,
  dialogForm: {},
  submitLoading: false,
})
```

它只是把旧时代的大状态团换了个 API。

默认应该拆成：

```js
const loading = ref(false)
const list = ref([])
const dialogVisible = ref(false)
const dialogForm = ref(createDialogForm())
const submitLoading = ref(false)
```

只有在“单个对象整体传递更自然、且不会频繁整体替换”的特殊小范围状态里，才考虑 `reactive()`。

## `methods` 要改成显式函数，不再依赖 `this`

旧代码：

```js
methods: {
  openEdit(row) {
    this.dialogVisible = true
    this.dialogForm = { ...row }
  },
}
```

迁移后：

```js
const openEdit = (row) => {
  dialogVisible.value = true
  dialogForm.value = { ...row }
}
```

函数依赖什么状态，就直接闭包捕获什么状态。

## 非 `script setup` 的 `setup()` 组件怎么迁

旧代码：

```js
export default defineComponent({
  setup() {
    const loading = ref(false)
    const list = ref([])

    const selectList = async () => {}

    return {
      loading,
      list,
      selectList,
    }
  },
})
```

迁移后：

```vue
<script setup>
import { ref } from 'vue'

const loading = ref(false)
const list = ref([])

const selectList = async () => {}
</script>
```

重点不是“把 `setup()` 保留下来”，而是把非 `script setup` 壳去掉。

## 生命周期先抽加载函数

不要把 `mounted()` 的内容直接原样塞进 `onMounted()`。

优先写成：

```js
const selectList = async () => {
  loading.value = true
  try {
    // await request
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  selectList()
})
```

这样后续查询、重置、翻页都能复用同一个入口。

## 校验器不要继续依赖 `this`

旧代码常见写法：

```js
validateLowValue(rule, value, callback) {
  if (value > this.dialogForm.highValue * 1) {
    callback(new Error('低报值不能大于高报值'))
  } else {
    callback()
  }
}
```

迁移后直接闭包表单状态：

```js
const dialogForm = ref(createDialogForm())

const validateLowValue = (_, value, callback) => {
  if (value === '' || value == null) {
    callback(new Error('低报值不能为空'))
    return
  }
  if (Number(value) > Number(dialogForm.value.highValue)) {
    callback(new Error('低报值不能大于高报值'))
    return
  }
  callback()
}
```

## `this` 的替代优先级

优先级如下：

1. 显式导入模块函数
2. 模板 `ref`
3. `defineEmits()` / `defineExpose()`
4. 路由、store、字典等官方或既有 composable

`getCurrentInstance()` 只在确实没有更干净出口时兜底，不要拿它继续模拟 Options API 的心智。

## `render()` / `h()` 的迁移规则

如果旧代码里的 `render()` / `h()` 只是为了渲染普通表单、列表或详情布局，优先改回模板和 `script setup`。

只有下面情况才考虑保留：

- 组件本质上是 render-driven
- 模板无法自然表达 vnode 组合
- 它是函数组件或渲染桥接层

即使保留，也必须是纯 Composition API。不要保留 `render` 选项式写法。

细则读 `05-special-cases-and-exceptions.md`。

## 迁移后常见收口

至少检查这些遗留物是否还能删除：

- 不再使用的 `mixins`
- 只为 `this` 服务的中间变量
- 只在旧标题驱动逻辑下存在的状态
- 旧式链式异步里重复的 loading 收口
- “先深拷贝再提交”但实际上没有改写入参的无效代码
