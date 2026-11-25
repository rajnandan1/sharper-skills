---
name: sharper-skills
description: An editor's proof on paper. Typed requests, red pencil marks, one copy action.
colors:
  signal: "#F04E23"
  signal-hover: "#F2643E"
  signal-press: "#E0461C"
  pencil: "#B3360F"
  ink: "#141414"
  paper: "#F4F2EC"
  muted: "#565B63"
  label-graphite: "#3A3E42"
  rule: "#DDD8CF"
  field-stroke: "#C9C4BA"
typography:
  display:
    fontFamily: "JetBrains Mono, ui-monospace, monospace"
    fontSize: "46px"
    fontWeight: 700
    lineHeight: 1.08
    letterSpacing: "-0.01em"
  headline:
    fontFamily: "JetBrains Mono, ui-monospace, monospace"
    fontSize: "26px"
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: "-0.005em"
  title:
    fontFamily: "JetBrains Mono, ui-monospace, monospace"
    fontSize: "19px"
    fontWeight: 600
    lineHeight: 1.3
  typed:
    fontFamily: "JetBrains Mono, ui-monospace, monospace"
    fontSize: "18px"
    fontWeight: 400
    lineHeight: 1.5
  body-lead:
    fontFamily: "system-ui, -apple-system, Segoe UI, Roboto, Helvetica Neue, Arial, sans-serif"
    fontSize: "18px"
    fontWeight: 400
    lineHeight: 1.45
  body:
    fontFamily: "system-ui, -apple-system, Segoe UI, Roboto, Helvetica Neue, Arial, sans-serif"
    fontSize: "17px"
    fontWeight: 400
    lineHeight: 1.5
  command:
    fontFamily: "JetBrains Mono, ui-monospace, monospace"
    fontSize: "16px"
    fontWeight: 500
    lineHeight: 1
  label:
    fontFamily: "JetBrains Mono, ui-monospace, monospace"
    fontSize: "14px"
    fontWeight: 400
    lineHeight: 1.4
  hand:
    fontFamily: "Caveat, cursive"
    fontSize: "23px"
    fontWeight: 500
    lineHeight: 1.3
rounded:
  focus: "2px"
  field: "8px"
spacing:
  stack-sm: "10px"
  stack-md: "14px"
  stack-lg: "22px"
  stack-xl: "28px"
  gutter-sm: "20px"
  gutter-md: "40px"
  section: "72px"
components:
  install-field:
    backgroundColor: "rgba(255,255,255,0.35)"
    textColor: "{colors.ink}"
    typography: "{typography.command}"
    rounded: "{rounded.field}"
    padding: "0 16px"
    height: "52px"
  copy-button:
    backgroundColor: "{colors.signal}"
    textColor: "{colors.ink}"
    rounded: "{rounded.field}"
    padding: "0 18px"
    height: "52px"
  copy-button-hover:
    backgroundColor: "{colors.signal-hover}"
    textColor: "{colors.ink}"
  copy-button-active:
    backgroundColor: "{colors.signal-press}"
    textColor: "{colors.ink}"
  nav-link:
    textColor: "{colors.ink}"
    padding: "10px 0"
  skill-entry:
    textColor: "{colors.ink}"
    typography: "{typography.title}"
  slip-label:
    textColor: "{colors.label-graphite}"
    typography: "{typography.label}"
  margin-note:
    textColor: "{colors.pencil}"
    typography: "{typography.hand}"
---

# Design System: sharper-skills

## Overview

This is the design system of the sharper-skills landing page, `site/index.html`. Source files: styles in `site/styles.css`, raster plates (the paper sheet, the pencil, the paper texture and the logo) in `site/assets/plates/`, fonts in `site/assets/fonts/`, brand files and rules in `brand/` and `brand/GUIDELINES.md`. "The approved comp" means the mock the user approved, `.impeccable/mocks/decision/model-pick.png`; "comp units" are pixels of that 1536 px wide mock, set as `--u: 100vw / 1536`. A "plate" is a raster image the page places as a whole.


**Creative North Star: "The Editor's Proof"**

Every surface is a proof sheet that an editor has worked over. The request arrives typed, in a monospace face on warm paper, and an editor's red pencil marks it until it says what was meant: a word struck through, a word underlined, a caret where something goes in, a figure circled, a short note in the margin with a drawn arrow. The explanation around the proof is set in the platform's plain sans, so the reader can tell at a glance what was typed and what is being said about it.

Density is low and reading-led. Content sits in vertical order on one paper ground, with no enclosed boxes. Groups are separated by a single ruled line, lists are numbered entries in a style sheet, and evidence is shown as typed slips with the editor's marks on them. Colour is almost absent: ink on paper, with one red-orange used only by the pencil and by the one action the page exists for, the copy button.

