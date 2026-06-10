# State Naming And Loading

## 状态拆分

弹窗内部至少拆出这些状态：

- `dialogType`：新增、详情、修改等场景
- `readonlyMode`：由场景派生出的只读态
- `recordLoading`：记录加载态
- `submitLoading`：提交加载态

不要用一个总 `dialogLoading` 覆盖所有流程。

```js
const dialogType = ref('insert')
const recordLoading = ref(false)
const submitLoading = ref(false)
const readonlyMode = computed(() => dialogType.value === 'detail')
```

## 命名偏好

- 用户直接触发的函数，使用 `handle` 前缀
- 内部编排、场景打开、数据装载，优先 `open`、`load`
- 布尔语义不强推 `isXxx`，优先贴近业务含义

参考片段：

```js
const handleDelete = async (row) => {
  // 用户点击删除
}

const openUpdateDialog = (id) => {
  // 内部场景打开
}

const loadRecord = async (id) => {
  // 内部数据装载
}
```

## loading 的使用边界

记录加载与提交加载作用在不同阶段，模板层面要显式区分：

```vue
<el-form
  v-loading="recordLoading"
  :disabled="readonlyMode || recordLoading"
>
  ...
</el-form>

<el-button
  v-if="!readonlyMode"
  :loading="submitLoading"
  :disabled="recordLoading"
  type="primary"
>
  提交
</el-button>
```
