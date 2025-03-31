import { ref, onMounted } from "vue";
import axios from "axios";

export default {
  setup() {
    const tasks = ref([]);
    const newTask = ref("");

    // Fetch tasks from FastAPI
    const fetchTasks = async () => {
      const response = await axios.get("http://127.0.0.1:8000/tasks");
      tasks.value = response.data;
    };

    // Add a new task
    const addTask = async () => {
      if (!newTask.value.trim()) return;
      const response = await axios.post("http://127.0.0.1:8000/tasks", {
        title: newTask.value,
        completed: false,
      });
      tasks.value.push(response.data);
      newTask.value = "";
    };

    // Toggle task completion
    const toggleTask = async (task) => {
      task.completed = !task.completed;
      await axios.put(`http://127.0.0.1:8000/tasks/${task.id}`, task);
    };

    // Delete a task
    const deleteTask = async (taskId) => {
      await axios.delete(`http://127.0.0.1:8000/tasks/${taskId}`);
      tasks.value = tasks.value.filter(task => task.id !== taskId);
    };

    onMounted(fetchTasks);

    return { tasks, newTask, addTask, toggleTask, deleteTask };
  },
  template: `
    <div>
      <h1>Task Manager</h1>
      <input v-model="newTask" placeholder="New task" />
      <button @click="addTask">Add Task</button>
      <ul>
        <li v-for="task in tasks" :key="task.id">
          <span :class="{ done: task.completed }" @click="toggleTask(task)">
            {{ task.title }}
          </span>
          <button @click="deleteTask(task.id)">Delete</button>
        </li>
      </ul>
    </div>
  `,
};
