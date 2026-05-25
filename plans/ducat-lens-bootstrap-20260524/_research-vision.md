# Free vision options for ducat-lens

## Image analysis

The Ducat Kiosk screenshot (`image.png`) shows: dark background, ornate gold Warframe UI chrome, a grid of Prime part cards. Each card contains a 3D rendered icon + item name in **white mixed-case text** on a dark panel. The font is Warframe's custom UI typeface — stylized serifs but **not distorted, rotated, or curved**. Contrast is high (white text, dark background). Text size in the screenshot is approximately 12–16px equivalent. This is **moderately favorable** for OCR: high contrast helps, but the custom serif font and small size will challenge engines trained on standard print fonts.

Prior art: WFinfo (WFCD) and WarframePrimeHelper both use Tesseract with HSV-based color filtering + screen crop preprocessing. This confirms the OCR-on-cropped-region approach is viable; neither project evaluated EasyOCR or LLM vision.
Sources: [WFinfo GitHub](https://github.com/WFCD/WFinfo) (accessed 2026-05-24), [WarframePrimeHelper GitHub](https://github.com/donaldsa18/WarframePrimeHelper) (accessed 2026-05-24).

---

## Ranked

### 1. Google Gemini 1.5 Flash (free tier vision API)

**Accuracy expectation on Warframe font:** Fact — large multimodal LLMs are trained on diverse image corpora including game UI and achieve near-human text recognition. Hypothesis: accuracy on Warframe Ducat Kiosk text expected ≥85%, conditioned on passing the full screenshot or a cropped card region. Evidence: Gemini 1.5 Flash is a 1M-context multimodal model; free tier explicitly supports image input on all modalities. What would confirm/refute: a live test pass against `image.png` (Phase 02 deliverable).

**Install size:** Zero local install — REST API only. Zero Python ML dependencies.

**Offline-capable:** No. Requires outbound HTTPS to `generativelanguage.googleapis.com`.

**Rate limits (free tier):** 15 RPM, 1,500 RPD, 1,000,000 TPM.
Source: [Gemini free tier guide](https://pecollective.com/tools/gemini-free-tier-guide/) (accessed 2026-05-24).

**License/terms:** Google API Terms of Service. Free tier data is not used for model training per Google AI Studio terms (as of 2025). No cost for free tier.

**Auth:** Requires `GOOGLE_API_KEY` (free, no credit card required for AI Studio key).

**Sample stub:**
```python
import google.generativeai as genai, base64, pathlib

genai.configure(api_key="GOOGLE_API_KEY")
model = genai.GenerativeModel("gemini-1.5-flash")
img_bytes = pathlib.Path("image.png").read_bytes()
img_b64 = base64.b64encode(img_bytes).decode()

response = model.generate_content([
    {"inline_data": {"mime_type": "image/png", "data": img_b64}},
    "List every Prime part name visible in this Warframe Ducat Kiosk screenshot. Return a JSON array of strings."
])
print(response.text)
```

**Pros:** Highest expected accuracy on stylized fonts; zero local ML dependencies; structured JSON output via prompt; handles full-screenshot or cropped input; no GPU required.

**Cons:** External API dependency (network outage = failure); 1,500 RPD cap limits batch processing; requires API key management; no offline fallback.

---

### 2. EasyOCR

**Accuracy expectation on Warframe font:** Fact — EasyOCR outperforms Tesseract on scene text and stylized fonts (CER 0.09 vs Tesseract 0.18 on diverse image benchmark). Hypothesis: on Warframe's custom serif font with preprocessing (HSV threshold crop), expected accuracy ≥65–75%. Evidence: benchmark at [tildalice.io](https://tildalice.io/ocr-tesseract-easyocr-paddleocr-benchmark/) shows EasyOCR best on font-varied datasets; prior Warframe tools using Tesseract report acceptable accuracy on cropped text regions (same signal, weaker engine). What would confirm/refute: test pass on `image.png` with HSV-crop preprocessing.

**Install size:** ~90MB model download (CRAFT detector + CRNN recognizer); PyTorch wheel ~500–800MB additional for CPU-only build. Total environment: ~1GB.
Source: [Medium EasyOCR guide](https://medium.com/@adityamahajan.work/easyocr-a-comprehensive-guide-5ff1cb850168) (accessed 2026-05-24); [PyImageSearch EasyOCR](https://pyimagesearch.com/2020/09/14/getting-started-with-easyocr-for-optical-character-recognition/) (accessed 2026-05-24).

**Offline-capable:** Yes. Models download once, run locally. GPU optional (CPU mode available, slower).

**License:** Apache 2.0.

**Auth:** None.

**Sample stub:**
```python
import easyocr
reader = easyocr.Reader(["en"])  # downloads ~90MB on first run
results = reader.readtext("image.png", detail=0)  # list of strings
print(results)
```

**Pros:** Best open-source accuracy on stylized/scene text; offline; no API key; Apache 2.0; supports GPU acceleration; handles mixed fonts well.

**Cons:** Heavy PyTorch dependency (~1GB env); slower on CPU; first-run model download; not suitable for serverless cold starts.

---

### 3. RapidOCR (ONNX)

**Accuracy expectation on Warframe font:** Hypothesis — delivers PaddleOCR-level accuracy without the PaddlePaddle dependency. PaddleOCR CER is 0.10 (benchmark above), so RapidOCR expected ~similar. For Warframe's font: likely 55–70% raw accuracy, improvable with preprocessing. Evidence: RapidOCR uses PaddleOCR ONNX models (same weights, different runtime); spacing issues noted in community testing. What would confirm/refute: test pass on `image.png`.

**Install size:** ~14.9MB wheel + ONNX Runtime (~10MB). No PyTorch. Total: ~25–30MB.
Source: [rapidocr-onnxruntime PyPI](https://pypi.org/project/rapidocr-onnxruntime/) (accessed 2026-05-24).

**Offline-capable:** Yes. ONNX models bundled or downloaded once.

**License:** Apache 2.0.

**Auth:** None.

**Sample stub:**
```python
from rapidocr_onnxruntime import RapidOCR
engine = RapidOCR()
result, _ = engine("image.png")
for line in result:
    print(line[1])  # recognized text
```

**Pros:** Lightest dependency footprint (~30MB); no PyTorch; Apache 2.0; cross-platform; good for serverless/container deployment; PaddleOCR-level accuracy.

**Cons:** Spacing consistency issues reported; slightly lower expected accuracy than EasyOCR on stylized fonts; smaller community than EasyOCR; ONNX model management required.

---

## Discarded

- **Tesseract (pytesseract)** — Fact: CER 0.18 on diverse benchmark, roughly 2x worse than EasyOCR. Requires custom font training (`tesstrain`) for Warframe's typeface to reach acceptable accuracy. Training pipeline adds significant setup cost for a public web tool where ground-truth data is limited. Prior Warframe tools (WFinfo, WarframePrimeHelper) use Tesseract only with heavy HSV preprocessing and still report edge cases. Baseline accuracy on stylized fonts without training is estimated <50%. Source: [tildalice.io benchmark](https://tildalice.io/ocr-tesseract-easyocr-paddleocr-benchmark/) (accessed 2026-05-24); [Tesseract custom font guide](https://ironsoftware.com/csharp/ocr/how-to/ocr-custom-font-training/) (accessed 2026-05-24).

- **PaddleOCR** — Hypothesis: accuracy comparable to RapidOCR (same underlying models) but requires PaddlePaddle dependency (~500MB+). PaddlePaddle has had install friction on Windows and is less commonly deployed in Python web stacks. RapidOCR provides the same model weights via ONNX with a fraction of the footprint. Not discarded for accuracy reasons — discarded for dependency weight vs. RapidOCR equivalence. Source: [cisdem OCR comparison](https://www.cisdem.com/resource/open-source-ocr.html) (accessed 2026-05-24); [tildalice.io benchmark](https://tildalice.io/ocr-tesseract-easyocr-paddleocr-benchmark/) (accessed 2026-05-24).

- **OpenCV template matching / perceptual hashing against icon library** — Hypothesis: could identify items by icon image rather than text. However, Warframe Prime part icons are 3D renders that vary with lighting/zoom across game versions; no maintained Python icon dump was found. WFinfo uses OCR, not template matching, indicating the community has not found icon matching reliable enough. This approach also requires a maintained icon database keyed to item names. Evidence gap: no public Python icon library for Warframe Ducat Kiosk confirmed. What would confirm viability: finding a versioned icon dump with stable per-item hashes.

- **Groq vision (Llama 4 Scout)** — Fact: free tier 30 RPM / 1,000 RPD / 30,000 TPM. Currently in preview ("should be used for experimentation"). Lower RPD than Gemini 1.5 Flash (1,000 vs 1,500). Model is preview-quality — not production-stable for a public tool. Source: [Groq rate limits](https://console.groq.com/docs/rate-limits) (accessed 2026-05-24); [Groq vision docs](https://console.groq.com/docs/vision) (accessed 2026-05-24).

---

## Abort condition check

Ranked options 1 (Gemini) and 2 (EasyOCR) both have credible paths to ≥65% accuracy on Warframe's font, with Gemini likely exceeding 85%. Abort condition (no free option ≥50%) is NOT triggered. Phase 02 must verify with an actual test pass.

---

## Sources

- [tildalice.io OCR benchmark](https://tildalice.io/ocr-tesseract-easyocr-paddleocr-benchmark/) (accessed 2026-05-24)
- [Gemini free tier rate limits](https://pecollective.com/tools/gemini-free-tier-guide/) (accessed 2026-05-24)
- [Google AI rate limits docs](https://ai.google.dev/gemini-api/docs/rate-limits) (accessed 2026-05-24)
- [Groq rate limits](https://console.groq.com/docs/rate-limits) (accessed 2026-05-24)
- [Groq vision docs](https://console.groq.com/docs/vision) (accessed 2026-05-24)
- [rapidocr-onnxruntime PyPI](https://pypi.org/project/rapidocr-onnxruntime/) (accessed 2026-05-24)
- [RapidOCR GitHub](https://github.com/RapidAI/RapidOCR) (accessed 2026-05-24)
- [EasyOCR PyImageSearch guide](https://pyimagesearch.com/2020/09/14/getting-started-with-easyocr-for-optical-character-recognition/) (accessed 2026-05-24)
- [EasyOCR comprehensive guide](https://medium.com/@adityamahajan.work/easyocr-a-comprehensive-guide-5ff1cb850168) (accessed 2026-05-24)
- [PaddleOCR vs EasyOCR comparison](https://tildalice.io/ocr-tesseract-easyocr-paddleocr-benchmark/) (accessed 2026-05-24)
- [WFinfo GitHub](https://github.com/WFCD/WFinfo) (accessed 2026-05-24)
- [WarframePrimeHelper GitHub](https://github.com/donaldsa18/WarframePrimeHelper) (accessed 2026-05-24)
- [cisdem open-source OCR comparison](https://www.cisdem.com/resource/open-source-ocr.html) (accessed 2026-05-24)
- [Tesseract custom font training](https://ironsoftware.com/csharp/ocr/how-to/ocr-custom-font-training/) (accessed 2026-05-24)
- [OCR accuracy 2025 benchmark](https://sparkco.ai/blog/ocr-accuracy-comparison-2025-benchmark-analysis) (accessed 2026-05-24)

---

## PaddleOCR re-evaluation (2026-05-25)

### PaddleOCR (PP-OCRv5, v3.5.0)

**Accuracy on Warframe font:** Fact — PP-OCRv5 (server model) achieves a weighted-average recognition accuracy of 0.8401 across printed, vertical, handwritten, and traditional Chinese/English text, up from PP-OCRv4's 0.5735 — a 26.66 percentage-point gain. On the tildalice.io benchmark (10,000 real-world images, updated March 2026), PaddleOCR CER is 0.10, identical to the tildalice RapidOCR figure and slightly worse than EasyOCR's 0.09. In the codesota.com invoice test (April 2026), PaddleOCR scored 100% vs EasyOCR 62.5% and RapidOCR 75.0% on clean document text — but this was a structured invoice, not a stylized game UI font. Hypothesis: on Warframe's white-on-dark custom serif font, PaddleOCR PP-OCRv5 is expected to match or marginally exceed EasyOCR on clean cropped card regions, given its stronger multi-scenario training corpus and 13pp improvement over PP-OCRv4 on complex scenarios. What would confirm: a live test pass against `image.png` with PP-OCRv5 models.
Sources: [PP-OCRv5 docs](http://www.paddleocr.ai/main/en/version3.x/algorithm/PP-OCRv5/PP-OCRv5.html) (accessed 2026-05-25); [tildalice.io benchmark](https://tildalice.io/ocr-tesseract-easyocr-paddleocr-benchmark/) (accessed 2026-05-25); [codesota.com best-for-python](https://www.codesota.com/ocr/best-for-python) (accessed 2026-05-25).

**Install size:**
- `paddleocr` wheel: 120.8 KB (PyPI, v3.5.0, released 2026-04-21). Fact.
- `paddlepaddle` CPU wheel: 104.7–104.8 MB (Windows x86_64), 194.8 MB (Linux x86_64). Fact.
- Total inferred environment (paddleocr + paddlepaddle CPU + transitive deps): Hypothesis — approximately 350–600 MB, based on paddlepaddle wheel size plus numpy/opencv/Pillow/requests transitive deps typically adding 100–250 MB. Comparison: EasyOCR total ~1–1.5 GB (PyTorch CPU), RapidOCR total ~25–80 MB (ONNX Runtime). What would confirm: `pip install paddleocr --dry-run` output with sizes.
Sources: [paddleocr PyPI](https://pypi.org/project/paddleocr/) (accessed 2026-05-25); [paddlepaddle PyPI](https://pypi.org/project/paddlepaddle/#files) (accessed 2026-05-25); [codesota.com](https://www.codesota.com/ocr/best-for-python) (~500 MB claim, accessed 2026-05-25).

**Offline-capable:** Yes. All models download once, run locally. CPU mode available; GPU optional (requires separate `paddlepaddle-gpu` wheel + CUDA version matching). Fact — same model-as-local-file architecture as EasyOCR/RapidOCR.
Source: [PaddleOCR installation docs](https://github.com/PaddlePaddle/PaddleOCR/blob/main/docs/version3.x/installation.en.md) (accessed 2026-05-25).

**License:** Apache 2.0. Fact — confirmed on GitHub main branch LICENSE file and Hugging Face model cards for PP-OCRv5 and PaddleOCR-VL as of 2026.
Source: [PaddleOCR/LICENSE on GitHub](https://github.com/PaddlePaddle/PaddleOCR/blob/main/LICENSE) (accessed 2026-05-25).

**Auth:** None. No API key, no signup, no external service per request. Fully self-contained after initial model download. Fact.

**Latest version:** 3.5.0 (released 2026-04-21). Recommended install: `pip install paddleocr` which pulls PP-OCRv5 models. PaddlePaddle backend: 3.3.1 (released 2026-03-24). PaddleOCR 3.x requires PaddlePaddle 3.0+. Python 3.8–3.13 supported; Python 3.9+ required if using optional dependency groups. Fact.
Sources: [paddleocr PyPI history](https://pypi.org/project/paddleocr/#history) (accessed 2026-05-25); [PaddleOCR GitHub releases](https://github.com/PaddlePaddle/PaddleOCR/releases) (accessed 2026-05-25).

**Sample stub (10-line minimal):**
```python
from paddleocr import PaddleOCR

ocr = PaddleOCR(use_angle_cls=True, lang="en")  # downloads models on first run
result = ocr.ocr("image.png", cls=True)
texts = [line[1][0] for block in result for line in block]
print(texts)
```

**Warframe `image.png` characterization for PaddleOCR specifically:**
The test image shows a dark-background Warframe Ducat Kiosk grid. The image as viewed contains: a dark navy/black UI background; multiple Prime part card tiles arranged in a 5-column grid; each card has a 3D-rendered icon in the upper portion and white mixed-case text (item name) in the lower portion; gold ornamental UI chrome borders each card. Text size is approximately 12–16px equivalent in the screenshot. Two difficulty factors for PaddleOCR specifically: (1) The ornamental gold card borders and 3D icon renders in the same frame may trigger PaddleOCR's layout analysis to detect non-text regions as text regions — PP-OCRv5's detector is trained on dense document layouts, not sparse game-UI grids. (2) The Warframe custom serif font is not in PaddleOCR's training corpus (trained on Chinese/English print and scene text). Countervailing factor: PaddleOCR handles white-on-dark text well as of PP-OCRv5 (vertical and scene text improvements). Net assessment: Hypothesis — PaddleOCR will perform comparably to EasyOCR on preprocessed (cropped, HSV-isolated) card-text strips; raw full-screenshot accuracy may suffer from spurious detections on UI chrome. This matches the prior-art pattern (WFinfo uses HSV crop before OCR regardless of engine). Evidence gap: no live test performed.

**Pros:**
- PP-OCRv5 is the most accurate free offline OCR engine by 2026 internal benchmarks (13pp over PP-OCRv4; 0.8401 weighted accuracy).
- Smaller total footprint than EasyOCR (~500 MB vs ~1–1.5 GB).
- Apache 2.0 license; no auth; no per-request external service.
- Active development cadence (11 releases May 2025 – Apr 2026).
- Supports Python 3.8–3.13; both Windows and Linux x86_64 have pre-built CPU wheels.
- Built-in angle classification handles tilted/rotated text better than EasyOCR baseline.

**Cons:**
- PaddlePaddle is a non-standard ML framework — not PyTorch/ONNX. Adds a 105–195 MB framework wheel with no reuse if the project ever adds other ML features.
- First-run model download still required (models not bundled in wheel).
- PaddleOCR 3.x was restructured significantly from 2.x; community tutorials are split across versions; some Stack Overflow / Medium answers target 2.x API (now breaking).
- Known install friction: Python 3.8 support is partial (doc-parser group requires 3.9+); GPU install requires CUDA version pinning; dependency conflict with LangChain 1.0.0 if `paddleocr[all]` is used.
- Inference latency on CPU is the worst of the three: codesota measured 4.85s/image on Apple M-series vs RapidOCR 0.21s, EasyOCR 0.66s. Disqualifying for a backend serving a public web tool.
- Windows LTSC / WSL2 users have reported missing pre-built wheel configurations (GitHub discussion #15960, 2025–2026).
- Community is primarily Chinese-language; English documentation lags behind.

**Sources (PaddleOCR section):**
- [paddleocr PyPI v3.5.0](https://pypi.org/project/paddleocr/) (accessed 2026-05-25)
- [paddlepaddle PyPI v3.3.1 files](https://pypi.org/project/paddlepaddle/#files) (accessed 2026-05-25)
- [PaddleOCR GitHub releases](https://github.com/PaddlePaddle/PaddleOCR/releases) (accessed 2026-05-25)
- [PP-OCRv5 introduction docs](http://www.paddleocr.ai/main/en/version3.x/algorithm/PP-OCRv5/PP-OCRv5.html) (accessed 2026-05-25)
- [PP-OCRv5 arXiv paper](https://arxiv.org/abs/2603.24373) (accessed 2026-05-25)
- [tildalice.io OCR benchmark (updated 2026-03-03)](https://tildalice.io/ocr-tesseract-easyocr-paddleocr-benchmark/) (accessed 2026-05-25)
- [codesota.com best Python OCR 2026](https://www.codesota.com/ocr/best-for-python) (accessed 2026-05-25)
- [PaddleOCR installation docs (v3.x)](https://github.com/PaddlePaddle/PaddleOCR/blob/main/docs/version3.x/installation.en.md) (accessed 2026-05-25)
- [PaddleOCR/LICENSE on GitHub](https://github.com/PaddlePaddle/PaddleOCR/blob/main/LICENSE) (accessed 2026-05-25)
- [PaddleOCR GitHub discussion #15960 (install issues)](https://github.com/PaddlePaddle/PaddleOCR/discussions/15960) (accessed 2026-05-25)
- [PaddleOCR-VL license (Hugging Face)](https://huggingface.co/PaddlePaddle/PaddleOCR-VL/blob/main/LICENSE) (accessed 2026-05-25)

---

### Revised ranked table: PaddleOCR vs EasyOCR vs RapidOCR for ducat-lens

| Dimension | PaddleOCR (PP-OCRv5 v3.5.0) | EasyOCR | RapidOCR (ONNX) |
|---|---|---|---|
| **Accuracy (CER, tildalice benchmark)** | 0.10 (Fact) | 0.09 (Fact) | ~0.10 (Hypothesis, same weights as Paddle) |
| **Accuracy (structured docs, codesota)** | 100% (Fact) | 62.5% (Fact) | 75.0% (Fact) |
| **PP-OCRv5 internal weighted accuracy** | 0.8401 (Fact) | N/A | N/A (Paddle ONNX weights, older gen) |
| **Total install footprint** | ~350–600 MB (Hypothesis) | ~1–1.5 GB (Fact) | ~25–80 MB (Fact) |
| **Inference speed (CPU, per image)** | ~4.85s (Fact, Apple M-series) | ~0.66s (Fact) | ~0.21s (Fact) |
| **Offline** | Yes | Yes | Yes |
| **License** | Apache 2.0 (Fact) | Apache 2.0 (Fact) | Apache 2.0 (Fact) |
| **Auth / API key** | None | None | None |
| **Windows CPU wheel** | Yes, 104.8 MB (Fact) | Yes (via PyTorch) | Yes, ONNX Runtime |
| **Linux CPU wheel** | Yes, 194.8 MB (Fact) | Yes (via PyTorch) | Yes, ONNX Runtime |
| **Install friction** | Moderate — PaddlePaddle non-standard framework, partial Python 3.8, CUDA pinning for GPU, LangChain conflict | Low | Low |
| **Framework dependency** | PaddlePaddle (non-standard) | PyTorch (standard) | ONNX Runtime (standard) |
| **Community / English docs** | Moderate (primarily Chinese-language) | Strong | Moderate |
| **Active maintenance (2025–2026)** | Very active (11 releases in 12 months) | Active | Active |
| **Spacing/word-boundary accuracy** | Good | Good | Known issues (community-reported) |
| **Structured-text suitability** | Best (PP-OCRv5 multi-scenario corpus) | Good | Good |

Sources: [tildalice.io](https://tildalice.io/ocr-tesseract-easyocr-paddleocr-benchmark/) (accessed 2026-05-25); [codesota.com](https://www.codesota.com/ocr/best-for-python) (accessed 2026-05-25); [paddlepaddle PyPI](https://pypi.org/project/paddlepaddle/#files) (accessed 2026-05-25); [paddleocr PyPI](https://pypi.org/project/paddleocr/) (accessed 2026-05-25).

---

### Final pick recommendation

**Pick: RapidOCR**, with EasyOCR as the tested fallback; PaddleOCR deprioritized.

PaddleOCR PP-OCRv5 is now demonstrably the most accurate free offline OCR engine by 2026 benchmarks. However, for ducat-lens specifically it is the wrong choice. The application is a stateless public web tool (FastAPI backend) that must return results quickly on a shared CPU server. PaddleOCR's CPU inference measured at ~4.85s per image — more than 20x slower than RapidOCR's 0.21s — is disqualifying for a per-request pipeline serving interactive web users. The heavier PaddlePaddle dependency (105–195 MB, non-standard framework outside Python web stacks) adds container/deployment complexity with no accuracy payoff over RapidOCR on this specific task: RapidOCR uses the same underlying PP-OCR model weights via ONNX, delivers comparable CER (0.10 vs 0.10), and installs in under 80 MB. EasyOCR remains ranked above PaddleOCR for ducat-lens — its PyTorch dependency is heavier (~1–1.5 GB), but PyTorch is a widely deployed framework, its latency at 0.66s is acceptable for web use, and it is the only engine of the three with documented superior accuracy on stylized/scene fonts (CER 0.09 vs 0.10). The revised ranking for ducat-lens is: (1) RapidOCR — lightest footprint, fastest inference, Apache 2.0, PaddleOCR-level accuracy via ONNX; (2) EasyOCR — best stylized-font accuracy, acceptable latency, higher footprint; (3) PaddleOCR — highest benchmark accuracy overall but worst CPU latency (~23x slower than RapidOCR), heavier non-standard framework, deprioritized for a web serving context.

**Abort conditions for PaddleOCR:**
- CPU inference latency ~4.85s/image on Apple M-series maps to 10–20s+ on shared cloud CPU. Alone, this aborts PaddleOCR for interactive web use.
- Dependency conflict between `paddleocr[all]` and LangChain 1.0.0 is a real integration risk if the project later adds LLM features.
- Windows LTSC / WSL2 users reported missing pre-built wheel configurations in GitHub discussion #15960 — not confirmed fully resolved.
- None of the above abort conditions apply to RapidOCR or EasyOCR.
