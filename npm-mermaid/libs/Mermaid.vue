<script setup lang="ts">
import mermaid from "mermaid";
import { type MermaidConfig } from "mermaid";
import { ref, watch } from "vue";
import { genSvgId } from "./utils";

// props
const props = defineProps<{
  graph: string;
  initConfig?: Partial<MermaidConfig>;
}>();

// events
const emit = defineEmits<{
  "update:graph": [graph: string];
}>();

const {
  initConfig = {
    securityLevel: "loose",
  },
} = props;

mermaid.initialize({
  ...initConfig,
  startOnLoad: false,
});

const container = ref<HTMLDivElement>();
const svgId = genSvgId();

watch([() => props.graph, container], async ([graph, container]) => {
  if (container) {
    const { svg, bindFunctions } = await mermaid.render(
      svgId,
      graph,
      container
    );
    container.innerHTML = svg;
    bindFunctions?.(container);
    emit("update:graph", graph);
  }
});
</script>

<template>
  <div ref="container"></div>
</template>

<style scoped></style>
