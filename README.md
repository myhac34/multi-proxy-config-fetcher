# Multi Proxy Config Fetcher

Automatically collects, tests, deduplicates, and groups V2Ray configurations.

## Features

- Fetches configs from multiple sources
- Removes duplicate configs
- Detects server countries
- Tests configs with Xray and Sing-box
- Groups configs by region
- Automatic updates with GitHub Actions

## Regions

Configs are grouped into:

- USA & Canada
- Western Europe
- Scandinavia
- Russia & CIS
- China & East Asia
- Middle East
- Eastern Europe
- Africa
- Other countries

## Subscription Links

After GitHub Actions runs, regional subscriptions are created in:

`configs/regional/`

These files can be used as subscription links in Throne and compatible clients.

## Update

GitHub Actions updates the configs automatically.

Manual update:

`Actions → Update Proxy Configs → Run workflow`

## Based on

https://github.com/4n0nymou3/multi-proxy-config-fetcher
