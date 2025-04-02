import { createApp } from 'vue';
import App from './App.vue';  // Import your main Vue component
import router from './router';
import './style.css';

createApp(App).use(router).mount('#app');
