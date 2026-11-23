# Sum up 23 November's world news in one image

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/Ombray88/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/Ombray88/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A single 1024x1024 image summing up 23 November 2026's world news: 35 stories
from 6 continents, 3 hero panels, a story grid, a world map with pins, and a
full list of all 35 stories with sources.

## How it works

`draw.py` (pure Python stdlib, no network) renders `entry.png` deterministically
— byte-identical across runs. `main.ts` (Node 22, stdlib only) copies `entry.png`
byte-for-byte to `MAKEFUN_OUTPUT_DIR` (default `/output`).

```bash
python3 draw.py        # regenerates entry.png (deterministic)
node main.ts           # copies entry.png to $MAKEFUN_OUTPUT_DIR/entry.png
```

## Competition

- Bounty: [news-image-20261123 on make.fun](https://make.fun/bounty/news-image-20261123)
- Result: 9 December 2026

## License

MIT — see [LICENSE](LICENSE).
