# Founder runbook: publish the Postman collection to the Public API Network

The Postman Public API Network ([postman.com/explore](https://www.postman.com/explore)) is a real discovery channel: developers search it for "sports odds" and "betting API" and import collections directly into their Postman app. Listing there requires your Postman account, so this is a founder task. Budget: 20 to 30 minutes, $0.

UI labels below are as of August 2026 and may drift slightly.

## One-time setup

1. **Create a free Postman account** at [postman.com](https://www.postman.com) (sign up with your normal founder identity, e.g. the GitHub login). The free plan is enough to publish to the network.
2. **Create a public workspace.** In the web app: `Workspaces > Create Workspace`. Pick a blank workspace, name it **ParlayAPI**, and set **Visibility: Public**. Public visibility is what lists the workspace on the Public API Network.
3. **Write the workspace overview.** The network search indexes workspace and collection names, summaries, and descriptions, so put the search terms people actually type in the summary. Suggested summary:
   > Sports odds API collections: real-time odds from 30+ sportsbooks and data sources, player props, arbitrage, prediction markets (Kalshi, Polymarket). Free tier, no card. Drop-in compatible with the-odds-api.
4. **Import the curated collection.** In the workspace: `Import > files` and pick `postman/ParlayAPI.postman_collection.json` from this repo (or paste the raw GitHub URL). Confirm the `apiKey` collection variable is EMPTY before publishing; never publish a workspace containing a real key.
5. **Optionally import the full-surface collection too.** `Import > Link` with `https://parlay-api.com/collections/postman.json` gives a second collection covering every endpoint. Rename it "ParlayAPI (full API reference)" so the curated one stays the obvious starting point.
6. **Verify the listing.** Log out (or use a private window), search [postman.com/explore](https://www.postman.com/explore) for "ParlayAPI" and then for "sports odds". The workspace should appear; new listings can take a little while to index.

## Optional polish

- **Run in Postman button:** in the workspace, open the collection, `Share > Via Run in Postman`, copy the markdown or HTML button, and add it to the site docs page and this repo's README.
- **Verified publisher:** Postman offers team verification for organizations (domain-based). Worth doing once ParlayAPI has a Postman team; it adds a checkmark on the listing.
- **Watch the metrics:** public workspaces show views and forks. Forks of the collection are a decent proxy for developer interest.

## Keeping it fresh

When the API or this repo changes:

1. Pull this repo, run `python3 tools/generate.py` if the catalog changed.
2. In Postman, `Import` the updated `postman/ParlayAPI.postman_collection.json` again and choose **Replace** when prompted, so the public listing keeps its URL, forks, and watchers.

## Also relevant (separate follow-up)

The site's `/mcp` page advertises a hosted remote MCP endpoint at `https://parlay-api.com/mcp/http`, but as of 2026-08-27 that path returns 404 in production (checked with POST initialize). The MCP folder in these collections documents the 404 fallback honestly. When the remote transport ships, delete that fallback note from `tools/generate.py` (MCP_DOCS) and regenerate.
