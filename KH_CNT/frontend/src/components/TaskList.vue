<template>
    <ul>
      <li v-for="task in tasks" :key="task.id">
        {{ task.title }} - {{ task.description }}
      </li>
    </ul>
  </template>
  
  <script>
  export default {
    props: ["tasks"],
  };
  </script>
  