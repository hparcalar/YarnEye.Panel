<script setup lang="ts">
import { reactive, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router';
import checkAuthRoute from '../handlers/auth.filter';

const logout = () => {
    localStorage.removeItem('hyarn_user');
    router.push({ name: 'login' });
}

const router = useRouter();
onMounted(() => {
  checkAuthRoute(router, 'panel')
});

</script>
<template>
     <div>
        <div class="w-full flex flex-wrap mx-0" id="topBar">
          <router-link
                class="w-150 flex-1"
                style="text-decoration:none;"
                to="/panel"
                v-slot="{href, route, navigate}"
                >
              <h5 :href="href" @click="navigate" class=" text-white text-left flex flex-wrap px-3 py-3">
                <img src="/heka.png" class="h-10">
                <span style="padding-top:10px;" class="mx-4 text-shadow-sm text-black">Yarn EYE</span>
              </h5>
           </router-link>
           <div class="py-3 px-3">
               <button type="button" class="bg-white rounded-1 text-black px-4" style="margin-top:10px;" @click="logout">
                   Çıkış Yap
               </button>
           </div>
       </div>
         <main>
            <router-view />
         </main>
     </div>
</template>

<style lang="postcss" scoped>

#topBar{
  background: rgb(207,231,250); /* Old browsers */
  background: -moz-linear-gradient(top,  rgba(207,231,250,1) 0%, rgba(99,147,193,1) 100%); /* FF3.6-15 */
  background: -webkit-linear-gradient(top,  rgba(207,231,250,1) 0%,rgba(99,147,193,1) 100%); /* Chrome10-25,Safari5.1-6 */
  background: linear-gradient(to bottom,  rgba(207,231,250,1) 0%,rgba(99,147,193,1) 100%); /* W3C, IE10+, FF16+, Chrome26+, Opera12+, Safari7+ */
  filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#cfe7fa', endColorstr='#6393c1',GradientType=0 ); /* IE6-9 */
}
.main-collapsed{
  padding-left:290px;
}
.main{
  padding-left: 65px;
}
</style>