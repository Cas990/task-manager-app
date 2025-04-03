<template>
    <div class="login">
      <h1>Login</h1>
      <form @submit.prevent="login">
        <label for="username">Username</label>
        <input type="text" id="username" v-model="username" required />
  
        <label for="password">Password</label>
        <input type="password" id="password" v-model="password" required />
  
        <button type="submit">Login</button>
      </form>
    </div>
  </template>
  
  <script>
  import axios from "axios"; 

  export default {
    data() {
      return {
        username: '',
        password: '',
      };
    },
    methods: {
      async login() {
        // Perform login logic here
        try {
          const response = await axios.post("http://127.0.0.1:8000/token/", new URLSearchParams({
              username: this.username,
              password: this.password,
            }),
            {headers: { "Content-Type": "application/x-www-form-urlencoded"} }
          );

          localStorage.setItem("token", response.data.access_token);
          this.$router.push("/tasks");          
        } catch (error) {
          console.error("Error logging in:", error);
          alert("Invalid credentials");
        }
      },   
    },     
  };
  </script>
  
  <style scoped>
  /* Add some basic styling for the login form */
  .login {
    display: flex;
    flex-direction: column;
    width: 300px;
    margin: 0 auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 10px;
  }
  
  label {
    margin-bottom: 5px;
  }
  
  input {
    margin-bottom: 15px;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
  
  button {
    padding: 10px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #45a049;
  }
  </style>
  