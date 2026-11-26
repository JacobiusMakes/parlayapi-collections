# Check a player-props response

Open this folder as a collection in Bruno. Select **Default** and run [Sandbox NFL player props](keyless/sandbox/sandbox-nfl-player-props.bru). This request uses no API key. The response contains a sport key, a count and a `props` array. The test checks the count against the array length and the sandbox flag on each row.

Choose one row and identify its player, market, source, line and available sides. An empty array gives you zero observations. Sandbox rows demonstrate the format. To assess live coverage for your own build, use a separate request with an entitled account.

## Compare one NBA points market

Open [NBA player points across sportsbook and DFS sources](keyed/nba-player-points-dfs-keyed.bru). The same named request is in the Postman and Insomnia collections. It selects NBA player points from DraftKings, PrizePicks and Underdog, with a 25-row limit and midpoint normalization. Check your plan before sending. In Bruno, use an environment with `baseUrl` set to `https://parlay-api.com` and its `apiKey` stored as a secret variable. [Current plans](https://parlay-api.com/pricing) · [Bruno secret variables](https://docs.usebruno.com/secrets-management/secret-variables)

The default keyed response is a list. Look for two sources covering the same event, player, market, period and side. Record each line before comparing prices. A different threshold describes a different proposition. An unknown period, missing side or absent source leaves the comparison incomplete. For legacy flat-payout DFS rows, midpoint is a normalized comparison value. Use any provided selection and payout metadata to interpret the offer.

Check the response headers for pagination, truncation or degraded sources before treating a small page as a whole board. The key-authenticated, zero-credit `/v1/sports/basketball_nba/props/coverage` diagnostic can help explain a missing source. [Player-props documentation](https://parlay-api.com/docs)
