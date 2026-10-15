import json
from pathlib import Path
from xml.etree import ElementTree


policies = {}
for name in ("dummy-deny-host", "dummy-deny-fwd"):
    root = ElementTree.parse(Path("/etc/firewalld/policies") / f"{name}.xml").getroot()
    policies[name] = {
        "target": root.attrib["target"],
        "priority": int(root.attrib["priority"]),
        "ingress": [zone.attrib["name"] for zone in root.findall("ingress-zone")],
        "egress": [zone.attrib["name"] for zone in root.findall("egress-zone")],
        "destinations": [
            [rule.attrib["family"], rule.find("destination").attrib["address"]]
            for rule in root.findall("rule")
        ],
        "drops": len(root.findall("rule/drop")),
        "accepts": len(root.findall("rule/accept")),
    }

print(json.dumps(policies))