The world rejects the category default for developer tools: a centred headline over a grid of identical feature cards with an icon in each. It is flat paper, not a glossy product UI.

**Key Characteristics:**
- Warm paper ground with a fine paper texture, and near-black ink type.
- Monospace for everything typed (headings, commands, skill names, labels); plain sans for explanation.
- One accent, Signal, kept for pencil marks and the copy action.
- Handwritten margin notes in a deeper Red Pencil, set in Caveat and tilted a few degrees.
- No cards, no shadows, no icons. Structure comes from ruled lines and numbering. The one exception is the copy glyph on the hero Copy button: an authored two-page SVG drawn in the button's ink, kept because the approved comp shows it.

## Colors

A two-ink palette: ink and paper carry the page, and one red-orange marks it.

### Primary
- **Signal Red-Orange**: the editor's pencil stroke and the copy action. It draws the strike-through, the underline, the caret, the circle round a figure and the margin arrows, and it fills the Copy button. The button lifts to **Signal, Lifted** on hover and darkens to **Signal, Pressed** when pressed.

### Secondary
- **Red Pencil**: the handwritten words of the margin notes, the rejection note on an evidence slip and the circled figure's text. It is Signal taken darker so that handwriting reads on Paper (5.4 to 1 on the WCAG contrast scale, higher is more legible).

### Neutral
- **Ink**: all type, the focus ring and the text on the Copy button (Ink on Signal is a brand pairing, 5.1 to 1).
- **Paper**: the page ground, always with the paper texture plate tiled over it, and the `theme-color`.
- **Graphite** (`muted`): secondary sans text: the subhead, section intros, skill descriptions, sources and the footer (6.1 to 1 on Paper).
- **Typewriter Graphite**: the small monospace labels on the proof sheet and on evidence slips, and table headers.
- **Ruled Line**: the 1 px rule above the footer and under the hero.
- **Field Stroke**: the 1 px border of the install command field.

### Named Rules
**The Pencil Only Rule.** Signal is never body text, never a background panel and never decoration. It appears as a pencil mark or as the Copy button, nowhere else. As text on Paper it is allowed only at 48 px and up (brand rule, 3.2 to 1).

**The Two Inks Rule.** On a marked-up item, the stroke is Signal and the handwriting is Red Pencil. Do not swap them.

## Typography

**Display Font:** JetBrains Mono (with ui-monospace, monospace), self-hosted, variable weight 100 to 800
**Body Font:** the platform sans (system-ui, -apple-system, Segoe UI, Roboto, Helvetica Neue, Arial)
**Hand Font:** Caveat (with cursive), self-hosted, weight 400 to 700

**Character:** The monospace is the typewriter of the proof: anything a person types or an agent reads is set in it. The sans is the editor's plain voice that explains. Caveat is the pencil, and it appears only as marks on the proof.

### Hierarchy
- **Display** (JetBrains Mono 700, clamp 28 px to 46 px, line height 1.08): the one hero headline, balanced over two lines.
- **Headline** (JetBrains Mono 700, 26 px, line height 1.2): section headings, written as short sentences that end with a full stop ("Install.", "Sources.").
- **Title** (JetBrains Mono 600, 19 px, line height 1.3): a skill's name in the numbered list.
- **Typed** (JetBrains Mono 400, 18 px, line height 1.5): typed text on an evidence slip, the text that carries the marks.
- **Command** (JetBrains Mono 500, 16 px, line height 1): the install command in its field.
- **Body Lead** (sans 400, 18 px, line height 1.45, at most 40ch): the hero subhead.
- **Body** (sans 400, 16 px to 17 px, line height 1.5, 58ch to 64ch): explanation, intros and install steps.
- **Label** (JetBrains Mono 400, 14 px, line height 1.4): slip labels, table headers and the skill names after each source.
- **Hand** (Caveat 500, 23 px, line height 1.3): margin notes and rejection notes. On the proof sheet the notes scale with the sheet in container units.

### Named Rules
**The Typed Versus Said Rule.** If a reader could paste it, type it or run it, it is monospace. If it explains, it is sans. Commands and skill names inside sans sentences are inline `code` in the monospace at 0.9em.

**The Pencil Hand Rule.** Caveat appears only as a note written on a typed item. It never sets a heading, a button or body text.

## Layout

Mobile first, one column, left-aligned throughout. Page gutters are 20 px below 720 px, 40 px from 720 px, and 84 comp units at 1100 px and up. Sections sit 72 px apart (110 px above the evidence section on desktop), and the footer sits 80 px below the last section. Inside a section the stack steps are 10 px, 14 px, 22 px and 28 px.

