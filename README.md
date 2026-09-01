# ParlayAPI request collections

Ready-to-import request collections for [ParlayAPI](https://parlay-api.com), the sports odds API: 30+ sportsbooks and data sources, player props, arbitrage and +EV tools, prediction markets (Kalshi, Polymarket), historical closing lines from 2005, and drop-in compatibility with the-odds-api.

One curated request set, three formats:

| Tool | File | Import |
|---|---|---|
| Bruno | [`bruno/parlayapi/`](bruno/parlayapi/) | git-native, no account needed: clone and open |
| Postman | [`postman/ParlayAPI.postman_collection.json`](postman/ParlayAPI.postman_collection.json) | Collection v2.1 |
| Insomnia | [`insomnia/ParlayAPI.insomnia_collection.json`](insomnia/ParlayAPI.insomnia_collection.json) | Insomnia v4 export |
| HTTPie CLI | [`httpie/keyless.sh`](httpie/keyless.sh) | plain `http` commands, paste and run |

Most of the collection needs **no API key at all**. Import it and press send.

The four files above are generated from one catalog in [`tools/generate.py`](tools/generate.py), which is what keeps them identical across formats. Postman users have a second option: a larger, separately curated collection hosted on the API's own domain, which is the one published to the Postman Public API Network. See below.

## Run in Postman

The canonical Postman collection lives on the API's own domain, so a re-import always picks up the current version:

```
https://parlay-api.com/collections/ParlayAPI.postman_collection.json
```

In Postman: **Import > Link**, paste that, done. Thirty requests in six folders, twelve of which run with no API key. The page behind it, with the folder breakdown and what every variable means, is [parlay-api.com/postman](https://parlay-api.com/postman).

Insomnia, Bruno, Hoppscotch and HTTPie all read Postman Collection v2.1, so the same URL imports into any of them.

### The button

Once the collection is published to a public Postman workspace, Postman issues a **Run in Postman** button bound to that workspace's collection id. Paste the id into this snippet and drop it wherever it belongs:

```markdown
[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/COLLECTION_ID)
```

```html
<div class="postman-run-button"
  data-postman-action="collection/import"
  data-postman-var-1="COLLECTION_ID"></div>
<script type="text/javascript">
  (function (p,o,s,t,m,a,n) {
    !p[s] && (p[s] = function () { (p[t] || (p[t] = [])).push(arguments); });
    !o.getElementById(s+t) && o.getElementsByTagName("head")[0].appendChild((
      (n = o.createElement("script")),
      (n.id = s+t), (n.async = 1), (n.src = m), n
    ));
  }(window, document, "_pm", "PostmanRunObject", "https://run.pstmn.io/button.js"));
</script>
```

Postman generates both forms under **collection > Share > Via Run in Postman**, so the id can be copied straight out of the app rather than assembled by hand. `COLLECTION_ID` above is a placeholder: the button does not resolve until the workspace is public, which is why the link-import instructions above are the ones to use today.

## What is in the collection

**Keyless folders (no key, no credits, run instantly):**

- **Sandbox**: sports list, NFL odds (h2h, spreads, totals), player props, arbitrage, events, scores. Static data with the exact response shapes of the real keyed endpoints, so you can build your integration before signing up.
- **Live scoreboard**: sports on the board, event search, and the command center feed behind [parlay-api.com/live](https://parlay-api.com/live).
- **Calculators**: Kelly stake sizing, edge/EV, hedging, and free bet conversion.
- **Meta and discovery**: per-endpoint credit costs and machine-readable API info.
- **Prediction markets**: keyword search across Kalshi, Polymarket, and Novig.

**Keyed folder** (uses a `{{apiKey}}` variable): list sports, real NFL odds, player props, arbitrage, account usage, and a the-odds-api `/v4` compatibility call. Get a free key (1,000 credits a month, no card) at [parlay-api.com/signup](https://parlay-api.com/signup).

**Remote MCP folder**: `POST https://parlay-api.com/mcp/http` examples (`initialize`, `tools/list`) for the hosted MCP streamable HTTP endpoint. If it returns 404 the remote transport is not deployed yet; use the local server via `uvx parlayapi-mcp` ([source](https://github.com/JacobiusMakes/parlay-api-mcp)).

## Import instructions

### Bruno

Bruno collections are plain files in git, so cloning this repo IS the import:

```sh
git clone https://github.com/JacobiusMakes/parlayapi-collections.git
```

Then in the Bruno app: **Open Collection** and pick the `bruno/parlayapi` folder. Select the `Default` environment. To use the keyed folder, edit the environment's `apiKey` value.

Or run the whole keyless set from the terminal without opening an app:

```sh
cd parlayapi-collections/bruno/parlayapi
npx @usebruno/cli run keyless -r --env Default
```

### Postman

**Import > files > `postman/ParlayAPI.postman_collection.json`**, or import by URL:

```
https://raw.githubusercontent.com/JacobiusMakes/parlayapi-collections/main/postman/ParlayAPI.postman_collection.json
```

The keyless folders work immediately. For the keyed folder, set the collection variable `apiKey` (collection > Variables tab).

### Insomnia

**Application menu > Preferences > Data > Import Data > From File** (or just drag the file in) and pick `insomnia/ParlayAPI.insomnia_collection.json`. `baseUrl` and `apiKey` live in the Base Environment.

### HTTPie

- **HTTPie Desktop / Web**: import the Postman collection file (HTTPie's importer accepts Postman v2.1).
- **HTTPie CLI**: `sh httpie/keyless.sh` runs every keyless request, or copy single commands out of the file.

## Verified against production

The keyless folder is CI-runnable and was verified against live production on 2026-08-27 with `@usebruno/cli` 4.0.0 (`npx @usebruno/cli run keyless -r --env Default`). Each request asserts HTTP 200:

```
keyless/calculators/kelly-stake-calculator (200 OK) - 270 ms
keyless/calculators/edge-calculator (200 OK) - 345 ms
keyless/calculators/hedge-calculator (200 OK) - 199 ms
keyless/calculators/free-bet-conversion-calculator (200 OK) - 136 ms
keyless/live/live-sports-on-the-board (200 OK) - 297 ms
keyless/live/live-search-events (200 OK) - 558 ms
keyless/live/live-command-center (200 OK) - 721 ms
keyless/meta/credit-costs-per-endpoint (200 OK) - 209 ms
keyless/meta/api-info-and-discovery (200 OK) - 160 ms
keyless/prediction-markets/search-prediction-markets (200 OK) - 7852 ms
keyless/sandbox/list-sandbox-sports (200 OK) - 226 ms
keyless/sandbox/sandbox-nfl-odds-h2h-spreads-totals (200 OK) - 236 ms
keyless/sandbox/sandbox-nfl-player-props (200 OK) - 148 ms
keyless/sandbox/sandbox-nfl-arbitrage (200 OK) - 135 ms
keyless/sandbox/sandbox-nfl-events (200 OK) - 161 ms
keyless/sandbox/sandbox-nfl-scores (200 OK) - 161 ms

Status: PASS | Requests: 16 (16 Passed) | Assertions: 16/16
```

## Quotas, honestly

- The **keyless folders cost nothing and need no account**: sandbox, live scoreboard, calculators, meta, and prediction-market search. Sandbox data is static; the live scoreboard and prediction-market data are real. Keyless surfaces are rate-limited per IP, so do not hammer them.
- The **keyed folder spends credits** from your plan. The free tier includes 1,000 credits a month with no card. Costs in this collection: odds is markets x regions credits (the h2h + us example is 1 credit), props is 3, arbitrage is 10, sports list and account usage are documented in [`/v1/meta/credit-costs`](https://parlay-api.com/v1/meta/credit-costs). Every paid response carries an `x-requests-last` header with the exact charge.
- Paid tiers and current prices: [parlay-api.com/pricing](https://parlay-api.com/pricing).

## Related

- Curated Postman collection hosted on the API's own domain, the canonical copy behind the Run in Postman button: [`https://parlay-api.com/collections/ParlayAPI.postman_collection.json`](https://parlay-api.com/collections/ParlayAPI.postman_collection.json) ([page](https://parlay-api.com/postman))
- Full auto-generated Postman collection of the entire API surface (every endpoint, not curated): [`https://parlay-api.com/collections/postman.json`](https://parlay-api.com/collections/postman.json)
- API docs: [parlay-api.com/docs](https://parlay-api.com/docs) and [OpenAPI spec](https://parlay-api.com/openapi.json)
- SDKs and ecosystem: [Python](https://github.com/JacobiusMakes/parlay-api-python), [JS](https://github.com/JacobiusMakes/parlay-api-js), [R](https://github.com/JacobiusMakes/parlayapiR), [Google Sheets](https://github.com/JacobiusMakes/parlayapi-sheets), [Raycast](https://github.com/JacobiusMakes/parlayapi-raycast), [MCP server](https://github.com/JacobiusMakes/parlay-api-mcp), [Discord bot](https://github.com/JacobiusMakes/parlayapi-discord-bot)

## Regenerating

All four outputs are generated from one request catalog in [`tools/generate.py`](tools/generate.py):

```sh
python3 tools/generate.py
```

Edit the catalog there, regenerate, and the Bruno, Postman, Insomnia, and HTTPie files stay in sync.

## License

MIT
