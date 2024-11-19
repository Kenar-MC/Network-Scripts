file_name = "raw_output.txt"

vlan_count = {}

with open(file_name, 'r') as file:
    for line in file:
        vlan = line.split()[1]
        if vlan in vlan_count:
            vlan_count[vlan] += 1
        else:
            vlan_count[vlan] = 1

for vlan, count in vlan_count.items():
    print("VLAN", vlan, "numarasında", count, "adet MAC adresi bulunmaktadır.")
