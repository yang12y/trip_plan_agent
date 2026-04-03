import { ref, onMounted } from 'vue';
import { RouterLink, RouterView } from 'vue-router';

export default {
  name: 'App',
  components: {
    RouterLink,
    RouterView
  },
  setup() {
    const weatherData = ref(null);
    const isLoadingWeather = ref(false);
    const weatherError = ref('');

    async function fetchWeather() {
      isLoadingWeather.value = true;
      weatherError.value = '';
      
      try {
        const response = await fetch('/api/weather/get', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ user_id: 'user1' })
        });
        
        if (!response.ok) {
          throw new Error('获取天气信息失败');
        }
        
        const data = await response.json();
        // 后端返回的数据格式是 { daily_weather_data: { daily_weather_data: { ... } } }
        // 我们需要访问嵌套的 daily_weather_data
        weatherData.value = data.daily_weather_data.daily_weather_data;
      } catch (err) {
        weatherError.value = err instanceof Error ? err.message : '获取天气信息失败';
      } finally {
        isLoadingWeather.value = false;
      }
    }

    onMounted(() => {
      fetchWeather();
    });

    function getWeatherIcon(weather) {
      const weatherIcons = {
        '晴': '☀️',
        '多云': '⛅',
        '阴': '☁️',
        '小雨': '🌧️',
        '中雨': '🌧️',
        '大雨': '⛈️',
        '雷阵雨': '⛈️',
        '小雪': '❄️',
        '中雪': '❄️',
        '大雪': '❄️',
        '雾': '🌫️',
        '霾': '🌫️'
      };
      return weatherIcons[weather] || '🌤️';
    }

    return {
      weatherData,
      isLoadingWeather,
      weatherError,
      fetchWeather,
      getWeatherIcon
    };
  }
}
