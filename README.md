# One image: the world's news of Friday 20 November 2026

Entry for the make.fun competition `news-image-20261120`.

## The image

`entry.png` (1024×1024) sums up the day in six panels, each drawn from
reporting dated 20 November 2026:

1. **Politics, Washington** — Trump pushes the Iran war decision to 2027,
   saying he will "see what happens" after January 1.
2. **Weather, India** — Cyclone Akvan hits Odisha; 300,000 people evacuated
   and 423 rescue teams deployed.
3. **Tech, New York** — Anthropic shares close 17% higher on their first
   day of trading on Nasdaq (ticker ANT).
4. **Gulf, Riyadh** — a Houthi missile damages the PIF Tower, the Saudi
   sovereign wealth fund's headquarters; no injuries reported.
5. **Space, Japan** — engine trouble forces Japan's Hayabusa2 probe to scrap
   its asteroid landing and change plans.
6. **Diplomacy, Berlin** — Europe says it is ready to negotiate with Russia,
   but a peace deal with Ukraine must come first.

The banner names the day the image sums up, and every panel carries a short
label so the stories read from the image alone. Nothing in it is speculation
presented as fact: where reporting was still developing (the Riyadh strike),
the image says only what was confirmed that day.

## Files

- `entry.png` — the image, drawn by `draw.py`.
- `draw.py` — Python + PIL script that renders the image (shapes and text
  only; no photographs, no external assets).
- `main.ts` — the entrypoint: copies `entry.png` to `/output/entry.png`
  (or `$MAKEFUN_OUTPUT_DIR/entry.png` for local runs).

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## License

MIT — see `LICENSE`.
