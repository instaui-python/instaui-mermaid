export interface MermaidNodeClickConfig {
  node: string;
  arg?: string;
}

export type MermaidNodeClickHandler = (node: string, arg: string) => void;

export interface MermaidClickBinder {
  enhance(code: string, configs: MermaidNodeClickConfig[]): string;

  dispose(): void;

  readonly namespace: string;
}

/* ---------------- internal ---------------- */

function generateNamespace(): string {
  return `mm_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;
}

function appendClickLines(code: string, lines: string[]): string {
  return (
    code.trimEnd() +
    "\n\n%% auto generated click handlers\n" +
    lines.join("\n") +
    "\n"
  );
}

type DispatcherFn = (nodeId: string) => void;

interface DispatcherWindow extends Window {
  [key: string]: DispatcherFn | any;
}

/* ---------------- public api ---------------- */

export function createMermaidClickBinder(
  handler: MermaidNodeClickHandler,
): MermaidClickBinder {
  const win = window as DispatcherWindow;

  const namespace = generateNamespace();
  const dispatcherName = `__MERMAID_CLICK_DISPATCHER__${namespace}`;

  const handlerMap = new Map<string, MermaidNodeClickHandler>();

  // dispatcher
  win[dispatcherName] = (nodeId: string) => {
    const fn = handlerMap.get(nodeId);
    if (fn) {
      fn(nodeId, nodeId);
    }
  };

  function enhance(code: string, configs: MermaidNodeClickConfig[]): string {
    handlerMap.clear();

    const clickLines: string[] = [];

    for (const cfg of configs) {
      const arg = cfg.arg ?? cfg.node;

      handlerMap.set(cfg.node, (node) => handler(node, arg));

      // mermaid syntax: click node functionName
      clickLines.push(`click ${cfg.node} ${dispatcherName}`);
    }

    return appendClickLines(code, clickLines);
  }

  function dispose() {
    handlerMap.clear();
    try {
      delete win[dispatcherName];
    } catch {
      win[dispatcherName] = undefined;
    }
  }

  return {
    enhance,
    dispose,
    namespace,
  };
}
