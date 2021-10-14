<script lang="ts">
    // Global Component State
    import { useWindowSize } from '@vueuse/core';
    
    const isClient = typeof window !== 'undefined';
    const { width: windowWidth } = useWindowSize();
    
    /* eslint-disable prefer-const */
    // WHY: eslint fails to detect re-assignment in <script setup>
    let modalCount = 0;
    let lastClickEvent: MouseEvent;
    
    if (isClient) {
      const clickEventListener = (event: MouseEvent) => {
        lastClickEvent = event;
      };
    
      document.addEventListener('click', clickEventListener, { capture: true });
      if (import.meta.hot) {
        const hmr = import.meta.hot!;
        if (hmr.data.prevEventListener)
          document.removeEventListener('click', hmr.data.prevEventListener, { capture: true });
    
        hmr.data.prevEventListener = clickEventListener;
      }
    }
    </script>
    <script setup lang="ts">
    import { watch, ref, computed, defineProps, defineEmit } from 'vue';
    
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
        default: '',
      },
      visible: {
        type: Boolean,
        default: false,
      },
      transitionDuration: {
        type: Number,
        default: 200,
      },
      okText: {
        type: String,
        default: 'OK',
      },
      okButtonProps: {
        type: Object,
        default: () => ({}),
      },
      cancelText: {
        type: String,
        default: 'Cancel',
      },
      isSubmitVisible: {
        type: Boolean,
        default: true
      },
      isCancelVisible: {
        type:Boolean,
        default: true
      },
      cancelButtonProps: {
        type: Object,
        default: () => ({}),
      },
      closable: {
        type: Boolean,
        default: true,
      },
      overlayClosable: {
        type: Boolean,
        default: true,
      },
    });
    const emit = defineEmit(['ok', 'cancel', 'after-close']);
    
    const onOverlayClick = () => {
      if (props.overlayClosable)
        emit('cancel');
    };
    const modalTitleId = `vModalTitle-${modalCount++}`;
    const modalTop = 50;
    const modalLeft = computed(() =>
      Math.max(0, (windowWidth.value - props.width) / 2),
    );
    
    const transformOrigin = ref({ x: 0, y: 0 });
    const transformOriginAttr = computed(() => `\
      ${transformOrigin.value.x}px\
      ${transformOrigin.value.y}px 0px`,
    );
    
    watch(
      () => props.visible,
      (isVisible) => {
        if (isVisible) {
          if (lastClickEvent.clientX || lastClickEvent.clientY) {
            transformOrigin.value.x = lastClickEvent.clientX - modalLeft.value;
            transformOrigin.value.y = lastClickEvent.clientY - modalTop;
          } else {
            transformOrigin.value.x = 0;
            transformOrigin.value.y = 0;
          }
        }
      },
    );
    
    // Handle body stylings
    if (isClient) {
      let lastBodyStyle: string | null = null;
      watch(
        () => props.visible,
        (isVisible) => {
          if (isVisible) {
            lastBodyStyle = document.body.getAttribute('style');
            document.body.style.overflow = 'hidden';
          }
          else {
            document.body.setAttribute('style', lastBodyStyle || '');
          }
        });
    }
    
    </script>
    <template>
      <teleport to="body">
        <div
          class="v-modal"
          :style="{ '--duration': `${props.transitionDuration}ms` }"
          v-bind="$attrs"
        >
          <transition name="v-modal__fade" :duration="props.transitionDuration">
            <div v-show="props.visible" class="v-modal__overlay" />
          </transition>
          <transition :duration="props.transitionDuration">
            <div
              v-show="props.visible"
              role="dialog"
              :aria-labelledby="modalTitleId"
              class="v-modal__wrapper"
              @click="onOverlayClick"
            >
              <transition
                name="v-modal__zoom"
                @after-leave="emit('after-close')"
              >
                <div
                  v-show="props.visible"
                  class="v-modal__modal"
                  :class="props.cssClass"
                  :style="{
                    top: `${modalTop}px`,
                    left: `${modalLeft}px`,
                    width: `${props.width}px`,
                    transformOrigin: transformOriginAttr,
                  }"
                  @click.stop
                >
                  <div class="v-modal__modal-header">
                    <p :id="modalTitleId" class="inline-block">
                      {{ props.title }}
                    </p>
                    <button
                      v-if="props.closable"
                      class="icon-btn v-modal__modal-close"
                      :tabindex="props.visible ? 0 : -1"
                      :title="props.cancelText"
                      @click="emit('cancel')"
                    >
                    </button>
                  </div>
                  <div
                    class="v-modal__modal-body"
                  >
                    <slot />
                  </div>
                  <div class="v-modal__modal-footer">
                    <button
                      v-if="props.isSubmitVisible == true"
                      class="btn v-modal__modal-button v-modal__ok-button"
                      v-bind="props.okButtonProps"
                      @click="emit('ok')"
                    >
                      {{ okText }}
                    </button>
                    <button
                      v-if="props.isCancelVisible == true"
                      class="btn btn-transparent v-modal__modal-button v-modal__cancel-button"
                      v-bind="props.cancelButtonProps"
                      @click="emit('cancel')"
                    >
                      {{ props.cancelText }}
                    </button>
                  </div>
                </div>
              </transition>
            </div>
          </transition>
        </div>
      </teleport>
    </template>
    <style lang="postcss">
    .v-modal {
      @apply relative;
    }
    .v-modal__overlay {
      @apply fixed inset-0 z-1000 bg-black bg-opacity-40;
    }
    .v-modal__wrapper {
      @apply fixed inset-0 z-1000;
    }
    .v-modal__modal {
      @apply absolute bg-white rounded max-w-screen;
    }
    .v-modal__modal-close {
      @apply absolute top-4 right-4;
    }
    .v-modal__modal-button {
      @apply py-2;
    }
    .v-modal__modal-header {
      @apply rounded-t p-4 border-b relative text-xl text-medium;
    }
    .v-modal__modal-body {
      @apply p-4;
    }
    .v-modal__modal-footer {
      @apply rounded-b px-4 py-2 space-x-2 border-t text-right;
    }
    
    /* Transition: Fade */
    .v-modal__fade-enter-active,
    .v-modal__fade-leave-active {
      @apply z-1000;
      transition-property: opacity;
      transition-duration: var(--duration);
      transition-timing-function: linear;
    }
    .v-modal__fade-enter-from,
    .v-modal__fade-leave-to {
      opacity: 0;
    }
    /* Transition: Zoom */
    .v-modal__zoom-enter-active,
    .v-modal__zoom-leave-active {
      transition-property: transform, opacity;
      transition-duration: var(--duration);
    }
    .v-modal__zoom-enter-active {
      transition-timing-function: easeOutQuint;
    }
    .v-modal__zoom-leave-active {
      transition-timing-function: easeInQuint;
    }
    
    .v-modal__zoom-enter-from,
    .v-modal__zoom-leave-to {
      transform: scale(0);
      opacity: 0;
    }
    
    .v-modal__zoom-enter-to,
    .v-modal__zoom-leave-from {
      transform: scale(1);
      opacity: 1;
    }
    </style>
    