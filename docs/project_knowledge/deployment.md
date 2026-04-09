# Deployment

## Goal

Bring up a small private access stack on Debian VPS infrastructure with:

- `x-ui`
- `Xray Reality`
- optional `Caddy + forwardproxy@naive`
- `mtg`
- optional `Sing-box / SFM` client configs

## Server Prerequisites

- Debian 12 VPS
- public IPv4
- root or sudo access
- open firewall ports

## Server Sizing

### Minimum

- `1 vCPU`
- `2 GB RAM`
- `10 GB SSD`
- `1 public IPv4`

Use this when:

- the server is for personal use
- user count is small
- traffic is light or occasional
- the main heavy case is Telegram and ordinary browsing

### Recommended

- `2 vCPU`
- `2-4 GB RAM`
- `10-20 GB SSD`
- `1 public IPv4`

Use this when:

- you want more CPU headroom
- you are migrating from an old server and want less risk
- several people may use it in parallel
- you prefer operational margin over saving a few dollars

### Practical Note

For a small private setup, an `e2-small` class VM is usually enough.

If you want the safer default and do not want to think much about resizing later, choose an `e2-medium` class VM.

## Recommended Open Ports

### Xray + MTProto VPS

- `80`
- `443`
- `2053`
- `2083`
- `2087`
- `2096`
- `29750`
- `8443`

### NaiveProxy VPS or Public IP

- `80`
- `443`

## Basic Order

1. Update the server and install base tools.
2. Install `x-ui`.
3. Set the panel credentials.
4. Create `Reality` inbounds.
5. Install `mtg`.
6. If needed, bring up `NaiveProxy` on a separate VPS or public IP.
7. Generate user configs.
8. Test from a real client before migration.

## x-ui Notes

- the panel can run directly by IP
- if using IP certificates, Let's Encrypt may require a short-lived certificate profile
- keep the panel path non-default

## MTProto Notes

- `8443` is a good default for Telegram-native proxy
- use fake TLS `ee` secrets
- publish only the final Telegram link, not private server internals

## NaiveProxy Notes

- treat `NaiveProxy` as a separate transport stack, not as "one more `Reality` port"
- recommended server stack: `Caddy + github.com/klzgrad/forwardproxy@naive`
- recommended topology: separate VPS or at least separate public IP
- keep the DNS record `DNS only` if using Cloudflare
- keep `:443` first in the `Caddyfile`
- use `basic_auth`, `hide_ip`, `hide_via`, and `probe_resistance`

## Client Configs

Use `scripts/generate_singbox_config.py` to build a reusable `Sing-box / SFM` profile.

Reality example:

```bash
python3 scripts/generate_singbox_config.py \
  --mode reality \
  --server YOUR_SERVER_IP \
  --uuid YOUR_UUID \
  --public-key YOUR_REALITY_PUBLIC_KEY \
  --short-id YOUR_SHORT_ID \
  --sni www.google.com \
  --pretty
```

Naive example:

```bash
python3 scripts/generate_singbox_config.py \
  --mode naive \
  --server naive.example.com \
  --username YOUR_NAIVE_USERNAME \
  --password YOUR_NAIVE_PASSWORD \
  --sni naive.example.com \
  --pretty
```

## Client App Mapping

Use the right format for the right client.

### SFM

Correct name:

- `SFM`
- `sing-box for Apple`

Use this when you want:

- a local JSON config
- split tunneling
- direct rules for selected domains
- full `sing-box` control

Input format:

- full local `sing-box` client JSON
- not an arbitrary JSON snippet
- not just a `vless://` URI wrapped in JSON

Where to paste:

- create a local profile
- open profile content
- paste the JSON

What that JSON should usually contain:

- `dns`
- `inbounds`
- `outbounds`
- `route`

Typical operator intent:

- `tun` inbound for system traffic
- direct routing for selected domains
- proxy routing for everything else
- `vless` outbound with `Reality`
- `naive` outbound for the backup path

### Hiddify Next

Input format:

- `vless://` link
- or subscription URL

Where to paste:

- import from clipboard
- import from link
- or add profile manually

### v2rayN

Input format:

- `vless://` link

Where to paste:

- import from clipboard
- import URL
- or scan QR if you generated one elsewhere

### v2rayNG

Input format:

- `vless://` link

Where to paste:

- import from clipboard
- manual import
- scan QR

## Operational Rule

- give `SFM` a proper `sing-box` config with real routing and DNS sections
- give `Hiddify Next`, `v2rayN`, and `v2rayNG` the `vless://` link
- describe `NaiveProxy` as a separate backup stack in your runbooks
