<template>
    <div class="task-page">
        <h1>Welcome, {{ username }}!</h1>
        <!-- Logout button -->
        <button @click="logout">Logout</button>
        <!-- Display user tasks here -->
        <TaskManager /> 
    </div>
</template>
  
<script>
  import TaskManager from '../components/TaskManager.vue';
  export default {
    components: {
      TaskManager
    },
    data() {
      return {
        username: '', // Initialize username
      };
    },
    created() {
      // Fetch the logged-in username from localStorage
      this.username = localStorage.getItem('user') || '';
    },
    methods: {
        logout() {
            localStorage.removeItem('user');
            this.username = null;
            this.password = null;
            this.$router.push('/');
        },
    },

  };
</script>
  
<style scoped>
.task-page {
    padding: 20px;
    text-align: center;
}

button {
    padding: 10px;
    background-color: #f44336;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

button:hover {
    background-color: #d32f2f;
}
  </style>
  