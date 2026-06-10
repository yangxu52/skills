<script setup>
import { onMounted, ref } from 'vue'
import FormDialog from './add-or-update.reference.vue'
import { Delete, List } from '@/api/example/referenceCrud.js'
import { useDict } from '@/components/Dict/useDict'
import { responseHandler } from '@/utils/tools'

defineOptions({ name: 'CrudReferencePage' })

const dict = useDict(['ENTITY_TYPE', 'COMMON_STATUS'])

const tableConfig = {
  table: { stripe: true, highlightCurrentRow: true },
  column: [
    { prop: 'index', type: 'index', label: '序号', align: 'center', width: 60 },
    { prop: 'name', label: '名称', align: 'center', minWidth: 180 },
    { prop: 'type', label: '类型', align: 'center', minWidth: 120, hasSlot: true },
    { prop: 'status', label: '状态', align: 'center', minWidth: 120, hasSlot: true },
    { prop: 'remark', label: '备注', align: 'center', minWidth: 220, showOverflowTooltip: true },
    { prop: 'createTime', label: '创建时间', align: 'center', minWidth: 180 },
    { prop: 'operation', label: '操作', align: 'center', width: 240, fixed: 'right', hasSlot: true },
  ],
}

const loading = ref(false)
const list = ref([])
const pagination = ref({
  current: 1,
  pageSize: 10,
  total: 0,
})
const formRef = ref(null)
const selectParams = ref({
  name: '',
  type: '',
  status: '',
  createTime: [],
})
const dialogRef = ref(null)

const selectList = async () => {
  loading.value = true
  try {
    const res = await List(selectParams.value, pagination.value)
    list.value = res.result.list
    pagination.value = res.result.pagination
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

const handleSelect = () => {
  pagination.value.current = 1
  selectList()
}

const handleReset = () => {
  formRef.value?.resetFields()
  pagination.value.current = 1
  selectList()
}

const handleOpenDialog = (type, id) => {
  dialogRef.value?.init({ type, id })
}

const handleDelete = async (row) => {
  try {
    const res = await Delete(row.id)
    responseHandler(res, '删除成功', () => {
      selectList()
    })
  } catch (error) {
    console.error(error)
  }
}

onMounted(() => {
  selectList()
})
</script>

<template>
  <div class="base-container base-container-search">
    <el-form ref="formRef" :model="selectParams" inline>
      <el-form-item label="名称" prop="name">
        <el-input v-model="selectParams.name" clearable placeholder="请输入名称" style="width: 12rem" />
      </el-form-item>
      <el-form-item label="类型" prop="type">
        <el-select v-model="selectParams.type" clearable filterable placeholder="请选择类型" style="width: 12rem">
          <el-option v-for="item in dict.ENTITY_TYPE" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
      </el-form-item>
      <el-form-item label="状态" prop="status">
        <el-select v-model="selectParams.status" clearable filterable placeholder="请选择状态" style="width: 12rem">
          <el-option v-for="item in dict.COMMON_STATUS" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
      </el-form-item>
      <el-form-item label="创建时间" prop="createTime">
        <el-date-picker
          v-model="selectParams.createTime"
          type="datetimerange"
          value-format="YYYY-MM-DD HH:mm:ss"
          range-separator="-"
          start-placeholder="开始时间"
          end-placeholder="结束时间" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="Search" @click="handleSelect">查询</el-button>
        <el-button icon="Refresh" @click="handleReset">重置</el-button>
      </el-form-item>
    </el-form>
  </div>

  <div class="base-container mt-20">
    <el-button type="success" icon="Plus" @click="handleOpenDialog('insert')">新增</el-button>

    <DynamicTable v-loading="loading" class="mt-20" :list="list" :config="tableConfig">
      <template #type="{ row }">
        <el-tag>{{ dict.label.ENTITY_TYPE[row.type] }}</el-tag>
      </template>
      <template #status="{ row }">
        <el-tag>{{ dict.label.COMMON_STATUS[row.status] }}</el-tag>
      </template>
      <template #operation="{ row }">
        <el-button size="small" @click="handleOpenDialog('detail', row.id)">详情</el-button>
        <el-button type="warning" size="small" @click="handleOpenDialog('update', row.id)">修改</el-button>
        <el-popconfirm title="确认删除?" @confirm="handleDelete(row)">
          <template #reference>
            <el-button type="danger" size="small">删除</el-button>
          </template>
        </el-popconfirm>
      </template>
    </DynamicTable>

    <Pagination v-model:page="pagination.current" v-model:size="pagination.pageSize" class="mt-20" :total="pagination.total" @pagination="selectList" />
  </div>

  <FormDialog ref="dialogRef" @refresh-list="selectList" />
</template>

<style lang="scss" scoped></style>
