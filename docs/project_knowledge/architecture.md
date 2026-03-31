# Architecture

## Main Components

### VPS

The VPS runs the access stack and exposes the public ports.

### x-ui

`x-ui` is the operator panel. It manages `Xray`, stores inbound definitions, and gives the operator a simple surface for creating or changing clients.

Typical files:

- `/etc/x-ui/x-ui.db`
- `/usr/local/x-ui`

### Xray

`Xray` handles the actual `VLESS + Reality` listeners:

- one main path on `443`
- optional fallback paths such as `2053` and `2083`

### mtg

`mtg` provides a Telegram-native `MTProto` proxy, usually on `8443`, with a fake TLS secret.

### Sing-box / SFM

End users consume the server with local JSON configs, usually on macOS or iPhone-compatible clients that can import `sing-box` style configs.

## Typical Flow

1. User device opens the local `tun` config.
2. DNS for selected domains stays local and direct.
3. All other traffic goes through `VLESS + Reality`.
4. Telegram can also use `MTProto` directly if needed.

## Optional Domain Layer

The core `Reality` paths do not require the operator's own domain.

A separate domain is mainly useful for:

- panel convenience
- cleaner TLS handling
- optional `gRPC + TLS` routes
