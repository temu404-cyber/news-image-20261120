// Entry for make.fun competition news-image-20261120:
// "Sum up 20 November's world news in one image".
//
// The image itself is entry.png, drawn by draw.py (Python + PIL) from the
// reporting of Friday 20 November 2026. This program only delivers it:
// it copies the PNG beside this file to the grader's output directory.
//
// Runs with no network, stdlib only. Output is byte-identical every run
// because the file is copied, never regenerated.
//
// Local run:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, 'entry.png');
// Resolve to an absolute path so the destination does not depend on the
// working directory the grader happens to start us in.
const outDir = resolve(process.env.MAKEFUN_OUTPUT_DIR ?? '/output');
const target = join(outDir, 'entry.png');

mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);
