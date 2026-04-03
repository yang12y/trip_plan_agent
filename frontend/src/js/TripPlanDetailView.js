import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';

export default {
  name: 'TripPlanDetailView',
  setup() {
    const route = useRoute();
    const isLoading = ref(true);
    const error = ref('');
    const tripPlan = ref(null);

    function formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString('zh-CN');
    }

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
        } else {
          error.value = data.message || '获取旅行计划失败';
        }
      } catch (err) {
        error.value = err instanceof Error ? err.message : '获取旅行计划失败';
      } finally {
        isLoading.value = false;
      }
    }

    onMounted(() => {
      fetchTripPlan();
    });

    return {
      isLoading,
      error,
      tripPlan,
      formatDate,
      fetchTripPlan
    };
  }
}