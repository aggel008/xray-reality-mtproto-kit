#!/usr/bin/env python3
import argparse
import json


DEFAULT_DIRECT_DOMAINS = [
    "ya.ru",
    "yandex.ru",
    "dzen.ru",
    "vk.com",
    "mail.ru",
    "gosuslugi.ru",
    "ozon.ru",
    "wildberries.ru",
    "avito.ru",
]


def build_common_config(proxy_outbound: dict, direct_domains: list[str]) -> dict:
    return {
        "log": {"level": "info"},
        "dns": {
            "servers": [
                {
                    "type": "https",
                    "tag": "doh-remote",
                    "server": "1.1.1.1",
                    "server_port": 443,
                    "path": "/dns-query",
                    "tls": {
                        "enabled": True,
                        "server_name": "cloudflare-dns.com",
                    },
                    "detour": "proxy",
                },
                {
                    "type": "local",
                    "tag": "dns-local",
                },
            ],
            "rules": [
                {
                    "domain_suffix": ["ru", "su", "xn--p1ai"],
                    "action": "route",
                    "server": "dns-local",
                    "strategy": "ipv4_only",
                },
                {
                    "domain": direct_domains,
                    "action": "route",
                    "server": "dns-local",
                    "strategy": "ipv4_only",
                },
                {
                    "action": "route",
                    "server": "doh-remote",
                    "strategy": "ipv4_only",
                },
            ],
            "final": "doh-remote",
        },
        "inbounds": [
            {
                "type": "tun",
                "tag": "tun-in",
                "address": ["172.19.0.1/30"],
                "auto_route": True,
                "strict_route": True,
                "mtu": 1400,
            }
        ],
        "outbounds": [
            proxy_outbound,
            {
                "type": "direct",
                "tag": "direct",
            },
            {
                "type": "block",
                "tag": "block",
            },
        ],
        "route": {
            "auto_detect_interface": True,
            "default_domain_resolver": "dns-local",
            "final": "proxy",
            "rules": [
                {"action": "sniff"},
                {
                    "type": "logical",
                    "mode": "or",
                    "rules": [
                        {"protocol": "dns"},
                        {"port": 53},
                    ],
                    "action": "hijack-dns",
                },
                {
                    "ip_is_private": True,
                    "outbound": "direct",
                },
                {
                    "domain_suffix": ["ru", "su", "xn--p1ai"],
                    "outbound": "direct",
                },
                {
                    "domain": direct_domains,
                    "outbound": "direct",
                },
            ],
        },
    }


def build_reality_outbound(args: argparse.Namespace) -> dict:
    return {
        "type": "vless",
        "tag": "proxy",
        "server": args.server,
        "server_port": args.port,
        "uuid": args.uuid,
        "packet_encoding": "xudp",
        "tls": {
            "enabled": True,
            "server_name": args.sni,
            "utls": {
                "enabled": True,
                "fingerprint": "chrome",
            },
            "reality": {
                "enabled": True,
                "public_key": args.public_key,
                "short_id": args.short_id,
            },
        },
    }


def build_naive_outbound(args: argparse.Namespace) -> dict:
    outbound = {
        "type": "naive",
        "tag": "proxy",
        "server": args.server,
        "server_port": args.port,
        "username": args.username,
        "password": args.password,
        "insecure_concurrency": args.insecure_concurrency,
        "quic": args.quic,
        "tls": {
            "enabled": True,
            "server_name": args.sni,
        },
    }
    if args.quic_congestion_control:
        outbound["quic_congestion_control"] = args.quic_congestion_control
    return outbound


def build_config(args: argparse.Namespace) -> dict:
    extra_domains = [d.strip() for d in args.direct_domains.split(",") if d.strip()]
    direct_domains = DEFAULT_DIRECT_DOMAINS + extra_domains
    proxy_outbound = (
        build_reality_outbound(args)
        if args.mode == "reality"
        else build_naive_outbound(args)
    )
    return build_common_config(proxy_outbound, direct_domains)


def validate_args(args: argparse.Namespace) -> None:
    if args.mode == "reality":
        required = (
            ("--uuid", args.uuid),
            ("--public-key", args.public_key),
            ("--short-id", args.short_id),
        )
    else:
        required = (
            ("--username", args.username),
            ("--password", args.password),
        )

    missing = [flag for flag, value in required if not value]
    if missing:
        raise SystemExit(
            f"Missing required arguments for --mode {args.mode}: {', '.join(missing)}"
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a Sing-box / SFM config for a Reality or Naive proxy."
    )
    parser.add_argument(
        "--mode",
        choices=("reality", "naive"),
        default="reality",
        help="Outbound type to generate",
    )
    parser.add_argument("--server", required=True, help="Server IP or hostname")
    parser.add_argument("--uuid", help="VLESS client UUID")
    parser.add_argument("--public-key", help="Reality public key")
    parser.add_argument("--short-id", help="Reality short ID")
    parser.add_argument("--username", help="NaiveProxy username")
    parser.add_argument("--password", help="NaiveProxy password")
    parser.add_argument(
        "--sni",
        default="www.google.com",
        help="Reality SNI or Naive TLS server_name",
    )
    parser.add_argument("--port", type=int, default=443, help="Server port")
    parser.add_argument(
        "--insecure-concurrency",
        type=int,
        default=0,
        help="NaiveProxy concurrent tunnel count",
    )
    parser.add_argument(
        "--quic",
        action="store_true",
        help="Use QUIC for NaiveProxy instead of HTTP/2",
    )
    parser.add_argument(
        "--quic-congestion-control",
        default="",
        help="Optional NaiveProxy QUIC congestion control value",
    )
    parser.add_argument(
        "--direct-domains",
        default="",
        help="Comma-separated domains that should bypass the proxy",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print JSON output",
    )
    args = parser.parse_args()
    validate_args(args)

    config = build_config(args)
    if args.pretty:
        print(json.dumps(config, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(config, ensure_ascii=False))


if __name__ == "__main__":
    main()
