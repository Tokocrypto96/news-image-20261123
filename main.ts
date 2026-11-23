// Entry point for the make.fun news-image-20261123 entry.
//
// Copies the pre-rendered entry.png from this repository into the output
// directory, then verifies the copy by reading it back: PNG signature and
// 1024x1024 dimensions must match. Run with:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "out";
const src = join(import.meta.dirname, "entry.png");
const dest = join(outDir, "entry.png");

mkdirSync(outDir, { recursive: true });
copyFileSync(src, dest);

// Read-back verification: PNG signature + IHDR dimensions + byte identity.
const buf = readFileSync(dest);
const orig = readFileSync(src);
if (!buf.equals(orig)) {
  throw new Error("copied file differs from entry.png in the repository");
}
const PNG_SIG = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!buf.subarray(0, 8).equals(PNG_SIG)) {
  throw new Error("output is not a PNG file");
}
const width = buf.readUInt32BE(16);
const height = buf.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  throw new Error(`unexpected dimensions ${width}x${height}, expected 1024x1024`);
}
console.log(`OK: ${dest} (${width}x${height}, ${buf.length} bytes)`);
