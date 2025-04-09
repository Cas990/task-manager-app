<template>
  <div class="task-manager">
    <h2>Manage Your Tasks</h2>
    <input v-model="newTask" placeholder="New task" />
    <button @click="addTask">Add Task</button>
    <ul>
      <li
        v-for="task in tasks"
        :key="task.id"
        :class="{'completed': task.completed}"
        @click="toggleTask(task)"
      >
        <span class="task-title">{{ task.title }}</span>
        <span v-if="task.completed" class="checkmark">✔</span>
        <button @click="deleteTask(task)" class="delete-button">Delete</button>
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

    // Fetch tasks from FastAPI
    const fetchTasks = async () => {
      const token = localStorage.getItem("token");
      if (!token) {
        alert("Not authenticated! Redirecting to login.");
        window.location.href = "/"; // Redirect to login page
        return;
      }

      try {
        const response = await axios.get("http://127.0.0.1:8000/tasks/", {
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
        const response = await axios.post(
          "http://127.0.0.1:8000/tasks/",
          {
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
        await axios.put(
          `http://127.0.0.1:8000/tasks/${task.id}`,
          task,
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
        await axios.delete(`http://127.0.0.1:8000/tasks/${task.id}`, {
          headers: { Authorization: `Bearer ${token}` }, // Pass token
        });
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
.task-manager {
  background-color: #fff;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  max-width: 600px;
  margin: 20px auto;
}

h2 {
  font-size: 2em;
  color: #333;
  margin-bottom: 10px;
}

input {
  padding: 10px;
  width: 100%;
  margin-bottom: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

button {
  padding: 10px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 10px;
}

button:hover {
  background-color: #45a049;
}

ul {
  list-style: none;
  padding: 0;
}

li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: black;
  background-color: #f9f9f9;
  padding: 10px;
  border-radius: 5px;
  margin-bottom: 10px;
  transition: background-color 0.3s ease;
}

li.completed {
  background-color: #4caf50; 
  color: white;
}

li .task-title {
  flex: 1;
}

li .checkmark {
  color: #fff;
  font-size: 1.5em;
  margin-left: 10px;
  font-weight: bold;
}

li button.delete-button {
  background-color: #f44336;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 5px;
  cursor: pointer;
}

li button.delete-button:hover {
  background-color: #d32f2f;
}
</style>
