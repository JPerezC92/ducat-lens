# CRT duotone — implementation snippets

Sibling artifact for `phase-01-forge.md`. Forge copies these blocks verbatim into the target files.

## Snippet A — append to `frontend/src/styles/global.css` inside `@layer utilities`

```css
.crt-duotone {
  position: relative;
  display: block;
  overflow: hidden;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  background: var(--color-bg);
}
.crt-duotone > img {
  display: block;
  width: 100%;
  height: auto;
  filter: grayscale(1) sepia(1) hue-rotate(160deg) saturate(2.5) contrast(1.1) brightness(0.85);
}
.crt-duotone::after {
  content: "";
  position: absolute;
  inset: 0;
  background: repeating-linear-gradient(
    to bottom,
    rgba(63, 200, 224, 0.12) 0px,
    rgba(63, 200, 224, 0.12) 1px,
    transparent 1px,
    transparent 2px
  );
  mix-blend-mode: overlay;
  pointer-events: none;
}
@media (prefers-reduced-motion: reduce) {
  .crt-duotone::after { opacity: 0.6; }
}
```

## Snippet B — hero figure (insert above existing H1 row in `frontend/src/pages/index.astro`)

```astro
<figure class="crt-duotone w-full max-w-lg mx-auto">
  <img
    src="/images/hero-prime.png"
    alt="Stylized Warframe Prime silhouette rendered in CRT duotone"
    width={W}
    height={H}
    loading="eager"
    fetchpriority="high"
  />
</figure>
```

Replace `W` / `H` with measured pixel dimensions printed by Snippet D (phase-01 step 3 stdout).

## Snippet C — example figure (insert at end of step-1 `<li>` in `frontend/src/pages/index.astro`)

```astro
<figure class="crt-duotone mt-3 max-w-md">
  <img
    src="/images/example-kiosk.jpg"
    alt="Example Warframe Ducat Kiosk inventory screenshot showing Prime parts"
    width={W2}
    height={H2}
    loading="lazy"
    decoding="async"
  />
</figure>
```

Replace `W2` / `H2` with measured pixel dimensions printed by Snippet D (phase-01 step 3 stdout).

## Snippet D — Pillow one-shot (run from repo root)

Use existing backend `pillow` dep — no new install. Captures dimensions + size + re-encodes example image to fit ≤ 500 KB cap.

```bash
cd backend && uv run python - <<'PY'
from PIL import Image
from pathlib import Path
import os, shutil

root = Path("..").resolve()
pub = root / "frontend" / "public" / "images"
pub.mkdir(parents=True, exist_ok=True)

# Hero — copy from temp download produced by phase-01 step 2:
#   curl -sL -o _tmp-hero.png "https://cdn.warframestat.us/img/LokiPrime.png"  (run at repo root)
hero_src = root / "_tmp-hero.png"
hero_dst = pub / "hero-prime.png"
shutil.copy(hero_src, hero_dst)
h = Image.open(hero_dst)
print(f"HERO {hero_dst.name}: {h.size[0]}x{h.size[1]} {os.path.getsize(hero_dst)} bytes")

# Example — re-encode image.png as JPEG q82 to fit ≤ 500 KB cap.
# PNG optimize alone cannot drop 676 KB source below 500 KB without lossy steps.
ex_src = root / "image.png"
ex_dst = pub / "example-kiosk.jpg"
ex = Image.open(ex_src).convert("RGB")
ex.save(ex_dst, "JPEG", quality=82, optimize=True)
print(f"EXAMPLE {ex_dst.name}: {ex.size[0]}x{ex.size[1]} {os.path.getsize(ex_dst)} bytes")
PY
```

> **Format note:** example is saved as `.jpg` (not `.png`) to land under 500 KB. Snippet C already references `/images/example-kiosk.jpg`. Hero stays PNG (needs alpha for transparent character bg).
