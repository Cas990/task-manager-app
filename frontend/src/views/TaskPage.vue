<template>
  <div class="task-page">
    <h1>Welcome, <span class="username">{{ username }}</span>!</h1>
    <!-- Logout button -->
    <button @click="logout" class="logout-button">Logout</button>
    <!-- Display user tasks here -->
    <TaskManager />
  </div>
</template>

<script>
import TaskManager from "../components/TaskManager.vue";
export default {
  components: {
    TaskManager,
  },
  data() {
    return {
      username: "", // Initialize username
    };
  },
/*************  ✨ Codeium Command ⭐  *************/
    /**
     * Lifecycle hook: fetch the logged-in username from localStorage when the component is created.
     * @function created
     */
/******  a26dcaf0-11eb-4447-8073-0b059ae96c78  *******/  created() {
    // Fetch the logged-in username from localStorage
    this.username = localStorage.getItem("user") || "";
  },
  methods: {
    /**
     * Logs out the user by removing the username from localStorage and redirecting to the login page.
     */
    logout() {
      localStorage.removeItem("user");
      this.username = null;
      this.$router.push("/");
    },
  },
};
</script>

<style scoped>
.task-page {
  padding: 30px;
  text-align: center;
  max-width: 1000px;
  margin: 0 auto;
  background-color: #fff; /* Set a white background for the task page */
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

h1 {
  font-size: 2.5em;
  color: #333;
  margin-bottom: 20px;
}

.username {
  color: #4caf50; /* Highlight the username in green */
  font-weight: bold;
}

.logout-button {
  padding: 12px 20px;
  background-color: #f44336;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1.1em;
  margin-top: 20px;
  transition: background-color 0.3s ease;
}

.logout-button:hover {
  background-color: #d32f2f;
}

/* Make the layout mobile-friendly */
@media (max-width: 600px) {
  .task-page {
    padding: 20px;
  }

  h1 {
    font-size: 2em;
  }

  .logout-button {
    width: 100%;
  }
}
</style>
