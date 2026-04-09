# Architecture

## Main Components

### VPS

One or more VPS instances run the access stack and expose the public ports.

### x-ui

`x-ui` is the operator panel. It manages `Xray`, stores inbound definitions, and gives the operator a simple surface for creating or changing clients.

Treat it as an operator-only surface:

- keep it behind SSH tunneling, a private VPN, or a strict source IP allowlist
- do not publish the admin port to the open internet by default

Typical files:

- `/etc/x-ui/x-ui.db`
- `/usr/local/x-ui`

### Xray

`Xray` handles the actual `VLESS + Reality` listeners:

- one main path on `443`
- optional fallback paths such as `2053` and `2083`

These fallback ports are still part of the same `Xray + Reality` family.

### NaiveProxy

`NaiveProxy` is a separate access stack based on `Caddy + forwardproxy@naive`.

Recommended topology:

- separate VPS
- or at least a separate public IP
- dedicated hostname such as `naive.example.com`

This is stronger diversification than "just add another `Reality` port" because the client and server stacks are different.

### mtg

`mtg` provides a Telegram-native `MTProto` proxy, usually on `8443`, with a fake TLS secret.

### Sing-box / SFM

End users consume the server with local JSON configs, usually on macOS or iPhone-compatible clients that can import `sing-box` style configs.

The templates in this repo default to full tunnel. Split-tunnel bypass rules are an explicit operator choice.

## Typical Flow

1. User device opens the local `tun` config.
2. DNS for selected domains stays local and direct.
3. All other traffic goes through either:
   - `VLESS + Reality` as the main path
   - `NaiveProxy` as the cross-stack backup path
4. Telegram can also use `MTProto` directly if needed.

## Optional Domain Layer

The core `Reality` paths do not require the operator's own domain.

A separate domain is mainly useful for:

- panel convenience
- cleaner TLS handling
- optional `gRPC + TLS` routes
- `NaiveProxy` hostnames and probe-resistant `Caddy` setup
