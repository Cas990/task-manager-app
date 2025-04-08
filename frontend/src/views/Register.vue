<template>
    <div class="register">
      <h1>Register</h1>
      <form @submit.prevent="register">
        <label for="username">Username</label>
        <input type="text" id="username" v-model="username" required />
  
        <label for="password">Password</label>
        <input type="password" id="password" v-model="password" required />
  
        <label for="confirmPassword">Confirm Password</label>
        <input type="password" id="confirmPassword" v-model="confirmPassword" required />
  
        <button type="submit">Register</button>
      </form>
      <p>Already have an account? <router-link to="login">Login here</router-link></p>
    </div>
</template>
  
<script>
  import axios from "axios";
  
  export default {
    data() {
      return {
        username: "",
        password: "",
        confirmPassword: ""
      };
    },
    methods: {
      async register() {
        if (this.password !== this.confirmPassword) {
          alert("Passwords do not match!");
          return;
        }
  
        try {
          await axios.post("http://127.0.0.1:8000/register/", {
            username: this.username,
            password: this.password
          });
          alert("Registration successful! You can now log in.");
          this.$router.push("/login");
        } catch (error) {
          console.error("Error registering:", error);
          alert("Registration failed. Try a different username.");
        }
      }
    }
  };
</script>
  
<style scoped>
.register {
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
  