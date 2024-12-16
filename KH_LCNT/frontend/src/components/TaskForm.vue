<template>
    <div>
      <h2>Create Task</h2>
      <form @submit.prevent="createTask">
        <div>
          <label>Title:</label>
          <input type="text" v-model="task.title" required />
        </div>
        <div>
          <label>Assignee:</label>
          <input type="text" v-model="task.assignee" required />
        </div>
        <div>
          <label>Deadline:</label>
          <input type="date" v-model="task.deadline" required />
        </div>
        <button type="submit">Add Task</button>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        task: {
          title: '',
          assignee: '',
          deadline: '',
        },
      };
    },
    methods: {
      createTask() {
        fetch('http://localhost:3000/tasks', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(this.task),
        })
          .then((response) => response.json())
          .then(() => {
            alert('Task added successfully!');
            this.task = { title: '', assignee: '', deadline: '' };
          });
      },
    },
  };
  </script>  