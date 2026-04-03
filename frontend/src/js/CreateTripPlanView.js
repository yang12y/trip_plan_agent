import { ref } from 'vue';
import { useRouter } from 'vue-router';

export default {
  name: 'CreateTripPlanView',
  setup() {
    const router = useRouter();
    const isLoading = ref(false);
    const error = ref('');
    const success = ref(false);

    const formData = ref({
      userId: '',
      message: '',
      budget: 0,
      currency: 'CNY'
    });

    async function createTripPlan() {
      isLoading.value = true;
      error.value = '';
      success.value = false;
      
      try {
        const response = await fetch('/api/trip-plan/create', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(formData.value)
        });
        
        if (!response.ok) {
          throw new Error('创建旅行计划失败');
        }
        
        const data = await response.json();
        if (data.state === 'success') {
          success.value = true;
        } else {
          error.value = data.message || '创建旅行计划失败';
        }
      } catch (err) {
        error.value = err instanceof Error ? err.message : '创建旅行计划失败';
      } finally {
        isLoading.value = false;
      }
    }

    return {
      isLoading,
      error,
      success,
      formData,
      createTripPlan
    };
  }
}