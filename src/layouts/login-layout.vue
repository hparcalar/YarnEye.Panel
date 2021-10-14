<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, reactive } from 'vue';
import { useRouter } from 'vue-router';

</script>
<template>
    <main class="h-full bg-gray-100 py-4">
        <router-view />
    </main>
</template>

    