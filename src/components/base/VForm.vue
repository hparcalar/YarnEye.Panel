<script setup lang="ts">
    import { defineProps, defineEmit } from 'vue';
    
    const emit = defineEmit(['submit', 'cancel']);
    const props = defineProps({
      title: {
        type: String,
        default: '',
      },
      description: {
        type: String,
        default: '',
      },
      disabled: {
        type: Boolean,
        default: false,
      },
      cancellable: {
        type: Boolean,
        default: true,
      },
      cancelText: {
        type: String,
        default: 'Vazgeç',
      },
      submitText: {
        type: String,
        default: 'Kaydet',
      },
      onSubmit: {},
    });
    
    </script>
    <template>
      <form class="v-form" @submit.prevent="emit('submit', $event)">
        <input class="v-form__first-focusable">
        <div class="v-form__body">
          <div>
            <h3 class="v-form__title">
              {{ props.title }}
            </h3>
            <p class="v-form__description">
              {{ props.description }}
            </p>
          </div>
          <div class="v-form__seperator" />
          <slot />
        </div>
        <div class="v-form__footer">
          <button type="submit" class="v-form__submit btn" :disabled="props.disabled">
            {{ props.submitText }}
          </button>
          <button
            v-if="cancellable"
            type="button"
            class="v-form__cancel btn btn-danger bg-gray-300"
            @click="emit('cancel')"
          >
            {{ props.cancelText }}
          </button>
        </div>
      </form>
    </template>
    <style lang="postcss">
    .v-form__body {
      @apply p-4 bg-white space-y-3 text-gray-800;
    }
    .v-form__first-focusable {
      @apply absolute opacity-0;
    }
    .v-form__title {
      @apply text-lg font-medium;
    }
    .v-form__description {
      @apply text-sm text-gray-600;
    }
    .v-form__seperator {
      @apply w-full h-1 border-t ;
    }
    .v-form__cancel {
      @apply ml-2;
    }
    .v-form__footer {
      @apply bg-gray-50 px-4 py-3 text-right border-t ;
    }
    </style>
    