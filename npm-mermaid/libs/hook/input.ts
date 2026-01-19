/**
 * Normalizes Mermaid input text by removing empty lines that might affect Frontmatter parsing
 * @param input Raw user input text
 * @returns Normalized text
 */
export function normalizeMermaidInput(input: string): string {
  if (!input) return "";

  // Remove leading empty lines
  let lines = input.split("\n");

  // Find first non-empty line
  const firstNonEmptyIndex = lines.findIndex((line) => line.trim() !== "");
  if (firstNonEmptyIndex === -1) return "";

  lines = lines.slice(firstNonEmptyIndex);

  // Handle frontmatter indentation
  // If there's frontmatter (starts with ---)
  if (lines[0].trim() === "---") {
    // Find frontmatter end line
    const endIndex = lines.findIndex(
      (line, idx) => idx > 0 && line.trim() === "---",
    );
    if (endIndex !== -1) {
      // Remove empty lines around frontmatter
      const frontmatter = lines.slice(0, endIndex + 1);
      const rest = lines.slice(endIndex + 1);

      // Remove empty lines after frontmatter
      const restTrimmed = rest
        .join("\n")
        .replace(/^\s*\n+/, "")
        .replace(/\n+$/, "");

      return [...frontmatter, restTrimmed].join("\n");
    }
  }

  // No frontmatter - just remove surrounding empty lines
  return lines
    .join("\n")
    .replace(/^\s*\n+/, "")
    .replace(/\n+$/, "");
}
