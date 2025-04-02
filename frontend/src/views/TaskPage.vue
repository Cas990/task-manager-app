<template>
    <div class="task-page">
        <h1>Welcome, {{ username }}!</h1>
        <p>Here are your tasks:</p>
        <!-- Display user tasks here -->

        <!-- Logout button -->
        <button @click="logout">Logout</button>
    </div>
</template>
  
<script>
  export default {
    data() {
      return {
        username: '',
      };
    },
    created() {
      // Get the logged-in user's username from localStorage
      this.username = localStorage.getItem('user');
    },
    methods: {
        logout() {
            localStorage.removeItem('user');
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
  