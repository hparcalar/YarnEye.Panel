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
      checkAuthRoute(router, 'lines');
      loadList();
    });

    const yarnService:YarnEyeService = new YarnEyeService();

    const lineList:Ref<ProdLine[]> = ref([]);
    const formData:Ref<ProdLine> = ref({ prodLineId: 0, prodLineCode: '', 
      prodLineName: '', orderNo: null, assignmentId: null });

    const loadList = async() => {
        const data = await yarnService.getProdLineList();
        if (data)
        {
            lineList.value = data;
        }
    }

    const selectProdLine = (item:ProdLine) => {
      formData.value = item;
    }

    const newProdLine = () => {
      formData.value = {
        prodLineId: 0, prodLineCode: '', 
          prodLineName: '', orderNo: null, assignmentId: null
      }
    }
    
    const saveProdLine = async() => {
      const postData = await yarnService.saveProdLine(formData.value); 
       if (postData.result == true){
          formData.value.prodLineId = postData.recordId;
          toast.success('Kayıt başarılı');
          await loadList();
       }
       else
        toast.error(postData.errorMessage);
    };
    
</script>
<template>
  <div class="py-2 px-3">
      <h5 class="font-bold  py-2 px-2 rounded-lg text-shadow-sm my-3" style="background-color:rgba(207,231,250,1);">Üretim Hatları</h5>
      <div class="grid grid-cols-12">
          <!-- PROD LINE FORM -->
          <div class="flex flex-col px-2 py-2 col-span-4 bg-gray-100">
            <VFormText
                v-model="formData.prodLineCode"
                class="my-2"
                :label="'Hat Kodu'"
                :required="true"
            />

            <VFormText
                v-model="formData.prodLineName"
                class="my-2"
                :label="'Hat Adı'"
                :required="true"
            />

            <div class="flex flex-row">
              <button 
                @click="newProdLine"
                type="button" class="my-2 btn btn-sm btn-primary w-120px">
                Yeni
              </button>
              <button 
                @click="saveProdLine"
                type="button" class="my-2 mx-2 btn btn-sm btn-success w-120px">
                Kaydet
              </button>
            </div>
          </div>

          <!-- PROD LINE LIST -->
          <div class="ml-2 px-2 py-2 col-span-8">
            <table class="my-0 table table-bordered table-condensed">
              <thead>
                <tr>
                  <th class="w-25">Hat Kodu</th>
                  <th class="w-50">Hat Adı</th>
                  <th class="w-25">#</th>
                </tr>
              </thead>
            </table>
            <table class="my-0 table table-bordered table-condensed">
              <tbody>
                <tr v-for="(item, index) in lineList" :key="index" 
                  :class="{'bg-blue-100': formData.prodLineId == item.prodLineId}">
                  <td class="w-25">{{ item.prodLineCode }}</td>
                  <td class="w-50">{{ item.prodLineName }}</td>
                  <td class="w-25 py-1">
                    <button 
                      @click="selectProdLine(item)"
                      type="button" class="btn btn-sm btn-primary">
                      Düzenle
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
      </div>
  </div>
</template>
<style lang="postcss" scoped>
.unfold-enter-start {
  max-height: 0
}
</style>
  