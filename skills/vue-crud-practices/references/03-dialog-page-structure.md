# Dialog Page Structure

## 职责边界

弹窗页默认负责：

- 新增场景
- 详情场景
- 修改场景
- 单条记录加载
- 表单提交

它不是纯展示组件，也不负责列表数据与分页数据。

它默认只承载“当前单条记录的查看与编辑”。如果一个操作已经变成审核、归档、子配置维护或多步骤流程，应另起组件或独立页面，不继续扩张这个弹窗页。

## 场景组织

业务场景靠 `dialogType` 区分，展示文案靠 `dialogTitle` 控制。不要反过来依赖标题推业务。

```js
const dialogVisible = ref(false)
const dialogType = ref('insert')
const dialogTitle = ref('')

const openInsertDialog = () => {
  dialogType.value = 'insert'
  dialogTitle.value = '新增'
  dialogVisible.value = true
}
```

## 对外入口

当前模板接受对象式入口，不强推改成全量 `props / emits` 驱动。

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

defineExpose({ init })
```

## 组件内部自己取组合式依赖

如果弹窗组件本身依赖：

- `useDict()`
- 路由
- store
- 权限或其他组合式上下文

优先在弹窗组件内部按需获取。

不要把这些组合式函数的结果在父组件里先组装，再通过 props 传给业务弹窗。props 更适合承载业务输入，而不是父层替子组件准备好的组合式上下文。

参考片段：

```vue
<script setup>
import { useDict } from '@/components/Dict/useDict.js'

const dict = useDict(['DEVICE_TYPE'])
</script>

<template>
  <el-select>
    <el-option v-for="item in dict.DEVICE_TYPE" :key="item.value" :label="item.label" :value="item.value" />
  </el-select>
</template>
```

## 记录加载流程

详情与修改可以共用同一套记录加载流程。先开弹窗，再拉数据；加载失败则关闭弹窗。

```js
const openDialogWithRecord = async (type, title, id) => {
  dialogType.value = type
  dialogTitle.value = title
  dialogVisible.value = true
  recordLoading.value = true
  try {
    const res = await Get(id)
    dialogForm.value = res.result
  } catch (err) {
    dialogVisible.value = false
    console.error(err)
  } finally {
    recordLoading.value = false
  }
}
```

## 最小弹窗模板参考

```vue
<script setup>
import { computed, ref } from 'vue'
import { Get, Insert, Update } from '@/api/module/function.js'
import { useDict } from '@/components/Dict/useDict.js'

const emit = defineEmits(['refresh-list'])
const dict = useDict(['STATUS'])
const dialogVisible = ref(false)
const dialogType = ref('insert')
const dialogTitle = ref('')
const recordLoading = ref(false)
const submitLoading = ref(false)
const dialogFormRef = ref(null)
const dialogForm = ref({})
const readonlyMode = computed(() => dialogType.value === 'detail')

const init = ({ type, id }) => {
  if (type === 'insert') {
    dialogType.value = 'insert'
    dialogTitle.value = '新增'
    dialogForm.value = {}
    dialogVisible.value = true
  } else {
    openDialogWithRecord(type, type === 'detail' ? '详情' : '修改', id)
  }
}

const openDialogWithRecord = async (type, title, id) => {
  dialogType.value = type
  dialogTitle.value = title
  dialogVisible.value = true
  recordLoading.value = true
  try {
    const res = await Get(id)
    dialogForm.value = res.result
  } catch (error) {
    dialogVisible.value = false
    console.error(error)
  } finally {
    recordLoading.value = false
  }
}

defineExpose({ init })
</script>

<template>
  <el-dialog v-model="dialogVisible" :title="dialogTitle" destroy-on-close>
    <el-form ref="dialogFormRef" v-loading="recordLoading" :model="dialogForm" :disabled="readonlyMode || recordLoading">
      <el-form-item label="状态">
        <el-select v-model="dialogForm.status">
          <el-option v-for="item in dict.STATUS" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="dialogVisible = false">关闭</el-button>
      <el-button v-if="!readonlyMode" type="primary" :loading="submitLoading" :disabled="recordLoading">提交</el-button>
    </template>
  </el-dialog>
</template>
```
