#!/usr/bin/env python3
"""Generate the Bruno, Postman, Insomnia, and HTTPie collections from one request catalog.

Run from the repo root:  python3 tools/generate.py
Outputs:
  bruno/parlayapi/...                          (git-native Bruno collection)
  postman/ParlayAPI.postman_collection.json    (Postman collection v2.1)
  insomnia/ParlayAPI.insomnia_collection.json  (Insomnia v4 export)
  httpie/keyless.sh                            (HTTPie CLI commands)
"""
import json
import os
import re
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://parlay-api.com"
SIGNUP = "Get a free API key (1,000 credits a month, no card): https://parlay-api.com/signup"

DESCRIPTION = (
    "ParlayAPI: real-time sports odds API. 30+ sportsbooks and data sources, player props, "
    "arbitrage and +EV tools, prediction markets (Kalshi, Polymarket), historical closing lines "
    "from 2005. Drop-in compatible with the-odds-api (same endpoint shapes, /v4 paths, ?apiKey= auth). "
    "Free tier: 1,000 credits a month, no card required. Docs: https://parlay-api.com/docs"
)

# folder key -> (display name, bruno path relative to collection root)
FOLDERS = {
    "sandbox": ("Keyless: Sandbox", "keyless/sandbox"),
    "live": ("Keyless: Live scoreboard", "keyless/live"),
    "calc": ("Keyless: Calculators", "keyless/calculators"),
    "meta": ("Keyless: Meta and discovery", "keyless/meta"),
    "pm": ("Keyless: Prediction markets", "keyless/prediction-markets"),
    "keyed": ("Keyed: real data with your API key", "keyed"),
    "mcp": ("Remote MCP", "mcp"),
}

MCP_INIT_BODY = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "protocolVersion": "2025-06-18",
        "capabilities": {},
        "clientInfo": {"name": "parlayapi-collections", "version": "1.0.0"},
    },
}
MCP_TOOLS_BODY = {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}

MCP_DOCS = (
    "MCP streamable HTTP endpoint hosted by ParlayAPI. Remote-capable MCP clients "
    "(claude.ai connectors, hosted agents) normally do this handshake for you: just point "
    "them at {base}/mcp/http. Keyless requests get the discovery and signup tools; add "
    "Authorization: Bearer <api_key> for the full set. Some deployments require the "
    "Mcp-Session-Id response header from initialize to be echoed on later calls. "
    "If this request returns 404 the remote transport is not deployed yet: install the "
    "local server instead with: uvx parlayapi-mcp (source: "
    "https://github.com/JacobiusMakes/parlay-api-mcp)."
).format(base=BASE)

