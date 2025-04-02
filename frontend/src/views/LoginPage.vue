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
  export default {
    data() {
      return {
        username: '',
        password: '',
      };
    },
    methods: {
      login() {
        // Call API to validate user credentials (this is a simple example)
        // You should replace it with a real API call.
        if (this.username === 'test' && this.password === 'password') {
          // Set user in localStorage for session persistence
          localStorage.setItem('user', this.username);
          // Redirect to the task page
          this.$router.push('/tasks');
        } else {
          alert('Invalid username or password');
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
  