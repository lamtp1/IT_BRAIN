<template>
    <div>
      <h1>Task Manager</h1>
      <TaskForm />
      <TaskList />
    </div>
  </template>
  
  <script>
  import TaskForm from '../components/TaskForm.vue';
  import TaskList from '../components/TaskList.vue';
  
  export default {
    components: {
      TaskForm,
      TaskList,
    },
  };
  </script>  