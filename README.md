# Xray Reality + MTProto Kit

Deploy `Xray Reality` and `MTProto` on a VPS with `x-ui`, reusable `Sing-box / SFM` client configs, and operator-friendly runbooks.

## Why This Exists

This repo is for people who want a small, understandable access stack:

- `VLESS + Reality` as the main path
- `MTProto` as the Telegram-native fallback
- `x-ui` as the operator panel
- `Sing-box / SFM` JSON configs for macOS

It is designed for small private deployments, staged migrations, and personal or family use.

## What Is Included

- deploy guidance for a Debian VPS
- `Sing-box / SFM` config template
- `mtg` systemd unit and example config
- a small config generator for client JSON
- durable operating docs in `docs/project_knowledge/`

## What Is Not Included

- live server credentials
- real UUIDs
- real panel passwords
- real MTProto secrets
- any private DNS or TLS material

This repo is meant to be publishable. Fill in your own secrets and values.

## Core Stack

- `x-ui`
- `Xray`
- `mtg`
- `Sing-box / SFM`

## Typical Ports

- `443` main `VLESS TCP + Reality`
- `2053` fallback `VLESS TCP + Reality`
- `2083` fallback `VLESS XHTTP + Reality`
- `8443` `MTProto`
- `29750` x-ui panel
- `2096` x-ui sub server

## Quick Start

1. Create a Debian VM.
2. Open firewall ports:
   - `80,443,2053,2083,2087,2096,29750,8443`
3. Install `x-ui`.
4. Create Reality inbounds in `x-ui`.
5. Install `mtg`.
6. Generate client JSON with:

```bash
python3 scripts/generate_singbox_config.py \
  --server 1.2.3.4 \
  --uuid YOUR_UUID \
  --public-key YOUR_REALITY_PUBLIC_KEY \
  --short-id YOUR_SHORT_ID \
  --sni www.google.com \
  --label my-main-reality
```

## Repo Layout

- `docs/project_knowledge/project.md`
- `docs/project_knowledge/architecture.md`
- `docs/project_knowledge/patterns.md`
- `docs/project_knowledge/deployment.md`
- `scripts/generate_singbox_config.py`
- `templates/sfm/reality-main.template.json`
- `templates/mtg/mtg.toml.example`
- `templates/systemd/mtg.service`

## Suggested GitHub Description

`Deploy Xray Reality + MTProto on a VPS with x-ui, reusable Sing-box/SFM configs, and operator runbooks.`

## License

MIT
