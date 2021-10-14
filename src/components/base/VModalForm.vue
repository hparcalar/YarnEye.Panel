<script lang="ts">
    // Global Component State
    
    /* eslint-disable prefer-const */
    // WHY: eslint fails to detect re-assignment in <script setup>
    
    let modalFormCount = 0;
    
    </script>
    <script setup lang="ts">
    import { watch, nextTick, defineProps, defineEmit } from 'vue';
    import VModal from './VModal.vue';
import VForm from './VForm.vue';
    
    const props = defineProps({
      title: {
        type: String,
        default: '',
      },
      width: {
        type: Number,
        default: 520,
      },
      cssClass: {
        type: String,
        default:'',
      },
      description: {
        type: String,
        default: '',
      },
      disabled: {
        type: Boolean,
        default: false,
      },
      visible: {
        type: Boolean,
        default: false,
      },
      cancelText: {
        type: String,
        default: 'Cancel',
      },
      submitText: {
        type: String,
        default: 'Submit',
      },
      isSubmitVisible: {
        type: Boolean,
        default: true
      },
      isCancelVisible: {
        type:Boolean,
        default: true
      }
    });
    
    const emit = defineEmit(['cancel', 'submit', 'after-close']);
    
    const modalFormId = `vModalForm-${modalFormCount++}`;
    
    // Move focus to form when modal is visible
    watch(
      () => props.visible,
      (isVisible) => {
        const form = document.getElementById(modalFormId) as HTMLFormElement | null;
        if (form) {
          const firstFocusable = form.querySelector('.v-form__first-focusable') as HTMLInputElement | null;
          if (firstFocusable) {
            if (isVisible) {
              nextTick(() => {
                firstFocusable.focus();
                firstFocusable.blur();
                firstFocusable.setAttribute('tabindex', '-1');
              });
            } else {
              firstFocusable.removeAttribute('tabindex');
            }
          }
        }
      }
    )
    
    const onOk = () => {
      const form = document.getElementById(modalFormId) as HTMLFormElement | null;
      if (form) {
        if (form.requestSubmit) { form.requestSubmit(); }
        else {
          const button = form.querySelector('button[type=submit]') as HTMLButtonElement | null;
          if (button)
            button.click();
          else
            throw new Error('No submit button inside form');
        }
      }
    }
    
    </script>
    <template inherit-attrs="false">
      <VModal
        class="v-modal-form__modal"
        v-bind="$attrs"
        :width="props.width"
        :css-class="props.cssClass"
        :title="props.title"
        :ok-text="props.submitText"
        :ok-button-props="{ disabled: props.disabled }"
        :cancel-text="props.cancelText"
        :visible="props.visible"
        :is-cancel-visible="props.isCancelVisible"
        :is-submit-visible="props.isSubmitVisible"
        @ok="onOk"
        @cancel="emit('cancel')"
        @after-close="emit('after-close')"
      >
        <VForm
          :id="modalFormId"
          :description="props.description"
          :disabled="props.disabled"
          class="v-modal-form__form"
          @submit="emit('submit')"
        >
          <slot />
        </VForm>
      </VModal>
    </template>
    <style lang="postcss">
    .v-modal-form__form {
      & .v-form__body {
        @apply py-0;
      }
      & .v-form__footer {
        @apply hidden;
      }
    }
    </style>
    