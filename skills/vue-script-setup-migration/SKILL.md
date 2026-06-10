---
name: vue-script-setup-migration
description: 将旧式 Vue 业务页面或业务组件迁移到现代 script setup 的技能。用于 Options API、`defineComponent()`、带 `setup()` 的非 script setup 组件、以及带 `render()` / `h()` 的旧承载方式重构，请求表述包括“把老页面改成 script setup”“把 Options API 改成 Composition API”“把这个 defineComponent 组件迁到 script setup”“去掉 this / data / methods / mixins”。适用于旧页面、旧业务组件和旧 CRUD 页面的 Vue 写法迁移，但只处理框架层迁移与必要拆分，并优先贴近当前仓库已接受的现代承载方式。不用于新建页面、字段驱动生成，或本来就应该保留纯 Composition API render 形态的特殊组件。
---

# Vue Script Setup Migration

## Goal

把旧式 Vue 业务页面和业务组件迁移到当前默认接受的现代写法：普通页面和普通业务组件优先落到 `script setup`，并在需要时完成多文件拆分、职责收敛和副作用整理。

这个 skill 的重点是 Vue 框架层面的旧写法到新写法迁移。

- 处理语法承载方式：Options API、`defineComponent()`、非 `script setup` 的 `setup()` / `render()` / `h()`
- 处理结构迁移：单文件大页面拆分、状态和副作用显式化
- 不负责定义 CRUD 页面本身该怎么组织；只有在目标明确仍是 CRUD 场景时，才继续进入对应 CRUD 规范

## Use This Skill For

- 把所有 Options API 页面迁移成 `script setup`
- 把所有非 `script setup` 的简化 Composition API 业务组件迁移成 `script setup`
- 把单文件大页面拆成页面组合层、子组件和必要的 composable
- 清理 `this`、`mixins`、旧生命周期分散和旧实例上下文依赖
- 判断一个旧页面在迁移后应保持单文件还是拆成多文件

## Do Not Use This Skill For

- 新页面直接落地
- 字段驱动生成或模板引擎设计
- 只做 CRUD 结构评审、弹窗边界判断、列表页职责收敛
- 已经是现代 `script setup` 的普通组件微调
- 本来就属于纯函数组件、纯逻辑桥接组件或必须保留纯 Composition API `h()` / `render()` 的特殊组件

## Workflow

1. 先读取 `references/01-entry-and-target.md`，确认旧写法范围、目标基线和迁移顺序。
2. 再按问题类型补读：
   - 单文件大页面怎么拆：`references/02-splitting-and-target-structure.md`
   - `data / computed / methods / watch / lifecycle / this` 以及非 `script setup` 的 `setup()` 组件怎么迁：`references/03-non-script-setup-mapping.md`
   - 旧页面里混有列表、弹窗、独立操作时怎么分流：`references/04-scenario-handoff.md`
   - `setup()` / `h()` / `render()` 什么时候可以保留：`references/05-special-cases-and-exceptions.md`
3. 交付前使用 `references/06-review-checklist.md` 复查。

## Working Rules

- 在这个仓库里，迁移目标先服从仓库内已经被接受的现代实现基线，再服从通用 Vue 最佳实践。
- 先定目标承载面和组件边界，再改语法。
- 默认现代基线是 JavaScript `script setup`，不是继续包一层 `defineComponent`。
- 非特殊场景不用 `reactive()` 聚合整页或整块业务状态，优先 `ref()`、`computed()` 和工厂函数。
- 先把页面拆成“页面组合层 / 独立交互组件 / 复用逻辑”三类角色，再决定是否抽 composable。
- composable 只在复用、状态副作用较重或明显有独立逻辑闭包时提取，不机械抽离。
- 默认保持 SFC 内聚。单个业务场景的局部逻辑优先留在所属 SFC 内；页面过重时优先先拆组件，不优先拆 `helpers.js`。
- 如果逻辑确实已经脱离单页私有范围，再按性质决定：有状态、副作用、生命周期的抽 composable；纯通用能力再抽共享工具。
- 不要把组合式函数的结果通过 props 在业务组件之间传来传去。业务子组件依赖的 `useDict()`、路由、store、权限等能力，优先在组件内部按需获取。
- 非特殊场景不用 `h()` / `render()`；如果确实保留，也必须是纯 Composition API 形态，不能混回 Options API。
- 迁移时顺手清理 `this`、`mixins`、过滤器式遗留写法、无效深拷贝和不再需要的中间状态。
- 如果迁移后的目标仍然是“列表页 + 单记录弹窗伪页面”，再继续按对应 CRUD 规范收敛结构细节。

