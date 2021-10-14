<script setup lang="ts">
    import { defineProps, defineEmit } from 'vue';
    
    const props = defineProps({
      modelValue: { type: Number, required: true },
      label: { type: String, default: '' },
      postfix: { type: String, default: '' },
      disabled: { type: Boolean, default: false },
      placeholder: { type: String, default: '' },
    });
    const emit = defineEmit(['update:modelValue']);
    
    const onInput = (event: Event) => {
      let htmlVal = 0;
      if ((event.target as HTMLInputElement).value && (event.target as HTMLInputElement).value.length > 0)
        htmlVal = parseInt((event.target as HTMLInputElement).value);
      emit('update:modelValue', htmlVal);
    }
    
    </script>
    <template inherit-attrs="false">
      <div :class="['v-form-number', { disabled: props.disabled }, $attrs.class]">
        <transition name="v-form-shared__fade">
          <span
            class="v-form-shared__label v-form-text__label"
          >
            {{ props.label }}
          </span>
        </transition>
        <div :class="['v-form-number__container', { 'has-postfix': props.postfix }]">
          <input
            type="number"
            class="v-form-number__input"
            :value="props.modelValue"
            :disabled="props.disabled"
            :placeholder="props.label || props.placeholder"
            @input="onInput"
          >
          <span v-show="postfix" class="v-form-number__postfix">
            {{ postfix }}
          </span>
        </div>
      </div>
    </template>
    <style lang="postcss">
    .v-form-number {
      position: relative;
    }
    .v-form-number__container {
      @apply flex items-center relative;
    }
    .v-form-number__label {
      @apply z-30;
    }
    .v-form-number__input {
      @apply block w-full px-3 py-2 font-normal relative z-20
            border rounded shadow-sm
            transition duration-100 ease-in-out
            focus:(ring-2 ring-blue-500 ring-offset-0 ring-opacity-50 outline-none)
            disabled:(opacity-50 cursor-not-allowed);
    
      @nest .v-form-number__container.has-postfix & {
        @apply rounded-r-none;
      }
    }
    .v-form-number__postfix {
      @apply block bg-gray-100 px-3 py-2 relative z-10
        border border-l-0
        rounded rounded-l-none;
    }
    </style>
    