import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';

export default {
  name: 'UpdateTripPlanView',
  setup() {
    const route = useRoute();
    const router = useRouter();
    const isLoading = ref(true);
    const isUpdating = ref(false);
    const error = ref('');
    const updateSuccess = ref(false);
    const tripPlan = ref(null);
    const formData = ref({});

    async function fetchTripPlan() {
      const userId = route.params.userId;
      isLoading.value = true;
      error.value = '';
      
      try {
        const response = await fetch(`/api/trip-plan/status/${userId}`);
        
        if (!response.ok) {
          throw new Error('获取旅行计划失败');
        }
        
        const data = await response.json();
        if (data.state === 'success') {
          tripPlan.value = data.data;
          // 初始化表单数据
          formData.value = {
            ...data.data,
            interests: data.data.interests.join(', ')
          };
        } else {
          error.value = data.message || '获取旅行计划失败';
        }
      } catch (err) {
        error.value = err instanceof Error ? err.message : '获取旅行计划失败';
      } finally {
        isLoading.value = false;
      }
    }

    async function updateTripPlan() {
      isUpdating.value = true;
      error.value = '';
      updateSuccess.value = false;
      
      try {
        // 处理兴趣偏好数组
        if (typeof formData.value.interests === 'string') {
          formData.value.interests = formData.value.interests.split(',').map((item) => item.trim());
        }
        
        const response = await fetch('/api/update-trip/update', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ state: formData.value })
        });
        
        if (!response.ok) {
          throw new Error('更新旅行计划失败');
        }
        
        const data = await response.json();
        if (data.state === 'success') {
          updateSuccess.value = true;
        } else {
          error.value = data.message || '更新旅行计划失败';
        }
      } catch (err) {
        error.value = err instanceof Error ? err.message : '更新旅行计划失败';
      } finally {
        isUpdating.value = false;
      }
    }

    onMounted(() => {
      fetchTripPlan();
    });

    return {
      isLoading,
      isUpdating,
      error,
      updateSuccess,
      tripPlan,
      formData,
      fetchTripPlan,
      updateTripPlan
    };
  }
}