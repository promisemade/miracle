export async function fetchJson(path) {
  const response = await fetch(path, { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`Impossible de charger ${path} (${response.status})`);
  }
  return response.json();
}

export function encodeRepoPath(path) {
  return path
    .split("/")
    .map((segment) => encodeURIComponent(segment))
    .join("/");
}

export function assetUrl(path) {
  if (!path) return "#";
  return `./${encodeRepoPath(path)}`;
}

export function localResourceUrl(sourceUrl) {
  if (!sourceUrl) return null;
  if (sourceUrl.startsWith("http://") || sourceUrl.startsWith("https://")) {
    return sourceUrl;
  }
  if (sourceUrl.startsWith("/resource/")) {
    return assetUrl(`Ressources/${sourceUrl.slice("/resource/".length)}`);
  }
  if (sourceUrl.startsWith("Ressources/")) {
    return assetUrl(sourceUrl);
  }
  return sourceUrl;
}

export function qs(selector, parent = document) {
  return parent.querySelector(selector);
}

export function qsa(selector, parent = document) {
  return Array.from(parent.querySelectorAll(selector));
}

export function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

export function sample(items, count) {
  const copy = [...items];
  for (let i = copy.length - 1; i > 0; i -= 1) {
    const j = Math.floor(Math.random() * (i + 1));
    [copy[i], copy[j]] = [copy[j], copy[i]];
  }
  return copy.slice(0, count);
}

export function countBy(items, getKey) {
  return items.reduce((acc, item) => {
    const key = getKey(item) || "Non renseigne";
    acc[key] = (acc[key] || 0) + 1;
    return acc;
  }, {});
}

export function toSortedEntries(record, limit = 10) {
  return Object.entries(record)
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0], "fr"))
    .slice(0, limit);
}

export function formatDate(value) {
  try {
    return new Date(value).toLocaleDateString("fr-FR");
  } catch {
    return value;
  }
}
