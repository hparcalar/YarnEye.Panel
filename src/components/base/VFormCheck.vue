<script setup lang="ts">
    import { defineProps, defineEmit } from 'vue';
    
    const props = defineProps({
      modelValue: { type: Boolean, required: true },
      label: { type: String, default: '' },
      postfix: { type: String, default: '' },
      disabled: { type: Boolean, default: false },
      placeholder: { type: String, default: '' },
    });
    const emit = defineEmit(['update:modelValue']);
    
    const onInput = (event: Event) => {
      let htmlVal = false;
      if ((event.target as HTMLInputElement).checked)
        htmlVal = true;
      emit('update:modelValue', htmlVal);
    }
    
    </script>
    <template inherit-attrs="false">
      <div :class="['v-form-check', { disabled: props.disabled }, $attrs.class]">
        <transition name="v-form-shared__fade">
          <span
            class="v-form-shared__label v-form-text__label"
          >
            {{ props.label }}
          </span>
        </transition>
        <div :class="['v-form-check__container', { 'has-postfix': props.postfix }]">
          <input
            type="checkbox"
            class="v-form-check__input"
            :checked="props.modelValue"
            :disabled="props.disabled"
            :placeholder="props.label || props.placeholder"
            @input="onInput"
          >
          <span v-show="postfix" class="v-form-check__postfix">
            {{ postfix }}
          </span>
        </div>
      </div>
    </template>
    <style lang="postcss">
    .v-form-check {
      position: relative;
    }
    .v-form-check__container {
      @apply flex items-center relative h-full;
    }
    .v-form-check__label {
      @apply z-30;
    }
    .v-form-check__input {
      @apply block w-full px-3 py-2 font-normal h-full relative z-20
            border rounded shadow-sm
            transition duration-100 ease-in-out
            focus:(ring-2 ring-blue-500 ring-offset-0 ring-opacity-50 outline-none)
            disabled:(opacity-50 cursor-not-allowed);
    
      @nest .v-form-check__container.has-postfix & {
        @apply rounded-r-none;
      }
    }
    .v-form-check__postfix {
      @apply block bg-gray-100 px-3 py-2 relative z-10
        border border-l-0
        rounded rounded-l-none;
    }
    </style>
    