# Each request: folder, name, method, path, query (list of [k, v]), headers, body(dict|None), docs, assert200
CATALOG = [
    # ---- Keyless: sandbox ----
    dict(folder="sandbox", name="List sandbox sports", method="GET", path="/v1/sandbox/sports", query=[],
         docs="Keyless and free. Lists the sport keys available in the sandbox. The sandbox mirrors real response shapes with static data, so you can build your integration before signing up."),
    dict(folder="sandbox", name="Sandbox NFL odds (h2h, spreads, totals)", method="GET",
         path="/v1/sandbox/sports/americanfootball_nfl/odds",
         query=[["regions", "us"], ["markets", "h2h,spreads,totals"], ["oddsFormat", "american"]],
         docs="Keyless and free. Same response shape as the keyed /v1/sports/{sport_key}/odds endpoint (and as the-odds-api), with static sandbox data."),
    dict(folder="sandbox", name="Sandbox NFL player props", method="GET",
         path="/v1/sandbox/sports/americanfootball_nfl/props", query=[],
         docs="Keyless and free. Player props response shape with static sandbox data."),
    dict(folder="sandbox", name="Sandbox NFL arbitrage", method="GET",
         path="/v1/sandbox/sports/americanfootball_nfl/arbitrage", query=[],
         docs="Keyless and free. Cross-book arbitrage finder response shape with static sandbox data."),
    dict(folder="sandbox", name="Sandbox NFL events", method="GET",
         path="/v1/sandbox/sports/americanfootball_nfl/events", query=[],
         docs="Keyless and free. Upcoming events list with static sandbox data."),
    dict(folder="sandbox", name="Sandbox NFL scores", method="GET",
         path="/v1/sandbox/sports/americanfootball_nfl/scores", query=[],
         docs="Keyless and free. Scores response shape with static sandbox data."),
    # ---- Keyless: live ----
    dict(folder="live", name="Live: sports on the board", method="GET", path="/live/api/sports", query=[],
         docs="Keyless and free. Sports that currently have live or upcoming games on the public live scoreboard."),
    dict(folder="live", name="Live: search events", method="GET", path="/live/api/search",
         query=[["q", "yankees"]],
         docs="Keyless and free. Search live and upcoming events by team or league name."),
    dict(folder="live", name="Live: command center", method="GET", path="/live/api/command_center",
         query=[["limit", "5"]],
         docs="Keyless and free. One call that returns the most watchable games right now with live state and odds movement."),
    # ---- Keyless: calculators ----
    dict(folder="calc", name="Kelly stake calculator", method="GET", path="/v1/calc/kelly",
         query=[["bankroll", "1000"], ["odds", "120"], ["win_prob", "0.55"], ["fraction", "0.25"]],
         docs="Keyless and free. Kelly criterion stake sizing. odds accepts American (120, -110) or decimal (2.20). fraction=0.25 is quarter Kelly."),
    dict(folder="calc", name="Edge calculator", method="GET", path="/v1/calc/edge",
         query=[["odds", "-110"], ["true_prob", "0.55"]],
         docs="Keyless and free. Expected value of a bet given your estimated true win probability. Alternative mode: pass sharp_over_odds and sharp_under_odds instead of true_prob to devig a sharp book's two-sided price."),
    dict(folder="calc", name="Hedge calculator", method="GET", path="/v1/calc/hedge",
         query=[["original_stake", "100"], ["original_odds", "250"], ["hedge_odds", "-140"]],
         docs="Keyless and free. How much to stake on the other side to lock in equal profit (target=equal_profit) or guarantee break-even (target=break_even)."),
    dict(folder="calc", name="Free bet conversion calculator", method="GET", path="/v1/calc/free-bet",
         query=[["free_bet_usd", "50"], ["bet_odds", "300"], ["hedge_odds", "-320"]],
         docs="Keyless and free. Optimal hedge for converting a free bet or bonus bet into withdrawable cash, with the conversion rate."),
    # ---- Keyless: meta ----
    dict(folder="meta", name="Credit costs per endpoint", method="GET", path="/v1/meta/credit-costs", query=[],
         docs="Keyless and free. Exact credit price of every endpoint, including the formula for variable-cost endpoints (markets x regions). Every paid response also carries an x-requests-last header with the exact charge."),
    dict(folder="meta", name="API info and discovery", method="GET", path="/v1/meta/api-info", query=[],
         docs="Keyless and free. Machine-readable overview: base URLs, auth options, SDK links, docs links."),
    # ---- Keyless: prediction markets ----
    dict(folder="pm", name="Search prediction markets", method="GET", path="/v1/prediction-markets/search",
         query=[["q", "nfl"], ["limit", "5"]],
         docs="Keyless and free. Search event markets across Kalshi, Polymarket, and Novig by keyword. Add sources=kalshi to filter, min_volume to cut thin markets."),
    # ---- Keyed ----
    dict(folder="keyed", name="List sports (keyed)", method="GET", path="/v1/sports", query=[],
         headers=[["X-API-Key", "{{apiKey}}"]],
         docs="0 credits. Lists all live sport keys. " + SIGNUP),
    dict(folder="keyed", name="NFL odds (keyed)", method="GET", path="/v1/sports/americanfootball_nfl/odds",
         query=[["regions", "us"], ["markets", "h2h"]],
         headers=[["X-API-Key", "{{apiKey}}"]],
         docs="Costs markets x regions credits (floor 1): h2h + us = 1 credit. Real-time odds from 30+ sportsbooks and data sources. " + SIGNUP),
    dict(folder="keyed", name="NFL player props (keyed)", method="GET",
         path="/v1/sports/americanfootball_nfl/props", query=[],
         headers=[["X-API-Key", "{{apiKey}}"]],
         docs="3 credits. Player props with American odds across books and DFS apps. " + SIGNUP),
    dict(folder="keyed", name="NFL arbitrage (keyed)", method="GET",
         path="/v1/sports/americanfootball_nfl/arbitrage", query=[],
         headers=[["X-API-Key", "{{apiKey}}"]],
         docs="10 credits. Pre-match arbitrage opportunities across books. " + SIGNUP),
    dict(folder="keyed", name="Account usage (keyed)", method="GET", path="/v1/account", query=[],
         headers=[["X-API-Key", "{{apiKey}}"]],
         docs="Check your remaining credits and current billing period usage. " + SIGNUP),
    dict(folder="keyed", name="the-odds-api compat: /v4/sports (keyed)", method="GET", path="/v4/sports",
         query=[["apiKey", "{{apiKey}}"]],
         docs="Drop-in the-odds-api compatibility: same /v4 path shape and ?apiKey= query auth. Point existing the-odds-api code at parlay-api.com and it works. " + SIGNUP),
    # ---- MCP ----
    dict(folder="mcp", name="MCP: initialize", method="POST", path="/mcp/http", query=[],
         headers=[["Content-Type", "application/json"], ["Accept", "application/json, text/event-stream"]],
         body=MCP_INIT_BODY, docs=MCP_DOCS, assert200=False),
    dict(folder="mcp", name="MCP: list tools", method="POST", path="/mcp/http", query=[],
         headers=[["Content-Type", "application/json"], ["Accept", "application/json, text/event-stream"]],
         body=MCP_TOOLS_BODY, docs=MCP_DOCS, assert200=False),
]


