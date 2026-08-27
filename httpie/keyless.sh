#!/bin/sh
# ParlayAPI keyless requests as HTTPie CLI commands. Every one of these runs
# with no API key and costs nothing. https://parlay-api.com/docs
# Get a free API key (1,000 credits a month, no card): https://parlay-api.com/signup
set -x

# List sandbox sports
http GET https://parlay-api.com/v1/sandbox/sports

# Sandbox NFL odds (h2h, spreads, totals)
http GET https://parlay-api.com/v1/sandbox/sports/americanfootball_nfl/odds regions==us markets==h2h,spreads,totals oddsFormat==american

# Sandbox NFL player props
http GET https://parlay-api.com/v1/sandbox/sports/americanfootball_nfl/props

# Sandbox NFL arbitrage
http GET https://parlay-api.com/v1/sandbox/sports/americanfootball_nfl/arbitrage

# Sandbox NFL events
http GET https://parlay-api.com/v1/sandbox/sports/americanfootball_nfl/events

# Sandbox NFL scores
http GET https://parlay-api.com/v1/sandbox/sports/americanfootball_nfl/scores

# Live: sports on the board
http GET https://parlay-api.com/live/api/sports

# Live: search events
http GET https://parlay-api.com/live/api/search q==yankees

# Live: command center
http GET https://parlay-api.com/live/api/command_center limit==5

# Kelly stake calculator
http GET https://parlay-api.com/v1/calc/kelly bankroll==1000 odds==120 win_prob==0.55 fraction==0.25

# Edge calculator
http GET https://parlay-api.com/v1/calc/edge odds==-110 true_prob==0.55

# Hedge calculator
http GET https://parlay-api.com/v1/calc/hedge original_stake==100 original_odds==250 hedge_odds==-140

# Free bet conversion calculator
http GET https://parlay-api.com/v1/calc/free-bet free_bet_usd==50 bet_odds==300 hedge_odds==-320

# Credit costs per endpoint
http GET https://parlay-api.com/v1/meta/credit-costs

# API info and discovery
http GET https://parlay-api.com/v1/meta/api-info

# Search prediction markets
http GET https://parlay-api.com/v1/prediction-markets/search q==nfl limit==5

# ---- Keyed examples (uncomment and export PARLAYAPI_KEY first) ----
# Get a free API key (1,000 credits a month, no card): https://parlay-api.com/signup
# http GET https://parlay-api.com/v1/sports "X-API-Key:$PARLAYAPI_KEY"
# http GET https://parlay-api.com/v1/sports/americanfootball_nfl/odds regions==us markets==h2h "X-API-Key:$PARLAYAPI_KEY"
# http GET https://parlay-api.com/v1/sports/americanfootball_nfl/props "X-API-Key:$PARLAYAPI_KEY"
# http GET https://parlay-api.com/v1/account "X-API-Key:$PARLAYAPI_KEY"

# ---- Remote MCP endpoint (streamable HTTP) ----
# If this 404s the remote transport is not deployed yet; use: uvx parlayapi-mcp
# http POST https://parlay-api.com/mcp/http jsonrpc=2.0 id:=1 method=initialize \
#   'Accept:application/json, text/event-stream'
