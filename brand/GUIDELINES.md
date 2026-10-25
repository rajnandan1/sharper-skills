# sharper-skills logo guidelines

One page. The files named here live in `brand/`.

## 1. The logo

The symbol is the `>` prompt sign drawn as two blades that taper to one point. The wordmark is `sharper-skills` set in JetBrains Mono Bold, outlined to paths, with the hyphen replaced by a small tapered blade. The symbol works alone. The wordmark works alone. The horizontal lockup is the default pairing. Use the stacked lockup where the horizontal one would drop below its minimum size.

| Use | File |
| --- | --- |
| Symbol, ink | `sharper-skills-symbol.svg` |
| Symbol, white, thinned for dark backgrounds | `sharper-skills-symbol-white.svg` |
| Symbol, one colour in Signal | `sharper-skills-symbol-mono-f04e23.svg` |
| Horizontal lockup, ink, white, black, Signal | `sharper-skills-horizontal*.svg`, PNG at 1200 px |
| Stacked lockup, ink, white, black, Signal | `sharper-skills-stacked*.svg` |
| Wordmark alone | `sharper-skills-wordmark.svg` |
| Plugin icon, ink on a Signal tile | `../.claude-plugin/icon.png`, 1024 px |
| Favicon and web icons | `web/` with `head-snippet.html` |

## 2. Clear space

Keep a margin around the logo equal to the symbol's back thickness, which is the height of one blade at its thick end. That is 80 units on the 256-unit symbol, or 0.4 times the symbol's height. Nothing else enters that margin.

## 3. Minimum size

| Asset | Screen | Print |
| --- | --- | --- |
| Symbol | 16 px tall | 5 mm tall |
| Horizontal lockup | 120 px wide | 30 mm wide |
| Stacked lockup | 64 px wide | 18 mm wide |

Below 24 px, use the symbol alone.

## 4. Colour

| Name | HEX | RGB | CMYK, approximate | Pantone, approximate | Use |
| --- | --- | --- | --- | --- | --- |
| Ink | `#141414` | 20, 20, 20 | 0, 0, 0, 92 | Black 6 C | The logo on light backgrounds |
| Paper | `#F4F2EC` | 244, 242, 236 | 0, 1, 3, 4 | Print as the paper stock | Light backgrounds, and the logo on Ink |
| Signal | `#F04E23` | 240, 78, 35 | 0, 68, 85, 6 | 172 C | The icon tile, and one accent at a time |

Approved pairings and their contrast ratios on the WCAG scale, higher is more legible:

- Ink on Paper, 16.5 to 1. The default.
- Paper or white on Ink, 16.5 to 1. The reversed version uses the thinned symbol file.
- Ink on Signal, 5.1 to 1. The app and plugin icon.
- Signal on Paper, 3.2 to 1. Large sizes only, 48 px and up.

Verify the Pantone and CMYK values against a physical guide before print.

## 5. Typography

The wordmark is JetBrains Mono Bold, licensed under the SIL Open Font License 1.1, which permits use in logos. The wordmark files contain outlines, so no font install is needed to reproduce them. For text next to the logo, use JetBrains Mono for code and labels, and the platform's default sans-serif for everything else.

## 6. Do not

- Do not rotate the symbol. It points right.
- Do not round the tip or the blade ends.
- Do not add a gradient, a shadow, or an outline.
- Do not place the Ink symbol on Ink, or the white symbol on Paper.
- Do not reset the wordmark in a live font or change the hyphen back to a plain dash.
- Do not stretch either lockup. Scale both axes together.

## 7. Provenance

Designed 2026-10-25. The symbol is a single six-point path with 30 degree outer edges and 15 degree inner edges, shifted 9 units right of geometric centre for optical balance. No trademark search has been run. Run a trademark search and a reverse-image search before wide commercial use.
