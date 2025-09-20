const perfix = "instaui-mermaid_svg-";
let count = 0;

export function genSvgId() {
  return `${perfix}${count++}`;
}
