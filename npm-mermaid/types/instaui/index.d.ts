import type { Ref } from "vue";

type TAppMode = "web" | "webview" | "zero";

declare module "instaui" {
  export function useBindingGetter(): {
    getRef: (key: any) => Ref;
  };

  export function useLanguage(): Ref<string>;
  export function useDark(): Ref<boolean>;
  export function getAppInfo(): {
    mode: TAppMode;
  };
}
