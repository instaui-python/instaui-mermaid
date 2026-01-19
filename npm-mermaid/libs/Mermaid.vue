<script setup lang="ts">
import mermaid from "mermaid";
import { type MermaidConfig } from "mermaid";
import { onBeforeUnmount, Ref, ref, watch } from "vue";
import { genSvgId } from "./utils";
import { createMermaidClickBinder } from "./hook/clickable";
import { normalizeMermaidInput } from "./hook/input";
import { useBindingGetter } from "instaui";

// props
interface TClickConfig {
  node: string;
  arg: string;
}

const props = defineProps<{
  graph: string;
  initConfig?: Partial<MermaidConfig>;
  clickConfigs?: TClickConfig[];
  errorRefName?: string;
}>();

// events
const emit = defineEmits<{
  "update:graph": [graph: string];
  "node:click": [
    {
      node: string;
      arg: string;
    },
  ];
  "render:error": [error: Error];
  "render:success": [graph: string];
}>();

const { initConfig, clickConfigs } = props;

const realInitConfig = {
  ...initConfig,
  startOnLoad: false,
  ...(clickConfigs && { securityLevel: "loose" }),
} satisfies MermaidConfig;

mermaid.initialize(realInitConfig);

const container = ref<HTMLDivElement>();
const svgId = genSvgId();

const binder = createMermaidClickBinder((node, arg) => {
  emit("node:click", {
    node,
    arg,
  });
});

const errorRef = props.errorRefName
  ? useBindingGetter().getRef(props.errorRefName)
  : null;
const lastGoodSvg = ref<string>("");

watch(
  [() => props.graph, container, () => props.clickConfigs],
  async ([graph, container, clickConfigs]) => {
    if (!container) return;

    graph = normalizeMermaidInput(graph);
    const realGraph = clickConfigs
      ? binder.enhance(graph, clickConfigs)
      : graph;

    const customErrorHandling = !!errorRef;

    if (customErrorHandling) {
      try {
        const { svg, bindFunctions } = await mermaid.render(
          svgId,
          realGraph,
          container,
        );
        container.innerHTML = svg;
        bindFunctions?.(container);
        lastGoodSvg.value = svg;
        emit("update:graph", realGraph);
        emit("render:success", realGraph);
        errorRef!.value = "";
      } catch (err: any) {
        container.innerHTML = lastGoodSvg.value;
        errorRef!.value = err?.message || String(err);
        emit("render:error", err);
      }
    } else {
      try {
        const { svg, bindFunctions } = await mermaid.render(
          svgId,
          realGraph,
          container,
        );
        container.innerHTML = svg;
        bindFunctions?.(container);
        emit("update:graph", realGraph);
        emit("render:success", realGraph);
      } catch (err: any) {
        console.warn("Mermaid render error (default mode):", err, realGraph);
        emit("render:error", err);
        throw err;
      }
    }
  },
);

onBeforeUnmount(() => binder.dispose());
</script>

<template>
  <div ref="container"></div>
</template>

<style scoped></style>
