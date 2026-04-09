import argparse
import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = (
    Path(__file__).resolve().parents[1] / "scripts" / "generate_singbox_config.py"
)
SPEC = importlib.util.spec_from_file_location("generate_singbox_config", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def make_args(**overrides):
    values = {
        "mode": "reality",
        "server": "1.2.3.4",
        "port": 443,
        "uuid": "00000000-0000-0000-0000-000000000000",
        "public_key": "PUBLIC_KEY",
        "short_id": "SHORT_ID",
        "username": None,
        "password": None,
        "sni": None,
        "insecure_concurrency": 0,
        "quic": False,
        "quic_congestion_control": "",
        "direct_domains": "",
        "direct_suffixes": "",
    }
    values.update(overrides)
    return argparse.Namespace(**values)


class GenerateSingboxConfigTests(unittest.TestCase):
    def test_reality_defaults_to_google_sni(self):
        args = make_args(mode="reality")

        MODULE.apply_mode_defaults(args)
        config = MODULE.build_config(args)

        self.assertEqual(
            config["outbounds"][0]["tls"]["server_name"],
            MODULE.DEFAULT_REALITY_SNI,
        )

    def test_naive_defaults_sni_to_server(self):
        args = make_args(
            mode="naive",
            server="naive.example.com",
            uuid=None,
            public_key=None,
            short_id=None,
            username="user",
            password="pass",
        )

        MODULE.apply_mode_defaults(args)
        config = MODULE.build_config(args)

        self.assertEqual(
            config["outbounds"][0]["tls"]["server_name"], "naive.example.com"
        )

    def test_full_tunnel_is_default(self):
        args = make_args(mode="reality")

        MODULE.apply_mode_defaults(args)
        config = MODULE.build_config(args)

        self.assertEqual(config["dns"]["rules"], [config["dns"]["rules"][-1]])
        self.assertEqual(
            config["route"]["rules"],
            [
                {"action": "sniff"},
                {
                    "type": "logical",
                    "mode": "or",
                    "rules": [{"protocol": "dns"}, {"port": 53}],
                    "action": "hijack-dns",
                },
                {"ip_is_private": True, "outbound": "direct"},
            ],
        )

    def test_split_tunnel_rules_are_opt_in(self):
        args = make_args(
            mode="reality",
            direct_suffixes="ru,su,xn--p1ai",
            direct_domains="ya.ru,mail.ru",
        )

        MODULE.apply_mode_defaults(args)
        config = MODULE.build_config(args)

        self.assertEqual(
            config["dns"]["rules"][0]["domain_suffix"], ["ru", "su", "xn--p1ai"]
        )
        self.assertEqual(config["dns"]["rules"][1]["domain"], ["ya.ru", "mail.ru"])
        self.assertEqual(
            config["route"]["rules"][-2]["domain_suffix"], ["ru", "su", "xn--p1ai"]
        )
        self.assertEqual(config["route"]["rules"][-1]["domain"], ["ya.ru", "mail.ru"])


if __name__ == "__main__":
    unittest.main()
