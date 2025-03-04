import json

with open("sample-data.json") as file:
    data = json.load(file)
print("Interface Status")
print("=" * 80)
print("{:<50} {:<20} {:<10} {:<10}".format("DN", "Description", "Speed", "MTU"))
print("-" * 80)
for item in data["imdata"]:
    attributes = item["l1PhysIf"]["attributes"]
    print("{:<50} {:<20} {:<10} {:<10}".format(attributes["dn"], attributes["descr"], attributes["speed"], attributes["mtu"]))
