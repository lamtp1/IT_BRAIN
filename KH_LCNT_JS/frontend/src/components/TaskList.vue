<template>
    <div>
      <h2>Task List</h2>
      <ul>
        <li v-for="task in tasks" :key="task.id">
          {{ task.title }} - {{ task.assignee }} ({{ task.deadline }})
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        tasks: [],
      };
    },
    mounted() {
      fetch('http://localhost:3000/tasks')
        .then((response) => response.json())
        .then((data) => {
          this.tasks = data;
        });
    },
  };
  </script>  