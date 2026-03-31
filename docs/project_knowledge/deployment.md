# Deployment

## Goal

Bring up a small private access server on a Debian VPS with:

- `x-ui`
- `Xray Reality`
- `mtg`
- optional `Sing-box / SFM` client configs

## Server Prerequisites

- Debian 12 VPS
- public IPv4
- root or sudo access
- open firewall ports

## Recommended Open Ports

- `80`
- `443`
- `2053`
- `2083`
- `2087`
- `2096`
- `29750`
- `8443`

## Basic Order

1. Update the server and install base tools.
2. Install `x-ui`.
3. Set the panel credentials.
4. Create `Reality` inbounds.
5. Install `mtg`.
6. Generate user configs.
7. Test from a real client before migration.

## x-ui Notes

- the panel can run directly by IP
- if using IP certificates, Let's Encrypt may require a short-lived certificate profile
- keep the panel path non-default

## MTProto Notes

- `8443` is a good default for Telegram-native proxy
- use fake TLS `ee` secrets
- publish only the final Telegram link, not private server internals

## Client Configs

Use `scripts/generate_singbox_config.py` to build a reusable `Sing-box / SFM` profile.

Example:

```bash
python3 scripts/generate_singbox_config.py \
  --server YOUR_SERVER_IP \
  --uuid YOUR_UUID \
  --public-key YOUR_REALITY_PUBLIC_KEY \
  --short-id YOUR_SHORT_ID \
  --sni www.google.com \
  --pretty
```
