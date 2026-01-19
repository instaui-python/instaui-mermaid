import { defineComponent as h, ref as k, watch as C, onBeforeUnmount as I, createElementBlock as M, openBlock as $ } from "vue";
import g from "mermaid";
const v = "instaui-mermaid_svg-";
let w = 0;
function x() {
  return `${v}${w++}`;
}
function L() {
  return `mm_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;
}
function y(o, n) {
  return o.trimEnd() + `

%% auto generated click handlers
` + n.join(`
`) + `
`;
}
function E(o) {
  const n = window, r = L(), e = `__MERMAID_CLICK_DISPATCHER__${r}`, i = /* @__PURE__ */ new Map();
  n[e] = (s) => {
    const l = i.get(s);
    l && l(s, s);
  };
  function a(s, l) {
    i.clear();
    const d = [];
    for (const t of l) {
      const c = t.arg ?? t.node;
      i.set(t.node, (m) => o(m, c)), d.push(`click ${t.node} ${e}`);
    }
    return y(s, d);
  }
  function f() {
    i.clear();
    try {
      delete n[e];
    } catch {
      n[e] = void 0;
    }
  }
  return {
    enhance: a,
    dispose: f,
    namespace: r
  };
}
function j(o) {
  if (!o) return "";
  let n = o.split(`
`);
  const r = n.findIndex((e) => e.trim() !== "");
  if (r === -1) return "";
  if (n = n.slice(r), n[0].trim() === "---") {
    const e = n.findIndex(
      (i, a) => a > 0 && i.trim() === "---"
    );
    if (e !== -1) {
      const i = n.slice(0, e + 1), f = n.slice(e + 1).join(`
`).replace(/^\s*\n+/, "").replace(/\n+$/, "");
      return [...i, f].join(`
`);
    }
  }
  return n.join(`
`).replace(/^\s*\n+/, "").replace(/\n+$/, "");
}
const N = /* @__PURE__ */ h({
  __name: "Mermaid",
  props: {
    graph: {},
    initConfig: {},
    clickConfigs: {}
  },
  emits: ["update:graph", "node:click"],
  setup(o, { emit: n }) {
    const r = o, e = n, { initConfig: i, clickConfigs: a } = r, f = {
      ...i,
      startOnLoad: !1,
      ...a && { securityLevel: "loose" }
    };
    g.initialize(f);
    const s = k(), l = x(), d = E((t, c) => {
      e("node:click", {
        node: t,
        arg: c
      });
    });
    return C(
      [() => r.graph, s, () => r.clickConfigs],
      async ([t, c, m]) => {
        if (c) {
          t = j(t);
          const u = m ? d.enhance(t, m) : t, { svg: _, bindFunctions: p } = await g.render(
            l,
            u,
            c
          );
          c.innerHTML = _, p == null || p(c), e("update:graph", u);
        }
      }
    ), I(() => d.dispose()), (t, c) => ($(), M("div", {
      ref_key: "container",
      ref: s
    }, null, 512));
  }
});
export {
  N as default
};
