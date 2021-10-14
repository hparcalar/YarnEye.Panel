<script setup lang="ts">
    import { computed, ref, onMounted } from 'vue';
    
    onMounted(() => {
        
    });
    
</script>
<template>
<div class="container-fluid flex flex-col h-full px-0">
    <div class="row my-2 px-2">
       <div class="col-md-4">
           <router-link
                to="/lines"
                v-slot="{href, route, navigate}"
                >
           <button type="button" :href="href" @click="navigate" id="btnProdLine" class="btn-secondary btn-block w-full h-150px">
               ÜRETİM HATLARI
           </button>
           </router-link>
       </div>

       <div class="col-md-4">
           <button type="button" id="btnSampleAssignment" class="btn-secondary btn-block w-full h-150px">
               ÖRNEKLEM ATAMA
           </button>
       </div>

       <div class="col-md-4">
           <button type="button" id="btnReports" class="btn-secondary btn-block w-full h-150px">
               RAPOR
           </button>
       </div>
    </div>
</div>
    
</template>
<style lang="postcss" scoped>
    .row button{
        font-weight: bold;
    }

    #btnProdLine {
        box-shadow:inset 0px 1px 0px 0px #bee2f9;
        background:linear-gradient(to bottom, #63b8ee 5%, #468ccf 100%);
        background-color:#63b8ee;
        border-radius:6px;
        border:1px solid #3866a3;
        display:inline-block;
        cursor:pointer;
        color:#14396a;
        font-family:Arial;
        font-size:15px;
        font-weight:bold;
        padding:6px 24px;
        text-decoration:none;
        text-shadow:0px 1px 0px #7cacde;
    }
    #btnProdLine:hover {
        background:linear-gradient(to bottom, #468ccf 5%, #63b8ee 100%);
        background-color:#468ccf;
    }
    #btnProdLine:active {
        position:relative;
        top:1px;
    }

    #btnReports {
        box-shadow:inset 0px 1px 0px 0px #ffffff;
        background:linear-gradient(to bottom, #f9f9f9 5%, #e9e9e9 100%);
        background-color:#f9f9f9;
        border-radius:6px;
        border:1px solid #dcdcdc;
        display:inline-block;
        cursor:pointer;
        color:#666666;
        font-family:Arial;
        font-size:15px;
        font-weight:bold;
        padding:6px 24px;
        text-decoration:none;
        text-shadow:0px 1px 0px #ffffff;
    }
    #btnReports:hover {
        background:linear-gradient(to bottom, #e9e9e9 5%, #f9f9f9 100%);
        background-color:#e9e9e9;
    }
    #btnReports:active {
        position:relative;
        top:1px;
    }

    #btnSampleAssignment {
        box-shadow:inset 0px 1px 0px 0px #caefab;
        background:linear-gradient(to bottom, #77d42a 5%, #5cb811 100%);
        background-color:#77d42a;
        border-radius:6px;
        border:1px solid #268a16;
        display:inline-block;
        cursor:pointer;
        color:#306108;
        font-family:Arial;
        font-size:15px;
        font-weight:bold;
        padding:6px 24px;
        text-decoration:none;
        text-shadow:0px 1px 0px #aade7c;
    }
    #btnSampleAssignment:hover {
        background:linear-gradient(to bottom, #5cb811 5%, #77d42a 100%);
        background-color:#5cb811;
    }
    #btnSampleAssignment:active {
        position:relative;
        top:1px;
    }

</style>