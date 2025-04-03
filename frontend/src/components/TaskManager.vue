<template>
  <div>
    <h1>Task Manager</h1>
    <input v-model="newTask" placeholder="New task" />
    <button @click="addTask">Add Task</button>
    <ul>
      <li v-for="task in tasks" :key="task.id">
        <span :class="{ done: task.completed }" @click="toggleTask(task)">
          {{ task.title }}
        </span>
        <button @click="deleteTask(task)">Delete</button>
      </li>
    </ul>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import axios from "axios";

export default {
  setup() {
    const tasks = ref([]);
    const newTask = ref("");

    // Fetch tasks from FastAPI (now with authentication)
    const fetchTasks = async () => {
      const token = localStorage.getItem("token");
      if (!token) {
        alert("Not authenticated! Redirecting to login.");
        window.location.href = "/"; // Redirect to login
        return;
      }

      try {
        const response = await axios.get("http://127.0.0.1:8000/tasks/",
        {
          headers: { Authorization: `Bearer ${token}` }, // Pass token
        });
        tasks.value = response.data;
      } catch (error) {
        console.error("Error fetching tasks:", error);
      }
    };

    // Add a new task
    const addTask = async () => {
      if (!newTask.value.trim()) return;

      const token = localStorage.getItem("token");
      if (!token) return;

      try {
        const response = await axios.post("http://127.0.0.1:8000/tasks/", {
          title: newTask.value,
          completed: false,
        },
        { headers: { Authorization: `Bearer ${token}` } } // Pass token
      );
        tasks.value.push(response.data);
        console.log("Added task:", response.data);
        newTask.value = "";
      } catch (error) {
        console.error("Error adding task:", error);
      }
    };

    // Toggle task completion
    const toggleTask = async (task) => {
      console.log("Toggling task with ID:", task.id);	
      task.completed = !task.completed;

      const token = localStorage.getItem("token");
      if (!token) return;

      try {
        await axios.put(`http://127.0.0.1:8000/tasks/${task.id}`, task,
        { headers: { Authorization: `Bearer ${token}` } } // Pass token
        );
      } catch (error) {
        console.error("Error updating task:", error);
      }
    };

    // Delete a task
    const deleteTask = async (task) => {
      console.log("Deleting task with ID:", task.id);
      if (!task.id) {
        console.error("Invalid task ID");
        return;
      }
      const token = localStorage.getItem("token");
      if (!token) return;

      try {
        await axios.delete(`http://127.0.0.1:8000/tasks/${task.id}`,
          { headers: { Authorization: `Bearer ${token}` } } // Pass token
        );
        tasks.value = tasks.value.filter((t) => t.id !== task.id);
      } catch (error) {
        console.error("Error deleting task:", error);
      }
    };

    onMounted(fetchTasks);

    return { tasks, newTask, addTask, toggleTask, deleteTask };
  },
};
</script>

<style scoped>
/* Add your styles here */
.done {
  text-decoration: line-through;
  cursor: pointer;
}
</style>
