<script setup lang="ts">
    import { ref, onMounted, Ref } from 'vue';
    import { useRouter } from 'vue-router';
    import checkAuthRoute from '../handlers/auth.filter';
    import VFormText from './base/VFormText.vue';
    import { YarnEyeService } from '../services/yarneye.service'
    import { ProdLine } from '../models/yarn.models'
    
    const router = useRouter();
    
    onMounted(() => {
      checkAuthRoute(router, 'lines');

      loadList();
    });

    const yarnService:YarnEyeService = new YarnEyeService();

    const lineList:Ref<ProdLine[]> = ref([]);
    const formData = ref({ prodLineId: 0, prodLineCode: '', prodLineName: '' });

    const loadList = async() => {
        const data = await yarnService.getProdLineList();
        if (data)
        {
            lineList.value = data;
        }
    }
    
    const onFormSubmit = () => {
      
    };
    
    </script>
    <template>
      <div>
          <h5>Üretim Hatları</h5>
          <div>
              
          </div>
      </div>
    </template>
    <style lang="postcss" scoped>
    .unfold-enter-start {
      max-height: 0
    }
    </style>
    