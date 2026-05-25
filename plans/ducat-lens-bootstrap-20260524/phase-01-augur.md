# Phase 01 — Research: free OCR/vision + Warframe ducat API

## Owner

Augur 🔮 (Senior Research Analyst)

## Pre

- User confirmed: ducat values only, free vision solution, no auth, no DB
- Test image at `D:/projects/ducat-lens/image.png` (Warframe Ducat Kiosk screenshot, ornate gold-on-dark UI)

## Reads

- `D:/projects/ducat-lens/image.png` — visual reference for OCR difficulty assessment
- Web (WebSearch + WebFetch) — for vision libs and Warframe APIs

## Writes

- `D:/projects/ducat-lens/plans/ducat-lens-bootstrap-20260524/_research-vision.md`
- `D:/projects/ducat-lens/plans/ducat-lens-bootstrap-20260524/_research-ducat-api.md`

## Steps

1. **Vision research** — investigate FREE options for detecting Warframe Prime part names from screenshots:
   - Tesseract (pytesseract) — baseline, likely poor on stylized font
   - EasyOCR — PyTorch-based, better on stylized text, ~64MB models, free
   - PaddleOCR — alternative, better Latin script accuracy, free
   - RapidOCR (ONNX) — lightweight, no PyTorch dep
   - Image-template matching against known Prime part icon library (no OCR — match item icons directly via OpenCV `cv2.matchTemplate` or perceptual hashing). Note: Warframe community maintains icon dumps.
   - Free vision LLM tier: Google Gemini 1.5 Flash free tier (15 RPM, 1500 RPD), Groq vision models
   For each: pros, cons, install size, accuracy expectation on stylized Warframe font, license, offline-capable yes/no. Rank top 3.
2. **Ducat API research** — confirm authoritative source for ducat values per Prime part:
   - Check if Digital Extremes (Warframe maker) exposes any official public API — search `developers.warframe.com`, `api.warframe.com`
   - Warframe Community Developers (`api.warframestat.us`) — check `/items` endpoint for ducat field
   - Warframe.market (`api.warframe.market/v1/items` + `/items/{slug}`) — known to return `ducats` field
   - Wiki dump (warframe.fandom.com) — fallback scrape
   For each: endpoint URL, response shape, rate limits, requires auth yes/no, license/terms, sample JSON. Pick primary + fallback.
3. Cite every source with URL + access date.
4. Hypothesis label every claim per Evidence discipline: Fact / Hypothesis / no Assumption.

## Output

`_research-vision.md` schema:
```
# Free vision options for ducat-lens
## Ranked
1. <lib> — accuracy / install / offline / license / sample code stub
2. ...
## Discarded
- <lib> — why
## Sources
- <url> (accessed 2026-05-24)
```

`_research-ducat-api.md` schema:
```
# Ducat data sources
## Primary recommendation
<API> — endpoint, auth, rate limits, sample response
## Fallback
<API> — same
## Discarded
- <source> — why
## Sources
- <url>
```

## Gate

- Both files exist
- Each vision option has explicit accuracy expectation for Warframe stylized font (Fact or labeled Hypothesis)
- Ducat API recommendation includes one working sample request returning a real ducat value
- Zero unsourced claims

## Abort conditions

- No free vision option produces ≥50% expected accuracy on stylized Warframe font → escalate to Cipher 🔓 to widen scope (paid tier, manual entry fallback)
- No public ducat API exists → escalate; consider bundled static JSON from wiki

## MCP whitelist/blacklist

- Allowed: WebSearch, WebFetch, Read, Glob, Grep, Write
- Forbidden: Edit (research is read-only output to its own artifact files)
