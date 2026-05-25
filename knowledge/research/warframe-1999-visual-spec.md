---
Researcher: Augur 🔮
Date: 2026-05-25
Subject: Warframe 1999 (Höllvania) visual design language — translation spec for ducat-lens
Evidence tiers: Tier 1 (official DE), Tier 2 (wiki), Tier 3 (dev interviews), Tier 4 (community)
---

# Warframe 1999 Visual Design Language — ducat-lens Spec

Brief for Lumen ✨ (Visual Director). Authored by Augur 🔮 (Senior Research Analyst). Source materials cross-referenced from official Digital Extremes posts, Warframe Wiki, art-team interviews (Creative Bloq, Dexerto, ArtStation), and 1999 ARG documentation.

---

## 1. Color Palette

**Evidence quality:** Medium. Directional colors well-documented; exact in-game hex values not publicly extractable without datamining.

### Backgrounds

- **Primary background**: `#0d0f14` to `#12151c` — deep near-black with cool blue-grey undertone. Höllvania uses raised black levels (forum bug thread); anime cinematic uses "semi-monochromatic" desaturation.
- **Secondary surfaces/panels**: `#1a1d26` to `#22253a` — desaturated cool charcoal.
- **Pom-2 chrome (windowed UI)**: `#b0b8c8` — Windows-era mid-grey (Fact: Pom-2 wiki).

### Neon accents — confirmed zone color script

Art Director Simon Dumonceau (Creative Bloq interview) explicitly names two zone color families:

| Zone | Color family | Hex approximation |
|---|---|---|
| Underground / Techrot tunnels | Desaturated greens + greys | base `#3a5c3a`, hotspots `#5dff6a` / `#4cde5a` |
| Mall / street level | Cold pinks + blues | pink `#e05090` → `#ff4d9b`; blue-teal `#3fc8e0` → `#00d4ff` |

- **Efervon chemical (Scaldra faction)** = bright green `#5dff6a` — "green pillars of light," "green-tinted tanks" (Fact: Höllvania wiki + farming guide). Functions as **hazard/warning** color in-world.
- **Techrot cyst** = yellow `#d4b820` (Fact: forum observation). Viable as **infected/corrupt** accent.

### Orokin gold presence in 1999

Minimal — Orokin gold is the pre-history aesthetic; 1999 deliberately contrasts. Only confirmed carry-over:
- **KIM messenger interface**: golden gradient `#c8a84b` → `#f0d060` for **favorable dialogue / Hex approval** (Fact: KIM wiki).
- **Devil's Triad gradient**: red `#e03030` for hostile dialogue choices.

### Text colors

- Primary: `#e8eaf0` (near-white)
- Secondary: `#8a9ab0` (muted cool grey)
- Muted/metadata: `#6e7e9c` (corrected from initial `#4a5568` — original failed WCAG AA at 3.0:1; current value clears ~4.75:1 on `#0d0f14`)
- Terminal/monospace: phosphor green `#4cde5a` on black (CRT monitor aesthetic)

### Status palette (derived from in-world faction colors)

| State | Color | Derivation |
|---|---|---|
| Success / positive | `#c8a84b` → `#f0d060` | KIM golden gradient (Hex approval) |
| Warning | `#5dff6a` | Efervon hazard chemical |
| Error / hostile | `#e03030` | Devil's Triad red |
| Neutral info | `#3fc8e0` | Mall zone cold blue |
| Infected / unknown | `#d4b820` | Techrot cyst yellow |

---

## 2. Typography

**Evidence quality:** Medium. Game fonts confirmed; 1999-specific UI font not confirmed as distinct from base game.

### Confirmed in-game fonts (Warframe Fonts wiki)

- **Ailerons** — condensed geometric display typeface, primary heading font. Free at designer's site.
- **Roboto (2013 vintage)** — general UI body text.
- **Flareserif 821 BT** (Albertus-based) — serif accent.
- **Noto Sans** — CJK fallback.

### 1999-specific typography hypothesis

ARG used monospaced terminal fonts (DE-OS desktop, TypeFlyte.app). Community requested "7-segment display inspired typeface" for unofficial 1999 theme (forum). No official 1999-specific UI font shipped.