def slug(name):
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return s


def qs(query):
    if not query:
        return ""
    return "?" + "&".join(f"{k}={v}" for k, v in query)


# ---------------- Bruno ----------------

def write_bruno():
    broot = os.path.join(ROOT, "bruno", "parlayapi")
    os.makedirs(os.path.join(broot, "environments"), exist_ok=True)
    with open(os.path.join(broot, "bruno.json"), "w") as f:
        json.dump({"version": "1", "name": "parlayapi", "type": "collection",
                   "ignore": ["node_modules", ".git"]}, f, indent=2)
        f.write("\n")
    with open(os.path.join(broot, "environments", "Default.bru"), "w") as f:
        f.write("vars {\n  baseUrl: https://parlay-api.com\n  apiKey: paste_your_free_key_here\n}\n")

    seq_by_folder = {}
    for req in CATALOG:
        _, rel = FOLDERS[req["folder"]]
        d = os.path.join(broot, rel)
        os.makedirs(d, exist_ok=True)
        seq = seq_by_folder.get(rel, 0) + 1
        seq_by_folder[rel] = seq
        lines = []
        lines.append("meta {")
        lines.append(f"  name: {req['name']}")
        lines.append("  type: http")
        lines.append(f"  seq: {seq}")
        lines.append("}")
        lines.append("")
        verb = req["method"].lower()
        body_kind = "json" if req.get("body") else "none"
        lines.append(f"{verb} {{")
        lines.append(f"  url: {{{{baseUrl}}}}{req['path']}{qs(req.get('query', []))}")
        lines.append(f"  body: {body_kind}")
        lines.append("  auth: none")
        lines.append("}")
        lines.append("")
        if req.get("headers"):
            lines.append("headers {")
            for k, v in req["headers"]:
                lines.append(f"  {k}: {v}")
            lines.append("}")
            lines.append("")
        if req.get("body"):
            body_text = json.dumps(req["body"], indent=2)
            lines.append("body:json {")
            for bl in body_text.splitlines():
                lines.append(f"  {bl}")
            lines.append("}")
            lines.append("")
        if req.get("assert200", True):
            lines.append("assert {")
            lines.append("  res.status: eq 200")
            lines.append("}")
            lines.append("")
        lines.append("docs {")
        lines.append(f"  {req['docs']}")
        lines.append("}")
        lines.append("")
        with open(os.path.join(d, slug(req["name"]) + ".bru"), "w") as f:
            f.write("\n".join(lines))


# ---------------- Postman v2.1 ----------------

def postman_request(req):
    query = [{"key": k, "value": v, "description": ""} for k, v in req.get("query", [])]
    raw = "{{baseUrl}}" + req["path"] + qs(req.get("query", []))
    r = {
        "name": req["name"],
        "request": {
            "method": req["method"],
            "header": [{"key": k, "value": v} for k, v in req.get("headers", [])],
            "url": {
                "raw": raw,
                "host": ["{{baseUrl}}"],
                "path": [p for p in req["path"].split("/") if p],
                "query": query,
            },
            "description": req["docs"],
        },
        "response": [],
    }
    if req.get("body"):
        r["request"]["body"] = {
            "mode": "raw",
            "raw": json.dumps(req["body"], indent=2),
            "options": {"raw": {"language": "json"}},
        }
    return r


def write_postman():
    items = []
    for fkey, (display, _) in FOLDERS.items():
        reqs = [postman_request(r) for r in CATALOG if r["folder"] == fkey]
        items.append({"name": display, "item": reqs})
    coll = {
        "info": {
            "name": "ParlayAPI (curated)",
            "description": DESCRIPTION + "\n\nKeyless folders run with no API key at all. "
                           "For the keyed folder, set the apiKey collection variable. " + SIGNUP,
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
        },
        "item": items,
        "variable": [
            {"key": "baseUrl", "value": BASE, "type": "string"},
            {"key": "apiKey", "value": "", "type": "string",
             "description": SIGNUP},
        ],
    }
    os.makedirs(os.path.join(ROOT, "postman"), exist_ok=True)
    with open(os.path.join(ROOT, "postman", "ParlayAPI.postman_collection.json"), "w") as f:
        json.dump(coll, f, indent=2)
        f.write("\n")


