<script setup lang="ts">
    import { ref, onMounted, Ref, inject } from 'vue';
    import { useRouter } from 'vue-router';
    import checkAuthRoute from '../handlers/auth.filter';
    import VFormText from './base/VFormText.vue';
    import { YarnEyeService } from '../services/yarneye.service'
    import { ProdLine } from '../models/yarn.models'
    
    const router = useRouter();
    const toast:any = inject('toast');
    
    onMounted(() => {
      checkAuthRoute(router, 'assignments');
      loadList();
    });

    const yarnService:YarnEyeService = new YarnEyeService();

    const lineList:Ref<ProdLine[]> = ref([]);
    const selectedLineList: Ref<ProdLine[]> = ref([]);
    const lineSelectionFinished: Ref<boolean> = ref(false);
    const sampleAssignmentFinished: Ref<boolean> = ref(false);

    const loadList = async() => {
        const data = await yarnService.getProdLineList();
        if (data)
        {
            lineList.value = data;
        }
    }

    const selectToggleProdLine = (item: ProdLine) => {
        if (selectedLineList.value.some(d => d.prodLineId == item.prodLineId))
            selectedLineList.value = selectedLineList.value.filter(d => d.prodLineId != item.prodLineId);
        else
            selectedLineList.value.push(item);
    }

    const isLineSelected = (item: ProdLine) => {
        return selectedLineList.value.some(d => d.prodLineId == item.prodLineId);
    }

    const finishLineSelection = () => {
        if (selectedLineList.value.length == 0){
            toast.error('En az 1 hat seçmelisiniz.');
            return;
        }

        lineSelectionFinished.value = true;
    }
    
</script>
<template>
  <div class="py-2 px-3">
      <h5 class="font-bold  py-2 px-2 rounded-lg text-shadow-sm my-3" 
        style="background-color:rgba(207,231,250,1);">Örneklem Atama</h5>
      <div class="px-2 py-2">
          <!-- PROD LINE SELECTION -->
          <div v-if="lineSelectionFinished == false" class="flex flex-col">
              <div class="flex flex-row justify-center bg-green-100 rounded-lg py-2 mb-4">
                  <h6 class="text-right font-bold" style="padding-top:10px;">Önce Hatları Seçin</h6>
                  <button 
                    @click="finishLineSelection"
                    type="button" class="btn btn-sm btn-success ml-3">
                      İleri
                  </button>
              </div>
              <div  class="flex flex-wrap">
                <button type="button" class="btn btn-primary mx-2 w-120px h-100px" 
                    v-for="(item, index) in lineList" :key="index"
                    :class="{'btn-success': isLineSelected(item) == true}"
                    @click="selectToggleProdLine(item)">
                    {{ item.prodLineCode }}
                </button>
            </div>
          </div>

          <!-- SAMPLE IMAGE ASSIGNMENT -->
          <div v-if="lineSelectionFinished == true && sampleAssignmentFinished == false">
              <div class="flex flex-row justify-center bg-green-100 rounded-lg py-2 mb-4">
                  <h6 class="text-right font-bold" style="padding-top:10px;">Örnek Bobini Yerleştirin</h6>
                  <button 
                    type="button" class="btn btn-sm btn-success ml-3">
                      Tamamla
                  </button>
              </div>
              <div>

              </div>
          </div>
      </div>
  </div>
</template>
<style lang="postcss" scoped>
.unfold-enter-start {
  max-height: 0
}
</style>
  