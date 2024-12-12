<template>
    <form @submit.prevent="submitForm">
      <input v-model="title" placeholder="Task Title" required />
      <textarea v-model="description" placeholder="Task Description"></textarea>
      <button type="submit">Add Task</button>
    </form>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    data() {
      return {
        title: "",
        description: "",
      };
    },
    methods: {
      submitForm() {
        axios
          .post("http://localhost:3000/tasks", {
            title: this.title,
            description: this.description,
          })
          .then(() => {
            this.$emit("task-created");
            this.title = "";
            this.description = "";
          });
      },
    },
  };
  </script>
  