// Entry for make.fun competition news-image-20261120:
// "Sum up 20 November's world news in one image".
//
// The deliverable is entry.png, drawn by draw.py (Python + PIL) from the
// reporting of Friday 20 November 2026. This entrypoint only hands it to
// the grader: it copies the PNG next to this file into the output folder.
//
// It needs no network and uses only the Node standard library. The copy
// makes every run byte-identical, because the file is never regenerated.
//
// Local run:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const folder = dirname(fileURLToPath(import.meta.url));
const png = join(folder, "entry.png");
// Resolve the destination up front so the result never depends on the
// working directory the grader happens to start in.
const outputDir = resolve(process.env.MAKEFUN_OUTPUT_DIR ?? "/output");

mkdirSync(outputDir, { recursive: true });
copyFileSync(png, join(outputDir, "entry.png"));
