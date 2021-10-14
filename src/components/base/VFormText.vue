<script setup lang="ts">
    import { defineProps, defineEmits } from 'vue';
    
    const props = defineProps({
      modelValue: { type: String, required: true },
      label: { type: String, default: '' },
      type: { type: String, default: 'text' },
      postfix: { type: String, default: '' },
      disabled: { type: Boolean, default: false },
      placeholder: { type: String, default: '' },
    });
    const emit = defineEmits(['update:modelValue']);
    
    const onInput = (event: Event) =>
      emit('update:modelValue', (event.target as HTMLInputElement).value);
    
    </script>
    <template inherit-attrs="false">
      <div :class="['v-form-text', { disabled: props.disabled }, $attrs.class]">
        <transition name="v-form-shared__fade">
          <span
            
            class="v-form-shared__label v-form-text__label"
          >
            {{ props.label }}
          </span>
        </transition>
        <div :class="['v-form-text__container', { 'has-postfix': props.postfix }]">
          <input
            :type="props.type"
            class="v-form-text__input"
            :value="props.modelValue"
            :disabled="props.disabled"
            :placeholder="props.label || props.placeholder"
            @input="onInput"
          >
          <span v-show="postfix" class="v-form-text__postfix">
            {{ postfix }}
          </span>
        </div>
      </div>
    </template>
    <style lang="postcss">
    .v-form-text {
      position: relative;
    }
    .v-form-text__container {
      @apply flex items-center relative;
    }
    .v-form-text__label {
      @apply z-30;
    }
    .v-form-text__input {
      @apply block w-full px-3 py-2 font-normal relative z-20
            border rounded shadow-sm
            transition duration-100 ease-in-out
            focus:(ring-2 ring-blue-500 ring-offset-0 ring-opacity-50 outline-none)
            disabled:(opacity-50 cursor-not-allowed);
    
      @nest .v-form-text__container.has-postfix & {
        @apply rounded-r-none;
      }
    }
    .v-form-text__postfix {
      @apply block bg-gray-100 px-3 py-2 relative z-10
        border border-l-0
        rounded rounded-l-none;
    }
    </style>
    