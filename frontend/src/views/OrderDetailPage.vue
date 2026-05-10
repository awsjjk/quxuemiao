<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-white nav-shadow px-6 py-3 flex justify-between items-center">
      <span class="text-xl font-bold text-primary flex items-center"><i class="fa fa-paw mr-2"></i>趣学喵</span>
      <button @click="$router.push('/dashboard')" class="text-sm border border-gray-300 rounded-lg px-4 py-2 hover:bg-gray-50 transition-colors"><i class="fa fa-arrow-left mr-1"></i>返回</button>
    </nav>
    <div class="max-w-2xl mx-auto py-8 px-4">

      <!-- 订单列表视图 -->
      <div v-if="route.params.id === '0'">
        <h2 class="text-xl font-bold text-gray-800 mb-4"><i class="fa fa-list-alt text-primary mr-2"></i>我的订单</h2>
        <p v-if="!orders.length" class="text-center py-20 text-gray-400"><i class="fa fa-inbox text-5xl mb-3 block"></i>暂无订单</p>
        <OrderCard v-for="o in orders" :key="o.id" :order="o" @click="$router.push(`/order/${o.id}`)" />
      </div>

      <!-- 订单详情视图 -->
      <div v-else>
        <h2 class="text-xl font-bold text-gray-800 mb-4"><i class="fa fa-file-text text-primary mr-2"></i>订单详情</h2>

        <p v-if="loading" class="text-center py-12 text-gray-400">加载中...</p>

        <template v-if="!loading && order">
          <!-- 订单信息 -->
          <div class="bg-white rounded-xl card-shadow p-6 mb-4">
            <div class="flex justify-between py-3 border-b border-gray-100 text-sm">
              <span class="text-gray-500">订单编号</span><span class="text-gray-700">#{{ order.id }}</span>
            </div>
            <div class="flex justify-between py-3 border-b border-gray-100 text-sm">
              <span class="text-gray-500">订单状态</span>
              <span :class="statusClass">{{ statusText }}</span>
            </div>
            <div class="flex justify-between py-3 border-b border-gray-100 text-sm">
              <span class="text-gray-500">需求标题</span><span class="text-gray-700">{{ order.demand_title || '--' }}</span>
            </div>
            <div class="flex justify-between py-3 border-b border-gray-100 text-sm">
              <span class="text-gray-500">家教姓名</span><span class="text-gray-700">{{ order.tutor_name || '--' }}</span>
            </div>
            <div class="flex justify-between py-3 border-b border-gray-100 text-sm">
              <span class="text-gray-500">家教学校</span><span class="text-gray-700">{{ order.tutor_school || '--' }}</span>
            </div>
            <div class="flex justify-between py-3 border-b border-gray-100 text-sm">
              <span class="text-gray-500">联系电话</span><span class="text-gray-700">{{ order.tutor_phone || '--' }}</span>
            </div>
            <div class="flex justify-between py-3 border-b border-gray-100 text-sm">
              <span class="text-gray-500">订单金额</span><span class="text-gray-700 font-semibold">¥{{ order.total_amount }}</span>
            </div>
            <div class="flex justify-between py-3 border-b border-gray-100 text-sm">
              <span class="text-gray-500">备注</span><span class="text-gray-700">{{ order.remark || '--' }}</span>
            </div>
            <div class="flex justify-between py-3 text-sm">
              <span class="text-gray-500">创建时间</span><span class="text-gray-700">{{ order.create_time?.slice(0, 10) }}</span>
            </div>
          </div>

          <!-- 操作按钮 -->
          <div v-if="order.status === 2" class="mb-4">
            <button @click="finishOrder" :disabled="saving" class="bg-green-600 hover:bg-green-700 text-white font-medium px-6 py-3 rounded-lg transition-colors disabled:opacity-60">
              <i class="fa fa-check-circle mr-2"></i>{{ saving ? '处理中...' : '确认完成' }}
            </button>
          </div>

          <!-- 评价 -->
          <div v-if="order.status === 3" class="mb-4">
            <RatingForm :order-id="order.id" @submitted="rated = true" />
            <p v-if="rated" class="text-green-600 text-sm text-center mt-2">✅ 评价已提交</p>
          </div>

          <!-- 课程记录 -->
          <div class="mt-6">
            <div class="flex justify-between items-center mb-3">
              <h3 class="font-semibold text-gray-800"><i class="fa fa-calendar text-primary mr-2"></i>课程记录</h3>
              <button @click="showCourseForm = !showCourseForm" class="text-sm bg-primary hover:bg-secondary text-white px-3 py-1.5 rounded-lg transition-colors">
                <i :class="showCourseForm ? 'fa fa-minus' : 'fa fa-plus'" class="mr-1"></i>{{ showCourseForm ? '收起' : '添加课程' }}
              </button>
            </div>

            <div v-if="showCourseForm" class="bg-white rounded-xl card-shadow p-4 mb-4 fade-in">
              <form @submit.prevent="createCourse" class="grid grid-cols-3 gap-3">
                <input v-model="courseForm.course_date" type="date" required class="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition-all" />
                <input v-model="courseForm.start_time" type="time" class="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition-all" />
                <input v-model="courseForm.end_time" type="time" class="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition-all" />
                <input v-model.number="courseForm.actual_duration" type="number" placeholder="实际时长(分钟)" class="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition-all" />
                <input v-model="courseForm.knowledge_points" placeholder="知识点（逗号分隔）" class="col-span-2 px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none transition-all" />
                <textarea v-model="courseForm.content" placeholder="课程内容" rows="2" class="col-span-3 px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none resize-none transition-all"></textarea>
                <textarea v-model="courseForm.homework" placeholder="课后作业" rows="2" class="col-span-3 px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none resize-none transition-all"></textarea>
                <textarea v-model="courseForm.tutor_feedback" placeholder="家教反馈" rows="2" class="col-span-3 px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none resize-none transition-all"></textarea>
                <button type="submit" :disabled="courseSaving" class="col-span-3 bg-primary hover:bg-secondary text-white font-medium py-2 rounded-lg transition-colors disabled:opacity-60">
                  <i class="fa fa-save mr-2"></i>{{ courseSaving ? '保存中...' : '保存课程记录' }}
                </button>
              </form>
            </div>

            <div v-if="courses.length" class="space-y-2">
              <div v-for="c in courses" :key="c.id" class="bg-white rounded-lg p-4 border border-gray-100">
                <div class="flex justify-between items-start mb-2">
                  <span class="font-semibold text-gray-800">{{ c.course_date }} {{ c.start_time }}-{{ c.end_time }}</span>
                  <span class="text-xs px-2 py-0.5 rounded-full" :class="c.status === 2 ? 'bg-green-50 text-green-600' : 'bg-yellow-50 text-yellow-600'">{{ c.status === 2 ? '已确认' : '待确认' }}</span>
                </div>
                <div class="text-sm text-gray-600 space-y-1">
                  <p v-if="c.content"><span class="text-gray-400">内容:</span> {{ c.content }}</p>
                  <p v-if="c.homework"><span class="text-gray-400">作业:</span> {{ c.homework }}</p>
                  <p v-if="c.tutor_feedback"><span class="text-gray-400">反馈:</span> {{ c.tutor_feedback }}</p>
                  <p v-if="c.knowledge_points?.length"><span class="text-gray-400">知识点:</span> {{ c.knowledge_points.join(', ') }}</p>
                </div>
              </div>
            </div>
          </div>
        </template>

        <p v-if="!loading && !order" class="text-center py-20 text-gray-400">订单不存在</p>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { orderAPI, courseAPI } from '../api'