### Recommendation for ducat-lens

| Tier | Font | Use |
|---|---|---|
| Headers | Barlow Condensed Bold/ExtraBold OR Rajdhani Bold | H1/H2/H3, panel titles, button labels |
| Data/tables | IBM Plex Mono OR Share Tech Mono | Item names, ducat values, code-style data |
| Body | Roboto (exact Warframe match) | Paragraphs, labels |
| Retro terminal | VT323 (Google Fonts) | KIM-style dialogue if used |

All Google Fonts — free, no licensing risk.

---

## 3. Panel and Border Treatment

**Evidence quality:** Medium-low. ARG visual confirmed; in-game HUD border style not directly documented.

### Confirmed elements

- **warframe.com/1999** website uses bracket/symbol separators: `;\]`, `</>`, `:@` — ASCII/code-style, not Orokin filigree (Fact: official site).
- **DE-OS desktop (ARG)**: windowed UI with title bars, close/minimize buttons — Windows 3.1 / early Windows mimicry.
- **Pom-2 interface**: icon toolbars, folder-and-file paradigm, standard dialog boxes.
- **KIM interface**: notification banners with `!` symbols, lock icons, clock icons — flat, functional icon language.

### Derived pattern for ducat-lens panels

- Corner bracket motifs via ASCII box-drawing (`⌐ ¬ └ ┘`) — period-correct, NOT curved Orokin filigree
- 1px or 2px border in desaturated neon accent (no thick ornate borders)
- Inset scanline texture at 5–8% opacity to suggest CRT glass
- No rivets / bolts (that's Grineer, not 1999)
- Subtle outer glow matching panel's zone accent: cold blue for UI chrome, green for data/tech contexts

---

## 4. Texture and Effects

**Evidence quality:** Medium. Confirmed from multiple production sources.

### Confirmed

- **Film grain**: Creative Bloq quote — "Desaturate, desaturate, throw some light bloom on it and grain." Period-authenticity tool.
- **Light bloom**: heavy around neon sources; Physically Based Lighting workflow.
- **Subsurface scattering / cold glow**: translates to web as `box-shadow` / `filter: drop-shadow` on neon-lit elements.
- **Desaturation**: backgrounds NOT fully saturated neons; neons reserved for accent highlights only.
- **CRT monitors / retro tech**: organic throughout Techrot zones; subtle CRT scanline overlay at 3–6% opacity on certain elements (NOT full-page).
- **Volumetric fog**: heavy environment fog. Web: subtle radial gradient dark-edge → lighter-center.

### Hypothesis (partial evidence)

- Glitch / chromatic aberration artifacts (ARG used "glitched Unicode characters"; Pom-2 sky has chromatic effect). Suggests occasional aberration on hover/error states.

### NOT confirmed

- Full-screen scanline overlays. Common in retro web design but not specifically documented as 1999 UI element. **Use low-intensity, panel-scoped only.**

---

## 5. Iconography

**Evidence quality:** Medium. ARG and KIM interface best documented.

### Confirmed icons (KIM wiki + ARG wiki)

- **Gear** (settings), **envelope** (email), **clock** (history), **lock** (locked content), **`!` banner** (notification), **red no-entry** (unavailable)
- DE-OS uses: **folder**, **application** icons (.app extensions) with period-appropriate boxy styling
- **Entrati eye motif** appears in ASCII art

### Style verdict

**Flat functional symbols** with slight terminal/technical personality. Lucide or Feather icons (modern equivalent), NOT illustrated or pixel-art icons. Monochrome or single-color-filled, sized small, paired with text labels.

---

## 6. Motion Patterns

**Evidence quality:** Low-medium. Indirect evidence from environmental descriptions + Warframe UI patterns.

### Confirmed

- **Flickering lights** in Höllvania environment description
- Warframe UI uses animated transitions broadly (forum confirmation)
- Pom-2 has **boot sequences** — load/initialization animation pattern

### Inferred (Hypothesis, period-accurate)

- Text appearing character-by-character (typewriter) — consistent with AIM/terminal aesthetic
- Screen-in sweep (horizontal scan line top → bottom on load) — late-90s OS aesthetic
- Cursor blink on focused inputs
- Flicker-on-hover for neon-lit elements (brief luminance pulse)

### NOT confirmed

- Auto-scroll / looping scan lines across full viewport

---

## 7. 1999 vs Standard Warframe Aesthetic

**Evidence quality:** High. Well-documented across developer interviews.

| Dimension | Standard Warframe (Orokin/Tenno) | Warframe 1999 |
|---|---|---|
| Background | Deep space black + cool blue-teal | Warmer near-black with cool blue-grey; raised blacks |
| Accent | Orokin gold, white filigree, Energy blue | Efervon green, cold pink/blue, desaturated grey-green |
| Architecture | Curved organic-geometric Orokin; Lotus motifs | Gothic Central/Eastern European brutalism; derelict mall; Soviet-military; CRT terminals |
| Typography | Same Ailerons + Roboto, "divine empire" framing | Same fonts, recontextualized as late-90s corporate/consumer |
| Panels | Ornate curved borders, golden inlays, energy-field glows | ASCII bracket corners, Windows-chrome panels, inset lines |
| Texture | Smooth polished Orokin surfaces | Film grain, bloom, desaturation, CRT glass, industrial decay |
| Motion | Smooth holographic animations | Boot sequences, typewriter, flicker, scan sweeps |
| Icons | Organic Lotus-derived glyphs | Flat functional symbols |
| Register | Alien transcendence, power, mystery | Nostalgia, decay, punk resistance, human warmth |
| Faction colors | Orokin gold/white; Grineer red-orange; Corpus blue-white | Scaldra olive-grey + Efervon green; Techrot yellow + bio-mech horror |

**Key finding (Fact: Fandomwire + Dexerto)**: Design team explicitly intended 1999 to feel "outside the game" while retaining Warframe essence. Visual references: Ghost in the Shell + Blade + Metal Gear Solid, NOT the usual Mass Effect-adjacent space opera.

---

## 8. Design Translation — ducat-lens

Three primary surfaces: (1) upload area, (2) results table, (3) status indicators.

### Global shell

- Background: `#0d0f14` (near-black, cool blue cast)
- Surfaces/cards: `#1a1d26`
- 3–5% opacity scanline overlay (CSS `repeating-linear-gradient`, 2px lines, 50/50 dark pattern) on **card backgrounds only**, NOT full viewport
- Subtle radial vignette (dark edges → lighter center) — "foggy underground" atmosphere
- Film grain: SVG noise overlay at 4% opacity on `body`

### Typography stack

- Headings: Barlow Condensed Bold / Rajdhani Bold, `letter-spacing: 0.05em`
- Data/results: IBM Plex Mono
- Labels/secondary: Roboto

### Upload zone

- Dark panel `#1a1d26`, 1px border `#3fc8e0` (cold blue, mall zone accent)
- Corner bracket motifs via CSS `::before` / `::after` with ASCII box-drawing (`⌐ ¬ └ ┘`) in `#3fc8e0`
- Hover: `box-shadow: 0 0 12px rgba(63, 200, 224, 0.6)` (cold blue phosphor glow)
- Upload icon: flat monochrome arrow-up (Lucide/Feather)
- Text: `#e8eaf0`, Rajdhani Bold

### Results table

- Row stripe: alternating `#0d0f14` and `#14172a` — very subtle, NOT high contrast
- Column headers: Barlow Condensed, `#3fc8e0`, tracked
- **Ducat value column**: IBM Plex Mono, value in Orokin gold `#c8a84b` — the one place gold is earned back (ducats are literally Orokin currency)
- High-value rows (sell): `#5dff6a` left border (2px) + muted green row tint
- Low-value rows (keep/skip): no accent or muted grey
- Sort/filter icons: flat Lucide, `#8a9ab0`

### Status indicators

| State | Color | CSS pattern |
|---|---|---|
| Processing / analyzing | `#3fc8e0` with pulse | Spinner or scan-sweep bar |
| Success / item found | `#c8a84b` | Border + icon tint |
| Warning / low confidence | `#5dff6a` | Icon + text |
| Error / failed | `#e03030` | Border + message |
| Infected / unknown | `#d4b820` | Rare; "unknown item" states |

### Motion rules

- Standard interactions: `transition: all 0.15s ease-out` — fast, snappy, period-accurate
- Results load: 2px `#3fc8e0` scan line top → bottom over 0.4s via `@keyframes transform` — "data scan complete"
- Hover on neon-accented elements: 80ms two-step opacity flicker (`1.0 → 0.7 → 1.0`)
- NO parallax, NO entrance animations over 0.3s

### Forbidden

- Orokin filigree borders (curved, golden, ornate) — pre-1999 Warframe
- Heavily saturated full-page neon backgrounds — palette is desaturated by design
- `border-radius` above `4px` — period UI was boxy
- Smooth cubic-bezier easing on every element — reserve smooth easing for scan sweep only
- Full-viewport CRT scanline overlay — period-accurate only for specific terminal/Pom-2-style panels

---

## 9. Logo

Locked: `frontend/public/logo.svg` — Orokin ducat 4-point star (`#c8a84b`) inside cold-blue lens reticle (`#3fc8e0`) with 1999 ASCII corner brackets. Scales favicon → header.

---

## 10. Gaps

| Gap | Impact | How to close |
|---|---|---|
| Exact hex values for in-game neon accents | High — all hex approximations | Game capture + color picker; community datamining repos |
| Whether dedicated "1999" UI theme ships as game option | Medium | Check Interface options post Update 38.5 |
| Hex Protoframe suit exact colors | Low-medium | ArtStation pages (403'd during research) |
| In-game HUD border treatment for 1999 missions | Medium | Direct game capture of Höllvania missions |
| Motion animation spec (flicker timing, scan sweep duration) | Low — approximated | Video frame-analysis of Pom-2 startup sequence |
| Techrot organic color (amber-orange vs yellow-green) | Medium — warning/corrupt state | Direct game capture of Techrot creatures |

---

## 11. Sources

### Tier 1 — Official Digital Extremes

- [warframe.com/en/1999](https://www.warframe.com/en/1999)
- [warframe.com/en/1999/atomicycle](https://www.warframe.com/en/1999/atomicycle)
- [warframe.com — Update 38 patch notes](https://www.warframe.com/en/patch-notes/pc/38-0-0)

### Tier 2 — Warframe Wiki

- [Höllvania](https://wiki.warframe.com/w/H%C3%B6llvania)
- [Kinemantik Instant Messenger](https://wiki.warframe.com/w/Kinemantik_Instant_Messenger)
- [Fonts](https://wiki.warframe.com/w/Fonts)
- [Pom-2](https://wiki.warframe.com/w/Pom-2)
- [1999 ARG](https://wiki.warframe.com/w/1999_ARG)
- [Settings/Interface/Backgrounds and Themes](https://wiki.warframe.com/w/Settings/Interface/Backgrounds_and_Themes)

### Tier 3 — Dev interviews / production

- [Creative Bloq — THE LINE anime short](https://www.creativebloq.com/3d/3d-animation/how-arthouse-studio-the-line-drew-on-warframe-1999s-unapologetic-stylishness-for-its-anime-short)
- [Dexerto — Höllvania setting](https://www.dexerto.com/gaming/warframe-team-explain-the-inspiration-behind-1999s-hollvania-setting-2978936/)
- [Irrational Passions — Warframe 1999 review](https://irrationalpassions.com/warframe-1999-makes-the-turn-of-the-century-a-nightmare-and-a-love-story/)
- [Orokin Archives — ARG documentation](https://www.orokinarchives.com/arg-1999/)
- [ArtStation — DE Warframe 1999 art blast](https://magazine.artstation.com/2025/02/digital-extremes-warframe-1999/)
- [Fandomwire — 1999 aesthetic overview](https://fandomwire.com/helped-to-keep-the-game-fresh-warframes-1999-update-was-a-huge-change-in-tone-but-it-still-retained-the-essence-of-the-game/)

### Tier 4 — Community

- [Warframe Forums — 1999 UI theme community request](https://forums.warframe.com/topic/1406700-1999-ui-theme/)