## Gotchas

- 不要做“语法翻译式迁移”：把 `data()` 改成 `ref()` 但仍然保留一个巨型页面。
- 不要为了少写 `.value` 就把搜索、表格、弹窗、提交状态全塞进一个 `reactive()` 大对象。
- 不要用 `getCurrentInstance()` 到处模拟 `this`；大多数旧依赖都应改成显式导入、模板 ref 或 `defineEmits()`。
- 不要因为旧代码用了 `defineComponent`、`render()` 或 `h()`，就在普通页面里继续保留这些壳。
- 不要把 `defineComponent({ render() {} })` 这种 Options API 风格 render 壳当成现代例外；特殊场景也必须是纯 Composition API。
- 不要把独立流程、独立配置或独立弹窗继续塞回同一个旧页面，只因为历史上它们写在一起。
- 不要为了“更清爽”把单页私有的表单工厂、列表归一化、payload 拼装默认拆成 `helpers.js`；这类逻辑默认先留在对应 SFC，或优先通过组件拆分消化。
- 不要把 `useDict()`、`useRoute()`、store 之类组合式函数的结果从父组件组装后再层层下传；这会把新的 Composition API 再做回旧式耦合链。
- 不要继续用标题、按钮文案或魔法字符串承担业务场景状态。
- 不要把所有旧页面都直接按 CRUD 处理；只有目标承载面已经确认仍是 CRUD 结构时才继续进入 CRUD 规范。

## Trigger Examples

- “把这个老的 options api 页面改成 `script setup`”
- “把这个非 `script setup` 的 composition api 组件改成 `script setup`”
- “把这个 `defineComponent` 页面拆成多文件 composition api，再收口到 `script setup`”
- “这个 Vue 单文件大页面太老了，帮我迁移并拆分结构”
- “去掉这个页面里的 `this`、`data`、`methods` 和 mixin 写法”
- “这个旧 CRUD 页面先迁到现代写法，再看要不要按当前 CRUD 模板收敛”

## Non-Trigger Examples

- “按当前 CRUD 模板新建一个列表页和弹窗页”
- “评审这个弹窗是否还应该留在 CRUD 页面里”
- “根据字段配置生成 CRUD 页面”
- “这个 `script setup` 组件里某个 watch 怎么写”
- “这个纯 render 函数组件要不要优化一下 vnode 结构”

## Validation Notes

- 确认普通页面和普通业务组件已经落到 `script setup`，没有残留 Options API 壳或非特殊场景的非 `script setup` 壳。
- 确认迁移不只是语法替换，而是完成了承载面和职责边界收敛。
- 确认状态没有被新的整页 `reactive()` 大对象重新糊回去。
- 确认副作用入口、加载流程、表单提交和局部弹窗状态已经显式化。
- 如果最终目标是 CRUD 页面，确认已再按对应 CRUD 规范校正结构和场景边界。
- 如果保留了 `setup()` / `h()` / `render()`，必须能说明这是特殊场景，而且实现仍然是纯 Composition API。

## Resource Navigation

- 迁移入口与目标基线：`references/01-entry-and-target.md`
- 拆分策略与目标结构：`references/02-splitting-and-target-structure.md`
- 所有非 `script setup` 旧写法到 `script setup` 映射：`references/03-non-script-setup-mapping.md`
- 场景分流与承载面交接：`references/04-scenario-handoff.md`
- 特殊场景例外：`references/05-special-cases-and-exceptions.md`
- 复查清单：`references/06-review-checklist.md`