import OrderCard from '../components/OrderCard.vue'
import RatingForm from '../components/RatingForm.vue'
const route = useRoute()
const orders = ref([]); const order = ref(null); const loading = ref(false); const saving = ref(false); const rated = ref(false)
const courses = ref([]); const showCourseForm = ref(false); const courseSaving = ref(false)
const courseForm = ref({ course_date: '', start_time: '', end_time: '', actual_duration: null, content: '', homework: '', knowledge_points: '', tutor_feedback: '', student_performance: '', parent_feedback: '' })
const statusText = computed(() => ({ 1: '待支付', 2: '进行中', 3: '已完成', 4: '已取消' }[order.value?.status] || '--'))
const statusClass = computed(() => {
  const s = order.value?.status
  return s === 1 ? 'text-yellow-600 font-medium' : s === 2 ? 'text-blue-600 font-medium' : s === 3 ? 'text-green-600 font-medium' : 'text-gray-700'
})

async function loadData(id) {
  if (id === '0') {
    const res = await orderAPI.list(); orders.value = res.data || []
  } else {
    loading.value = true; order.value = null; courses.value = []; rated.value = false
    try { const res = await orderAPI.detail(Number(id)); order.value = res.code === 200 ? res.data : null; if (res.code === 200) await fetchCourses() } catch (e) { order.value = null } finally { loading.value = false }
  }
}
onMounted(() => loadData(route.params.id))
watch(() => route.params.id, (newId) => { if (newId) loadData(newId) })
async function fetchCourses() { try { const res = await courseAPI.list(Number(route.params.id)); courses.value = res.data } catch (e) {} }
async function finishOrder() { saving.value = true; try { await orderAPI.updateStatus(order.value.id, 3); order.value.status = 3 } catch (e) { alert(e.response?.data?.msg || '操作失败') } finally { saving.value = false } }
async function createCourse() {
  courseSaving.value = true
  try {
    await courseAPI.create({
      order_id: order.value.id,
      ...courseForm.value,
      knowledge_points: courseForm.value.knowledge_points.split(',').map(s => s.trim()).filter(Boolean)
    })
    courseForm.value = { course_date: '', start_time: '', end_time: '', actual_duration: null, content: '', homework: '', knowledge_points: '', tutor_feedback: '', student_performance: '', parent_feedback: '' }
    showCourseForm.value = false; fetchCourses()
  } catch (e) { alert(e.response?.data?.msg || '创建失败') }
  finally { courseSaving.value = false }
}
</script>
