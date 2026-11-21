<template>
  <div class="users-view">
    <div class="page-header">
      <h1>Користувачі</h1>
    </div>
    <div class="coming-soon">
      <svg class="icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M17 21V19C17 18.4696 16.7893 17.9609 16.4142 17.5858C16.0391 17.2107 15.5304 17 15 17H9C8.46957 17 7.96086 17.2107 7.58579 17.5858C7.21071 17.9609 7 18.4696 7 19V21M9 11C10.6569 11 12 9.65685 12 8C12 6.34315 10.6569 5 9 5C7.34315 5 6 6.34315 6 8C6 9.65685 7.34315 11 9 11ZM14 7C15.6569 7 17 5.65685 17 4C17 2.34315 15.6569 1 14 1C12.3431 1 11 2.34315 11 4C11 5.65685 12.3431 7 14 7ZM20 19V21M20 17C19.4696 17 18.9609 17.2107 18.5858 17.5858C18.2107 17.9609 18 18.4696 18 19V21M14 11C15.6569 11 17 12.3431 17 14C17 14.5304 16.7893 15.0391 16.4142 15.4142C16.0391 15.7893 15.5304 16 15 16H9C8.46957 16 7.96086 15.7893 7.58579 15.4142C7.21071 15.0391 7 14.5304 7 14C7 12.3431 8.34315 11 10 11H14Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      <h2>Управління користувачами</h2>
      <p>Ця функція зараз у розробці. Незабаром тут з'явиться можливість керувати користувачами системи.</p>
    </div>
  </div>
</template>

<script setup lang="ts">
</script>

<style scoped>
.users-view {
  max-width: 800px;
}

.page-header {
  margin-bottom: 2rem;
}

.page-header h1 {
  margin: 0;
  font-size: 1.5rem;
  color: #0f172a;
}

.coming-soon {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  background-color: #ffffff;
  border-radius: 0.75rem;
  border: 1px solid #e2e8f0;
  text-align: center;
}

.icon {
  width: 64px;
  height: 64px;
  color: #94a3b8;
  margin-bottom: 1.5rem;
}

.coming-soon h2 {
  margin: 0 0 0.5rem;
  font-size: 1.25rem;
  color: #0f172a;
}

.coming-soon p {
  margin: 0;
  color: #64748b;
  max-width: 400px;
}
</style>
