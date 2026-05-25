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
