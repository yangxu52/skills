# Special Cases And Exceptions

## 默认规则

普通页面和普通业务组件，默认都应该迁成 `script setup`。

下面这些例外，只是说明“可以不强制 `script setup`”，不是允许继续回到 Options API。

非纯函数组件、非纯逻辑桥接组件、非特殊渲染场景，默认不用 `h()` / `render()`。

如果确实保留 `h()` / `render()`，也必须是纯 Composition API 形态，不能保留 `data`、`computed`、`methods`、生命周期对象钩子或 `render` 选项式壳。

## 可以保留纯 Composition API `setup()` / `h()` / `render()` 的情况

### 1. 纯渲染桥接组件

组件的核心职责是动态拼 vnode、转发 slot、包装第三方渲染契约。

例如：

```js
import { defineComponent, h } from 'vue'

export default defineComponent({
  name: 'PermissionGate',
  props: {
    allowed: Boolean,
  },
  setup(props, { slots }) {
    return () => (props.allowed ? slots.default?.() : h('span', '无权限'))
  },
})
```

### 2. 必须以函数组件表达的极薄组件

组件几乎没有内部状态，只负责一个极轻的 vnode 包装层。

### 3. provider / bridge 一类纯逻辑组件

它本身不承载普通业务模板，而是提供上下文、注入能力或渲染桥接。

例如：

```js
import { defineComponent, h, provide } from 'vue'

export default defineComponent({
  name: 'FeatureProvider',
  setup(_, { slots }) {
    provide('feature-key', { enabled: true })
    return () => h('div', slots.default?.())
  },
})
```

## 不构成例外的情况

下面这些不算特殊场景，仍然应该迁成 `script setup`：

- 普通列表页
- 普通详情页
- 普通查询表单
- 普通新增 / 修改弹窗
- 普通卡片、表格、描述区
- 只是因为“历史上这么写”而存在的 `render()` / `h()`
- 只是因为想少写 `.value` 就继续保留非 `script setup` 壳

## 特殊场景也不能带着 Options API 旧壳

即使属于特殊场景，也不要保留下面这些遗留写法：

- `data`
- `computed`
- `methods`
- `watch`
- 生命周期对象钩子
- `this` 驱动的数据流
- `render()` 选项式写法

如果保留 `setup()` / `h()` / `render()`，它应该是一个明确、克制、现代的纯 Composition API 组件。

## 判断问题

迁移前先问自己：

1. 这个组件是不是主要在处理 vnode，而不是普通业务模板？
2. 模板语法是不是已经明显不适合表达它？
3. 如果改成 `script setup` 模板写法，会不会反而更绕？

只有三个问题里至少两个答案明显是“是”，才值得保留 render 方案。