From 720 px the skill list goes to two columns with a 48 px column gap, and the evidence slips go to two columns with a 28 px gap. At 1100 px the evidence gap widens to 56 px, and the skill list becomes a fixed four-row, two-column grid with no gaps. At 1100 px and up the hero is an absolute composition measured from the approved comp in units of 100vw / 1536 (`--u`), with the proof sheet at the right edge and a ruled line under the left part of the hero; below 1100 px the hero falls back to a normal grid stack. Install and Sources share a row on desktop. Below 560 px the install command field and its Copy button stack vertically.

Line lengths stay short: 40ch for the subhead, 58ch to 64ch for body paragraphs.

## Elevation & Depth

The system is flat. No element has a box-shadow, a gradient or a blur. Depth comes only from raster plates: the paper texture tiled on the page, and on the hero a photographed paper sheet with a pencil lying at its edge. Everything that is not a plate lies flat on the paper.

### Named Rules
**The Flat Paper Rule.** If an element needs to stand out, give it a ruled line, a number or a pencil mark, never a shadow or a raised surface.

## Shapes

Corners are square by default. The only rounded shape is the install command group: the field and the Copy button join into one 8 px rounded bar, with the field holding the left corners and the button the right. The focus ring has a 2 px radius. The circle round a figure is a deliberately uneven hand-drawn ellipse, tilted by 3 degrees. Strike-throughs and underlines are wavy hand strokes, not CSS text decoration. Margin notes tilt 4 to 10 degrees. Slips are open at the sides: only a 1 px top rule marks where one begins.

## Components

### Buttons
The page has one button: **Copy**, paired with the install command it copies.
- **Shape:** the right half of the 8 px rounded install bar.
- **Primary:** Signal fill with Ink text, sans 500 at 20 px (18 px in the install steps), 52 px tall (46 px in the install steps), at least 104 px wide.
- **Hover / Focus:** Signal, Lifted on hover; Signal, Pressed and a 1 px downward shift when pressed; the global 2 px Ink focus ring with a 3 px offset. The fill colour change takes 120 ms ease-out, and only when the user allows motion.
- **States:** the label changes to "Copied" for 2.4 s. If the clipboard fails, the command is selected and the label says "Press Ctrl+C". A live status line under the hero bar repeats the result in words.

### Inputs / Fields
- **Style:** the install command as a read-only field: JetBrains Mono 500 at 16 px (14 px in the install steps, 12 px to 12.5 px on phones), Ink text on a 35% white wash over the paper, 1 px Field Stroke border with no right border, so it joins the button.
- **Focus:** the 2 px Ink ring, drawn inside the field (offset −2 px).

### Navigation
- **Style:** four plain sans text links in a row (16 px on phones, 18 comp units on desktop), no underline at rest, underline on hover, 10 px vertical padding for the touch target. No active state and no menu: the page is one sheet.

### Numbered Skill Entry
- An ordered list where each entry is a mono counter ("1.") in a narrow first column, the skill name in Title type, and one Graphite sans line under it. No box, no icon, no divider.

### Evidence Slip (signature)
- A typed slip open at the sides with a 1 px top rule. It starts with a Label line that says where the item comes from, then the typed item in Typed style. A rejected line is struck through in Signal and followed by a Hand note in Red Pencil. Tables inside a slip have a 1 px solid rule under the header and dashed rules between rows, with figures right-aligned. A figure that matters is circled in Signal.

### Marked-up Proof Sheet (signature)
- The hero plate: a raster paper sheet with live HTML text placed on it in container units. A Label line, a struck typed task, then the rewritten prompt in monospace with underlines and carets, and margin notes with hand-drawn arrows. The notes and carets pencil in one after another (520 ms each, `cubic-bezier(0.16, 1, 0.3, 1)`, from 350 ms to 1040 ms), only when the user allows motion. A caption under the sheet says what the example is.

## Do's and Don'ts

### Do:
- **Do** set every typed or runnable thing in JetBrains Mono and every explanation in the platform sans.
- **Do** keep Signal to pencil marks (strike, underline, caret, circle, arrow) and the Copy button.
- **Do** write handwritten notes in Red Pencil Caveat, tilted 4 to 10 degrees, next to the item they mark.
- **Do** separate groups with a 1 px rule and order lists with numbers.
- **Do** keep the paper texture on the page ground.
- **Do** pair every install command with a Copy button that confirms in words.
- **Do** gate every animation behind `prefers-reduced-motion: no-preference`.

### Don't:
- **Don't** build a grid of feature cards, or enclose content groups (skills, slips, sources) in boxes with borders, fills or shadows. The install bar is the one stroked and washed element, because it is a field.
- **Don't** add icon glyphs beyond the hero copy glyph. An arrow on the proof is a pencil stroke inside a margin note, not an icon.
- **Don't** use Signal as running text on Paper below 48 px, or as a background panel.
- **Don't** add shadows, gradients or glows to any element or to the logo.
- **Don't** rotate, recolour, stretch or re-set the logo in a live font; use the files in `brand/`.
- **Don't** use Caveat for headings, buttons or body text.
