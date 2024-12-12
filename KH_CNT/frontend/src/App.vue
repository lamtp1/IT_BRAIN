<template>
    <div id="app">
      <h1>Task Manager</h1>
      <TaskForm @task-created="fetchTasks" />
      <TaskList :tasks="tasks" />
    </div>
  </template>
  
  <script>
  import TaskList from "./components/TaskList.vue";
  import TaskForm from "./components/TaskForm.vue";
  import axios from "axios";
  
  export default {
    components: { TaskList, TaskForm },
    data() {
      return {
        tasks: [],
      };
    },
    methods: {
      fetchTasks() {
        axios.get("http://localhost:3000/tasks").then((res) => {
          this.tasks = res.data;
        });
      },
    },
    mounted() {
      this.fetchTasks();
    },
  };
  </script>
  