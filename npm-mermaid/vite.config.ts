import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import path from "path";

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  base: "./",

  build: {
    lib: {
      entry: {
        "instaui-mermaid": path.resolve(__dirname, "libs/index.ts"),
      },
      fileName: (_, entryName) => `${entryName}.js`,
      formats: ["es"],
    },
    // sourcemap: "inline",

    rollupOptions: {
      external: ["vue", "mermaid", "instaui"],
      // output: [],
    },
  },
});
