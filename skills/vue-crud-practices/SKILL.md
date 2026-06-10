---
name: vue-crud-practices
description: Vue 3 Composition API 管理端 CRUD 实践技能。用于新建或重构当前仓库里的列表页 + 弹窗伪页面这类 CRUD 页面，帮助对齐仓库内已接受的 CRUD 页面承载方式、列表页职责、弹窗场景、状态拆分、异步收口、表单提交和操作边界。适用于“按现有 CRUD 模板风格落地页面”“评审该页面是否偏离当前 CRUD 模式”“判断某个操作应留在 CRUD 弹窗还是拆成独立承载面”等请求。不用于字段驱动生成、FreeMarker 模板设计，或老旧单文件页面迁移到多文件 Composition API 架构。
---

# Vue CRUD Practices

## Overview

使用这个技能对齐常见的 Vue 3 CRUD 页面实现方式。

它覆盖两类任务：

- 新 CRUD 页面落地
- 既有 CRUD 页面重构

默认语境是“列表页 + 单记录弹窗伪页面”。如果需求已经明显跨流程、跨子域，或已经变成独立配置面，先判断是否还应继续套用这套模式；不适用时，应该改成同页独立操作、独立组件或独立页面，而不是继续往 `add-or-update.vue` 里塞分支。

如果目标页面还不是当前普遍接受的 `<script setup>` 写法，先使用 `vue-script-setup-migration` 指导迁移。当前 skill 只在目标明确属于 CRUD 场景时继续规范。

## Use This Skill For

- 按当前 CRUD 模板风格组织一个新页面
- 把旧 CRUD 页面收敛到当前实现约定
- 评审一个 CRUD 页面是否偏离当前结构和状态边界
- 判断某个操作应该落在 CRUD 弹窗、同页独立操作、独立组件还是独立页面

## Do Not Use This Skill For

- 字段驱动代码生成
- FreeMarker 或其他模板引擎设计
- 通用 Vue 教程式说明
- 脱离当前 CRUD 模式的大型业务流设计
- 老旧 Options API 单文件大页面迁移到多文件拆分、Composition API、功能内聚的改造方案

## Workflow

1. 先读取 `references/01-usage-modes.md`，确认当前任务属于新页面落地还是旧页面重构，并先做一次“是否适用当前 CRUD 弹窗”的判断。
2. 再按问题类型读取对应参考文件：
   - 列表页职责与组织：`references/02-list-page-structure.md`
   - 弹窗页职责与场景：`references/03-dialog-page-structure.md`
   - 状态拆分、命名、loading：`references/04-state-naming-and-loading.md`
   - 表单初始化、校验、提交：`references/05-form-validation-and-submit.md`
   - 操作是否应拆出当前 CRUD：`references/06-operation-boundaries.md`
   - 当前默认接受的实现基线：`references/07-default-baseline.md`
   - 如果需要直接参考完整骨架，再看 `assets/index.reference.vue` 与 `assets/add-or-update.reference.vue`
3. 交付前使用 `references/08-review-checklist.md` 复查。

## Working Rules

- 在这个仓库里，CRUD 落地先服从当前已经被接受的模板家族和承载方式，再补通用 Vue 细节。
- 优先贴近当前模板的真实使用场景，不追求理想化架构。
- 优先降低理解和修改成本，不为形式统一引入额外抽象。
- 页面可以承担组合层职责，但不要把明显独立的流程硬塞进一个弹窗。
- 先判断操作承载面，再决定是否写新组件、写行操作函数，还是单独起页面。
- 规则默认服务于“可读、可改、可复制”，不是服务于“看起来更工程化”。

## Gotchas

- 不要用 `dialogTitle` 反推业务场景。业务判断依赖 `dialogType`。
- 不要用一个总 `dialogLoading` 覆盖记录加载和提交加载。拆成 `recordLoading` 与 `submitLoading`。
- 不要把列表数据、分页数据、查询状态挪进弹窗页。它们属于列表页。
- 不要为了形式统一强推全量 `props / emits` 驱动。当前模板接受 `ref.init({ type, id })`。
- 不要默认在提交前做深拷贝。只有请求封装会改写入参或提交前需要结构转换时才处理。
- 不要把组合式函数的结果通过 props 在业务父子组件之间来回透传；像 `useDict()` 这类依赖，优先在真正使用的业务组件内部按需获取。
- 不要把当前 CRUD 家族默认替换成裸 `el-table`；原生表格不是禁用项，但在当前内部写法里，`DynamicTable + tableConfig` 是优先基线。
- 不要为了“看起来更清爽”默认把单页私有转换逻辑拆成 `helpers.js`；先保持 SFC 内聚，页面重时先拆组件。
- 不要把审核、归档、独立子配置维护这类操作继续塞进 CRUD 弹窗。
- 如果某个操作已经不适合当前 CRUD 弹窗，先判断它属于直接行操作、同页独立弹窗，还是独立页面，再决定承载面。
- 不要因为接口文件相同或接口路径相近，就把不同交互形态的操作合并进同一个 CRUD 弹窗。
- 不要把当前 skill 当成“老旧页面迁移方案”。当前 skill 只负责 CRUD 场景规范，不负责 Vue 框架层的旧写法到新写法迁移。

## Trigger Examples

- “按现有 Vue CRUD 模板风格落一个列表页和弹窗页”
- “帮我把这个旧 CRUD 页面重构到当前约定”
- “这个弹窗页面的 loading 和场景状态怎么拆”
- “这个操作还适不适合留在当前 CRUD 弹窗里”
- “评审一下这个管理端 CRUD 页面有没有偏离当前实践”

## Non-Trigger Examples

- “根据字段定义直接生成 CRUD 页面代码”
- “帮我设计 FreeMarker 模板变量体系”
- “Vue 3 Composition API 最佳实践是什么”
- “这个需求应该做成向导页还是多步骤工作流”
- “把这个老旧 Options API 单文件页面改造成多文件 Composition API”

## Validation Notes

- 确认页面仍然符合“列表页 + 弹窗伪页面”这套前提，或者明确给出不适用的理由。
- 确认状态拆分、异步收口、表单提交流程与当前参考文件一致。
- 如果是重构，优先验证业务行为未变，再验证结构是否收敛。
- 如果某个操作不再适用当前 CRUD 模式，确认它已经被拆成独立组件或独立页面，并拥有自己的入口、状态和提交流程。

## Reference Map

- 使用方式与切入顺序：`references/01-usage-modes.md`
- 列表页结构：`references/02-list-page-structure.md`
- 弹窗页结构：`references/03-dialog-page-structure.md`
- 状态、命名与 loading：`references/04-state-naming-and-loading.md`
- 表单、校验与提交：`references/05-form-validation-and-submit.md`
- 操作边界：`references/06-operation-boundaries.md`
- 默认实现基线：`references/07-default-baseline.md`
- 复查清单：`references/08-review-checklist.md`
- 完整参考资产：`assets/index.reference.vue`、`assets/add-or-update.reference.vue`
