<template>
  <div>
    <h1>Task Manager</h1>

    <!-- Task List -->
    <div v-for="task in tasks" :key="task.id" class="task-card">
      <div class="task-content">
        <!-- Checkbox for completion status -->
        <input type="checkbox" :checked="task.completed" @change="toggleTask(task)" />
        <span :class="{ done: task.completed }" @click="toggleTask(task)">
          {{ task.title }}
        </span>
        <!-- Delete button -->
        <button @click="deleteTask(task)" class="delete-button">Delete</button>
      </div>
    </div>

    <!-- Floating Add Task Button -->
    <button @click="openAddTaskModal" class="add-task-button">+</button>

    <!-- Add Task Modal -->
    <div v-if="showAddTaskModal" class="modal">
      <div class="modal-content">
        <input v-model="newTask" type="text" placeholder="Enter new task" />
        <button @click="addTask">Add Task</button>
        <button @click="closeAddTaskModal">Cancel</button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import axios from "axios";

export default {
  setup() {
    const tasks = ref([]);
    const newTask = ref("");
    const showAddTaskModal = ref(false); // To toggle the modal visibility

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

    // Modal functions
    const openAddTaskModal = () => {
      showAddTaskModal.value = true;
    };

    const closeAddTaskModal = () => {
      showAddTaskModal.value = false;
      newTask.value = "";
    };

    onMounted(fetchTasks);

    return { tasks, newTask, addTask, toggleTask, deleteTask, showAddTaskModal,
      openAddTaskModal,
      closeAddTaskModal, };
  },
};
</script>

<style scoped>
/* Task Card Styling */
.task-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 1rem;
}

.task-content {
  display: flex;
  align-items: center;
  width: 100%;
}

.done {
  text-decoration: line-through;
  color: #888;
  cursor: pointer;
}

/* Checkbox styling */
input[type="checkbox"] {
  margin-right: 10px;
}

/* Delete Button Styling */
button {
  padding: 5px 10px;
  background-color: #f44336;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #d32f2f;
}

/* Floating Add Task Button */
.add-task-button {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 50%;
  padding: 15px;
  font-size: 20px;
  cursor: pointer;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
  z-index: 100;
}

.add-task-button:hover {
  background-color: #45a049;
}

/* Modal Styling */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

input {
  padding: 10px;
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
}

/* Mobile responsiveness */
@media (max-width: 600px) {
  .task-card {
    flex-direction: column;
    align-items: flex-start;
    padding: 10px;
  }

  .task-content {
    flex-direction: column;
    align-items: flex-start;
  }

  .task-card button {
    margin-top: 10px;
    width: 100%;
  }
}
</style>
