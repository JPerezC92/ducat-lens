# Ducat data sources

## Image analysis note

From `image.png`: ducat values are displayed in the Kiosk UI (e.g., the gold coin icon + number per card). However, these values are small and in the UI chrome — OCR on the value number is unreliable. The recommended architecture reads item names via vision, then looks up ducat values from an API or static dataset. This file covers the lookup layer.

---

## Ducat value background

Fact (source: [wiki.warframe.com/w/Orokin_Ducats](https://wiki.warframe.com/w/Orokin_Ducats), accessed 2026-05-24):
- Common (bronze) Prime parts: **15 ducats**
- Uncommon (silver): **45 ducats**
- Rare (gold): **100 ducats**
- Adjusted values for rarity-shifted items: **25** and **65 ducats**
- Five tiers total: 15, 25, 45, 65, 100

Sample values confirmed from wiki (accessed 2026-05-24):
- Wisp Prime Blueprint = **100 ducats**
- Braton Prime Barrel = **15 ducats**
- Wisp Prime Chassis Blueprint = **65 ducats**

---

## Primary recommendation: WFCD/warframe-items (static JSON, MIT license)

**Type:** Static JSON dataset, not a live REST API. Published as npm package `@wfcd/items`, also available as raw GitHub JSON files.

**Endpoint / source:**
```
https://raw.githubusercontent.com/WFCD/warframe-items/master/data/json/Warframes.json
https://raw.githubusercontent.com/WFCD/warframe-items/master/data/json/Primary.json
# ... one file per category (Secondary, Melee, etc.)
```

**Auth:** None. Public GitHub raw URLs.

**Rate limits:** GitHub raw CDN — no stated rate limit for reasonable read traffic. For a backend that caches at startup, one fetch per deploy is sufficient.

**Update cadence:** Fact — the package is auto-updated with each Warframe release (published 6 hours before research was conducted, per npm registry). Source: [@wfcd/items npm](https://www.npmjs.com/package/@wfcd/items) (accessed 2026-05-24).

**Relevant fields per item component:**
```json
{
  "name": "Ash Prime Systems Blueprint",
  "primeSellingPrice": 65,
  "ducats": 65,
  "tradable": true,
  "drops": [...]
}
```
Fact: both `primeSellingPrice` and `ducats` fields confirmed present in `Warframes.json` (Ash Prime entry verified via raw GitHub fetch, accessed 2026-05-24). Both fields hold identical integer values representing the Ducat Kiosk sell price.

**License:** MIT. Source: [WFCD/warframe-items GitHub](https://github.com/WFCD/warframe-items) (accessed 2026-05-24).

**Recommended usage pattern for ducat-lens backend:**
```python
import httpx, json

CATEGORIES = ["Warframes", "Primary", "Secondary", "Melee", "Companions"]
BASE = "https://raw.githubusercontent.com/WFCD/warframe-items/master/data/json"

async def build_ducat_lookup() -> dict[str, int]:
    """Returns {item_name_lower: ducat_value} for all Prime parts."""
    lookup = {}
    async with httpx.AsyncClient() as client:
        for cat in CATEGORIES:
            data = (await client.get(f"{BASE}/{cat}.json")).json()
            for item in data:
                if not item.get("name", "").endswith("Prime"):
                    continue
                for comp in item.get("components", []):
                    ducats = comp.get("ducats") or comp.get("primeSellingPrice")
                    if ducats:
                        lookup[comp["name"].lower()] = ducats
    return lookup
```

**Why primary:**
- Zero rate limits (cache at startup — one HTTP fetch per category file per deploy)
- MIT license — no ToS concerns for a public web tool
- Both `ducats` and `primeSellingPrice` fields present
- Updated automatically with game releases
- No auth required
- Offline-friendly: can ship the JSON files as bundled static assets

**Gap:** JSON files are split by category. The backend must fetch multiple files and build a merged lookup. Item name matching requires normalization (e.g., OCR output "Wisp Prime Blueprint" must match key "Wisp Prime Blueprint" — case + spacing sensitive).

---

## Fallback: warframe.market API v1

**Endpoint:**
```
GET https://api.warframe.market/v1/items/{url_name}
```
Example: `GET https://api.warframe.market/v1/items/braton_prime_barrel`

**Auth:** None for GET requests. Optional `Authorization: JWT <token>` for write operations only.

**Rate limits:** Not publicly documented. Community usage suggests no hard limit for unauthenticated GET requests; a per-IP soft limit of ~5 req/s is community-reported (unconfirmed in official docs). Source: [warframe.market API docs](https://warframe.market/api_docs) (accessed 2026-05-24).

**Response shape:** Fact (confirmed via [cwong8.github.io scrape analysis](https://cwong8.github.io/projects/warframe_market/JSON_SQL/), accessed 2026-05-24):
```json
{
  "payload": {
    "item": {
      "items_in_set": [
        {
          "id": "54a73e65e779893a797fff5d",
          "url_name": "braton_prime_barrel",
          "item_name": "Braton Prime Barrel",
          "ducats": 15,
          "rarity": "common",
          "trading_tax": 2000,
          "tags": ["prime", "primary", "component"],
          "icon": "...",
          "thumb": "..."
        }
      ]
    }
  }
}
```
Fact: `ducats` field confirmed present in `items_in_set` array. Field is an integer. Source: cwong8.github.io analysis confirms the `if "ducats" in item_in_set:` pattern and integer cast.

**Live fetch status:** Direct fetch to `api.warframe.market/v1/items` redirected to 404 during this research session (2026-05-24). Hypothesis: the v1 API may require a specific `Platform` header or may be experiencing routing issues. Evidence: HTTP 302 → `warframe.market/error/404` on raw URL fetch. What would confirm/refute: test with `curl -H "Platform: pc"` header (community convention for v1).

**Terms:** Warframe.market does not publish explicit API terms for read-only use. Community has used the API since ~2017 without takedowns. Hypothesis: read-only unauthenticated usage is tolerated. What would confirm: official API terms page (not found in research).

**License:** No stated data license. Treat as "use at your own risk."

**Why fallback (not primary):**
- Live API redirect to 404 during research — reliability uncertain at time of writing
- No official rate limit documentation
- v1 marked as deprecated (v2 migration pending per [market-api-spec](https://github.com/WFCD/market-api-spec))
- ToS ambiguous

**Sample request (Python):**
```python
import httpx

async def get_ducat_from_market(url_name: str) -> int | None:
    headers = {"Platform": "pc", "Accept": "application/json"}
    url = f"https://api.warframe.market/v1/items/{url_name}"
    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=headers)
        if r.status_code != 200:
            return None
        data = r.json()
        for part in data["payload"]["item"]["items_in_set"]:
            if part["url_name"] == url_name:
                return part.get("ducats")
    return None
```

---

## Discarded

- **Official Warframe API (`developers.warframe.com`, `api.warframe.com`)** — Fact: no public REST API for item data exists at these domains. The Warframe forums thread on the topic confirms no official public API is maintained by Digital Extremes for external developers. Source: [Warframe Forums official API thread](https://forums.warframe.com/topic/1391372-official-api/) (accessed 2026-05-24). WFCD/warframe-items itself pulls from the Warframe mobile export (a private internal API endpoint), not a public developer API.

- **warframestat.us API (`api.warframestat.us`)** — Fact: the `/items/search/{query}` endpoint exists and returns item data. The docs reference a `primeSellingPrice` field. However, direct fetch returned HTTP 403 during this research session, and the API focuses on world state (alerts, fissures, sortie) rather than static item catalogs. Source: [docs.warframestat.us](https://docs.warframestat.us/) (accessed 2026-05-24). The item data it provides is sourced from the same WFCD/warframe-items dataset — going to the source (WFCD GitHub JSON) is simpler and more reliable.

- **Wiki scrape (warframe.fandom.com, wiki.warframe.com)** — Fact: ducat tables exist and were accessible during this research (wiki.warframe.com/w/Ducats/Prices/All returned full data). However, wiki HTML scraping is fragile (DOM changes break parsers), warframe.fandom.com returned 403, and maintaining a scraper adds ongoing maintenance burden. WFCD/warframe-items provides the same data in machine-readable JSON with MIT license. Wiki scrape is viable as a last-resort static snapshot only.

---

## Real ducat value — confirmed sample

Source: wiki.warframe.com/w/Ducats/Prices/All (accessed 2026-05-24) + WFCD/warframe-items Warframes.json (Ash Prime entry accessed 2026-05-24):

| Item | Ducat value | Source |
|---|---|---|
| Wisp Prime Blueprint | **100** | wiki.warframe.com (Fact) |
| Wisp Prime Chassis Blueprint | **65** | wiki.warframe.com (Fact) |
| Braton Prime Barrel | **15** | wiki.warframe.com (Fact) |
| Ash Prime Systems Blueprint | **65** | WFCD Warframes.json `ducats` field (Fact) |

---

## Abort condition check

A public ducat data source exists (WFCD/warframe-items, MIT license, JSON, auto-updated). Abort condition (no public ducat API) is NOT triggered.

---

## Sources

- [WFCD/warframe-items GitHub](https://github.com/WFCD/warframe-items) (accessed 2026-05-24)
- [@wfcd/items npm](https://www.npmjs.com/package/@wfcd/items) (accessed 2026-05-24)
- [WFCD/warframe-items Warframes.json (raw)](https://raw.githubusercontent.com/WFCD/warframe-items/master/data/json/Warframes.json) (accessed 2026-05-24)
- [warframe.market API docs](https://warframe.market/api_docs) (accessed 2026-05-24)
- [cwong8.github.io warframe.market scrape analysis](https://cwong8.github.io/projects/warframe_market/JSON_SQL/) (accessed 2026-05-24)
- [WFCD/market-api-spec openapi.yaml](https://github.com/WFCD/market-api-spec/blob/master/openapi.yaml) (accessed 2026-05-24)
- [docs.warframestat.us](https://docs.warframestat.us/) (accessed 2026-05-24)
- [wiki.warframe.com/w/Orokin_Ducats](https://wiki.warframe.com/w/Orokin_Ducats) (accessed 2026-05-24)
- [wiki.warframe.com/w/Ducats/Prices/All](https://wiki.warframe.com/w/Ducats/Prices/All) (accessed 2026-05-24)
- [Warframe Forums official API thread](https://forums.warframe.com/topic/1391372-official-api/) (accessed 2026-05-24)
- [Hyrulien/Ducanator GitHub](https://github.com/Hyrulien/Ducanator) (accessed 2026-05-24)
