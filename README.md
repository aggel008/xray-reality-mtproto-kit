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

## Server Size

For this stack, the server does not need to be large.

### Minimum

- `1 vCPU`
- `2 GB RAM`
- `10 GB SSD`
- `Debian 12`
- `1 public IPv4`

Good for:

- personal use
- family use
- a few occasional users
- mostly Telegram + normal browsing

### Recommended

- `2 vCPU`
- `2-4 GB RAM`
- `10-20 GB SSD`
- `Debian 12`
- `1 public IPv4`

Good for:

- safer headroom
- small private groups
- staged migration from an older VPN server
- operators who do not want to think about CPU pressure

### Real Example

The real working migration server used during development of this repo was:

- `e2-small`
- `Debian 12`
- `10 GB disk`

That size was enough for a small private deployment.

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
  --pretty
```

## Client Apps And Import Methods

### Correct Client Names

- `SFM` = `sing-box for Apple`
- `Hiddify Next`
- `v2rayN`
- `v2rayNG`

### Which Format Each Client Wants

- `SFM`: full `sing-box` JSON config
- `Hiddify Next`: usually `vless://` link or subscription URL
- `v2rayN`: `vless://` link
- `v2rayNG`: `vless://` link

### SFM

Use `SFM` when you want a local `sing-box` config with:

- split tunneling
- custom DNS rules
- direct routing for selected domains

Typical flow:

1. Create a local profile in `SFM`.
2. Open the profile content editor.
3. Paste the generated JSON config.
4. Save and enable the profile.

Important:

- `SFM` does not primarily want a raw `vless://` URI
- do not give it an arbitrary JSON blob
- give it a real local `sing-box` config with:
  - `dns` rules
  - `tun` inbound
  - `route` rules
  - `vless` outbound
- the templates and generator in this repo are meant for exactly that

### Hiddify Next

Typical flow:

1. Open `Hiddify Next`.
2. Choose import from clipboard, import from link, or add profile manually.
3. Paste the `vless://` link.
4. Save and connect.

### v2rayN

Typical flow:

1. Open `v2rayN`.
2. Use import from clipboard or import URL.
3. Paste the `vless://` link.
4. Select the profile and connect.

### v2rayNG

Typical flow:

1. Open `v2rayNG`.
2. Use import from clipboard, scan QR, or manual import.
3. Paste the `vless://` link.
4. Select the profile and connect.

### Practical Rule

- If the client asks for JSON, give it a proper `sing-box` client config, not a random JSON object
- That config should normally include:
  - `dns`
  - `inbounds`
  - `outbounds`
  - `route`
- If the client asks for a link, give it the `vless://` URI

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
