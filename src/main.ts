import { createApp } from 'vue'
import App from './App.vue'
import { createRouter, createWebHistory } from 'vue-router'
import Toaster from "@meforma/vue-toaster";
import { setupLayouts } from 'virtual:generated-layouts'
import generatedRoutes from 'virtual:generated-pages'
import 'virtual:windi.css';
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.min.js'
import './styles/layout-pages.css';
import './styles/components.css';

const routes = setupLayouts(generatedRoutes)

const router = createRouter({
    history: createWebHistory(),
    routes,
});

const app = createApp(App)
    app.use(router)
    .use(Toaster, {
        position: "bottom-right",
      })
    .provide('toast', app.config.globalProperties.$toast)
    .mount('#app')
