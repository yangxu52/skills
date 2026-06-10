# Form Validation And Submit

## 表单初始化

表单初始值使用工厂函数，避免多个场景共享同一个默认对象。

```js
const createDialogForm = () => ({
  name: '',
  status: '',
  remark: '',
})

const dialogForm = ref({})
```

如果表单里有嵌套对象或数组，默认直接写在工厂函数里，不为“看起来统一”提前再抽一层。

## 校验规则

表单规则是否响应式，要看是否会被场景联动替换。当前模板默认允许保留响应式写法。

```js
const dialogFormRules = ref({
  name: [{ required: true, message: '必填项不能为空', trigger: 'blur' }],
})
```

## 提交流程

默认使用 `async / await + try / catch / finally`。校验失败直接中断，提交成功后关闭弹窗并刷新列表。

```js
const handleDialogSubmit = async () => {
  const valid = await dialogFormRef.value.validate().catch(() => false)
  if (!valid) {
    return
  }

  submitLoading.value = true
  try {
    const data = dialogForm.value
    const action = data.id ? Update : Insert
    const res = await action(data)
    responseHandler(res, data.id ? '修改成功' : '新增成功', () => {
      handleDialogCancel()
      emit('refresh-list')
    })
  } catch (err) {
    console.error(err)
  } finally {
    submitLoading.value = false
  }
}
```

## 深拷贝

默认不在提交前做深拷贝。只有以下情况再处理：

- 提交前要做结构转换
- 请求封装会改写入参
- 表单值需要和原始记录做隔离比较
