// main.ts — entrypoint for make.fun competition gta6-meme-x-01.
//
// Reads POST.json from the repository (MAKEFUN_BOT_DIR), validates that its
// url names an X post, copies it to MAKEFUN_OUTPUT_DIR/POST.json and verifies
// the copy byte-for-byte. That is all it does.
//
// Run: mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const BOT_DIR = process.env.MAKEFUN_BOT_DIR;
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR;

if (!BOT_DIR) {
  console.error("MAKEFUN_BOT_DIR is not set");
  process.exit(1);
}
if (!OUTPUT_DIR) {
  console.error("MAKEFUN_OUTPUT_DIR is not set");
  process.exit(1);
}

const URL_RE =
  /^https:\/\/(?:x\.com|twitter\.com)\/(?:[A-Za-z0-9_]+|%3Chandle%3E|<handle>)\/status\/(?:\d+|<id>)$/;

const srcPath = join(BOT_DIR, "POST.json");
const raw = readFileSync(srcPath, "utf8");

let parsed: unknown;
try {
  parsed = JSON.parse(raw);
} catch {
  console.error("POST.json is not valid JSON");
  process.exit(1);
}
if (typeof parsed !== "object" || parsed === null || Array.isArray(parsed)) {
  console.error("POST.json must be a JSON object");
  process.exit(1);
}
const url = (parsed as Record<string, unknown>).url;
if (typeof url !== "string" || !URL_RE.test(url)) {
  console.error(`POST.json url is not an X post address: ${String(url)}`);
  process.exit(1);
}

mkdirSync(OUTPUT_DIR, { recursive: true });
const destPath = join(OUTPUT_DIR, "POST.json");
writeFileSync(destPath, raw, "utf8");

const copied = readFileSync(destPath, "utf8");
if (copied !== raw) {
  console.error("POST.json copy failed byte-for-byte verification");
  process.exit(1);
}

console.log(`POST.json copied to ${destPath}: ${url}`);
