<script setup lang="ts">
import mermaid from "mermaid";
import { type MermaidConfig } from "mermaid";
import { onBeforeUnmount, ref, watch } from "vue";
import { genSvgId } from "./utils";
import { createMermaidClickBinder } from "./hook/clickable";
import { normalizeMermaidInput } from "./hook/input";

// props
interface TClickConfig {
  node: string;
  arg: string;
}

const props = defineProps<{
  graph: string;
  initConfig?: Partial<MermaidConfig>;
  clickConfigs?: TClickConfig[];
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

watch(
  [() => props.graph, container, () => props.clickConfigs],
  async ([graph, container, clickConfigs]) => {
    if (container) {
      graph = normalizeMermaidInput(graph);

      const realGraph = clickConfigs
        ? binder.enhance(graph, clickConfigs)
        : graph;

      const { svg, bindFunctions } = await mermaid.render(
        svgId,
        realGraph,
        container,
      );
      container.innerHTML = svg;
      bindFunctions?.(container);
      emit("update:graph", realGraph);
    }
  },
);

onBeforeUnmount(() => binder.dispose());
</script>

<template>
  <div ref="container"></div>
</template>

<style scoped></style>
