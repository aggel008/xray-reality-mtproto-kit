# Project

## What This Project Is

`xray-reality-naive-mtproto-kit` is a small deployment kit for running a private access stack on one or more VPS instances.

It combines:

- `VLESS + Reality` for the main access path
- `NaiveProxy` for a cross-stack backup path
- `MTProto` for Telegram-native access
- `x-ui` for operator management of the `Xray` side
- `Sing-box / SFM` JSON configs for end users

## Who It Serves

- solo operators
- small private teams
- family access setups
- staged server migrations where zero lockout matters

## Main Deliverables

- reusable deploy docs
- full-tunnel client config templates for `Reality` and `Naive`
- small config generation tooling
- example `Caddy` configuration for `NaiveProxy`
- operational patterns that are easy to hand off to another agent