# ---------------- Insomnia v4 ----------------

def write_insomnia():
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    resources = [
        {"_id": "wrk_parlayapi", "_type": "workspace", "name": "ParlayAPI (curated)",
         "description": DESCRIPTION, "scope": "collection"},
        {"_id": "env_parlayapi_base", "_type": "environment", "parentId": "wrk_parlayapi",
         "name": "Base Environment",
         "data": {"baseUrl": BASE, "apiKey": "paste_your_free_key_here"}},
    ]
    for i, (fkey, (display, _)) in enumerate(FOLDERS.items(), start=1):
        fid = f"fld_parlayapi_{fkey}"
        resources.append({"_id": fid, "_type": "request_group", "parentId": "wrk_parlayapi",
                          "name": display, "metaSortKey": i * 100})
        for j, req in enumerate([r for r in CATALOG if r["folder"] == fkey], start=1):
            rid = f"req_{fkey}_{j}"
            res = {
                "_id": rid,
                "_type": "request",
                "parentId": fid,
                "name": req["name"],
                "description": req["docs"],
                "method": req["method"],
                "url": "{{ _.baseUrl }}" + req["path"],
                "parameters": [{"name": k, "value": v.replace("{{apiKey}}", "{{ _.apiKey }}")}
                               for k, v in req.get("query", [])],
                "headers": [{"name": k, "value": v.replace("{{apiKey}}", "{{ _.apiKey }}")}
                            for k, v in req.get("headers", [])],
                "metaSortKey": j * 100,
            }
            if req.get("body"):
                res["body"] = {"mimeType": "application/json",
                               "text": json.dumps(req["body"], indent=2)}
            resources.append(res)
    export = {
        "_type": "export",
        "__export_format": 4,
        "__export_date": now,
        "__export_source": "parlayapi-collections",
        "resources": resources,
    }
    os.makedirs(os.path.join(ROOT, "insomnia"), exist_ok=True)
    with open(os.path.join(ROOT, "insomnia", "ParlayAPI.insomnia_collection.json"), "w") as f:
        json.dump(export, f, indent=2)
        f.write("\n")


# ---------------- HTTPie ----------------

def write_httpie():
    lines = [
        "#!/bin/sh",
        "# ParlayAPI keyless requests as HTTPie CLI commands. Every one of these runs",
        "# with no API key and costs nothing. https://parlay-api.com/docs",
        "# " + SIGNUP,
        "set -x",
        "",
    ]
    for req in CATALOG:
        if req["folder"] in ("keyed",):
            continue
        if req["folder"] == "mcp":
            continue
        parts = [f"http GET {BASE}{req['path']}"]
        for k, v in req.get("query", []):
            parts.append(f"{k}=={v}")
        lines.append("# " + req["name"])
        lines.append(" ".join(parts))
        lines.append("")
    lines += [
        "# ---- Keyed examples (uncomment and export PARLAYAPI_KEY first) ----",
        "# " + SIGNUP,
        '# http GET https://parlay-api.com/v1/sports "X-API-Key:$PARLAYAPI_KEY"',
        '# http GET https://parlay-api.com/v1/sports/americanfootball_nfl/odds regions==us markets==h2h "X-API-Key:$PARLAYAPI_KEY"',
        '# http GET https://parlay-api.com/v1/sports/americanfootball_nfl/props "X-API-Key:$PARLAYAPI_KEY"',
        '# http GET https://parlay-api.com/v1/account "X-API-Key:$PARLAYAPI_KEY"',
        "",
        "# ---- Remote MCP endpoint (streamable HTTP) ----",
        "# If this 404s the remote transport is not deployed yet; use: uvx parlayapi-mcp",
        "# http POST https://parlay-api.com/mcp/http jsonrpc=2.0 id:=1 method=initialize \\",
        "#   'Accept:application/json, text/event-stream'",
        "",
    ]
    os.makedirs(os.path.join(ROOT, "httpie"), exist_ok=True)
    p = os.path.join(ROOT, "httpie", "keyless.sh")
    with open(p, "w") as f:
        f.write("\n".join(lines))
    os.chmod(p, 0o755)


if __name__ == "__main__":
    write_bruno()
    write_postman()
    write_insomnia()
    write_httpie()
    print("generated: bruno/, postman/, insomnia/, httpie/")
