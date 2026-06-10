<script setup>
import { computed, ref } from 'vue'
import { Get, Insert, Update } from '@/api/example/referenceCrud.js'
import { useDict } from '@/components/Dict/useDict'
import { responseHandler } from '@/utils/tools'

defineOptions({ name: 'CrudReferenceFormDialog' })

const emit = defineEmits(['refresh-list'])
const dict = useDict(['ENTITY_TYPE', 'COMMON_STATUS'])
const dialogVisible = ref(false)
const dialogType = ref('insert')
const dialogTitle = ref('')
const recordLoading = ref(false)
const submitLoading = ref(false)
const dialogFormRef = ref(null)
const dialogForm = ref({})
const readonlyMode = computed(() => dialogType.value === 'detail')

const createDialogForm = () => ({
  name: '',
  type: '',
  status: '',
  remark: '',
  createTime: '',
})

const dialogFormRules = ref({
  name: [{ required: true, message: '请输入名称', trigger: 'blur' }],
  type: [{ required: true, message: '请选择类型', trigger: 'change' }],
  status: [{ required: true, message: '请选择状态', trigger: 'change' }],
  createTime: [{ required: true, message: '请选择创建时间', trigger: 'change' }],
})

const handleDialogCancel = () => {
  dialogForm.value = {}
  dialogFormRef.value?.resetFields()
  dialogVisible.value = false
}

const handleDialogSubmit = async () => {
  const valid = await dialogFormRef.value?.validate().catch(() => false)
  if (!valid) {
    return
  }

  submitLoading.value = true
  try {
    const data = dialogForm.value
    const action = data.id ? Update : Insert
    const successMessage = data.id ? '修改成功' : '新增成功'
    const res = await action(data)
    responseHandler(res, successMessage, () => {
      handleDialogCancel()
      emit('refresh-list')
    })
  } catch (error) {
    console.error(error)
  } finally {
    submitLoading.value = false
  }
}

const openInsertDialog = () => {
  dialogType.value = 'insert'
  dialogTitle.value = '新增'
  dialogForm.value = createDialogForm()
  dialogVisible.value = true
}

const openDialogWithRecord = async (type, title, id) => {
  dialogType.value = type
  dialogTitle.value = title
  dialogForm.value = {}
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

const openDetailDialog = (id) => {
  openDialogWithRecord('detail', '详情', id)
}

const openUpdateDialog = (id) => {
  openDialogWithRecord('update', '修改', id)
}

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
</script>

<template>
  <el-dialog v-model="dialogVisible" :title="dialogTitle" append-to-body destroy-on-close width="80%" @close="handleDialogCancel">
    <el-form
      ref="dialogFormRef"
      v-loading="recordLoading"
      class="dialog-form"
      :model="dialogForm"
      :rules="dialogFormRules"
      :disabled="readonlyMode || recordLoading"
      label-position="top">
      <el-form-item label="名称" prop="name">
        <el-input v-model="dialogForm.name" placeholder="请输入名称" style="width: 100%" />
      </el-form-item>

      <el-form-item label="类型" prop="type">
        <el-select v-model="dialogForm.type" clearable filterable placeholder="请选择类型" style="width: 100%">
          <el-option v-for="item in dict.ENTITY_TYPE" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
      </el-form-item>

      <el-form-item label="状态" prop="status">
        <el-select v-model="dialogForm.status" clearable filterable placeholder="请选择状态" style="width: 100%">
          <el-option v-for="item in dict.COMMON_STATUS" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
      </el-form-item>

      <el-form-item label="备注" prop="remark">
        <el-input v-model="dialogForm.remark" type="textarea" :rows="4" placeholder="请输入备注" style="width: 100%" />
      </el-form-item>

      <el-form-item label="创建时间" prop="createTime">
        <el-date-picker v-model="dialogForm.createTime" type="datetime" value-format="YYYY-MM-DD HH:mm:ss" placeholder="请选择创建时间" style="width: 100%" />
      </el-form-item>
    </el-form>

    <template #footer>
      <span class="dialog-footer">
        <el-button @click="handleDialogCancel">关闭</el-button>
        <el-button v-if="!readonlyMode" :loading="submitLoading" :disabled="recordLoading" type="primary" @click="handleDialogSubmit">提交</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<style lang="scss" scoped>
.dialog-form {
  max-height: 70vh;
  padding: 0 1rem 0 0;
  overflow-y: auto;
  overflow-x: hidden;
}
</style>
