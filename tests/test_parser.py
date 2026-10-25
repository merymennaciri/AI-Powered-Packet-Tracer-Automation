import unittest

from packet_tracer_ai.cli import parse_request


class ParseRequestTests(unittest.TestCase):
    def test_ospf_dhcp(self):
        result = parse_request("2 routers, 4 PCs per LAN, OSPF and DHCP")
        self.assertEqual(result["routers"], 2)
        self.assertEqual(result["pcs_per_lan"], 4)
        self.assertEqual(result["routing"], "ospf")
        self.assertTrue(result["dhcp"])
        self.assertFalse(result["deploy"])

    def test_router_on_a_stick(self):
        result = parse_request("1 router, 3 VLANs, router-on-a-stick and DHCP")
        self.assertEqual(result["routers"], 1)
        self.assertEqual(result["vlans"], 3)
        self.assertEqual(result["template"], "router_on_a_stick")

    def test_no_dhcp(self):
        result = parse_request("2 routers without DHCP, static routing")
        self.assertFalse(result["dhcp"])
        self.assertEqual(result["routing"], "static")

    def test_wan(self):
        result = parse_request("3 routers with WAN and OSPF")
        self.assertEqual(result["routers"], 3)
        self.assertTrue(result["has_wan"])
        self.assertEqual(result["template"], "multi_lan_wan")


if __name__ == "__main__":
    unittest.main()
