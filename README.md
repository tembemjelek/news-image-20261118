# Sum up 18 November 2026 world news in one image

make.fun bounty: news-image-20261118

Account: @steady-comet-66 (Solana wallet fbmh...o9ER, full address not shown on profile)

Deadline: Fri 20 Nov 2026 07:00 WIB

## How it works

`main.py` is a deterministic Python 3.13 program, standard library
only, no network. It draws a 1024x1024 newspaper front page with its
own 5x7 bitmap font and its own PNG encoder (zlib/struct), and writes `/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR/entry.png` locally).

Run locally:

```
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Stories in the image (all Wed 18 Nov 2026)

- Lead: Iran hits back at Kuwait and Bahrain after the US strike
  on Qeshm Island; a UAE ship is hit in Hormuz (1 missing, 11 hurt)
- Xi greets Trump in Shenzhen; Xi and Putin meet a day before
  the first Trump-Xi-Putin summit
- Ukraine hits the Kerch Bridge for a second day
- Democrat Mary Peltola wins Alaska's Senate seat; Democrats
  take a 56-44 majority
- Nvidia beats forecasts: $115.8B revenue, up 103%; board says
  it will not reinstate Jensen Huang
- Also: Ebola in DR Congo passes 11,000 cases; Cyclone Akvan
  heads for India; Gaza flood risk for 950,000 displaced people

Full facts and sources: see NOTES.md.
