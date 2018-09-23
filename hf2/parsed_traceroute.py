import subprocess
import socket
import json
import csv

# helpers
def traceroute(max_ttl, host):
    p = subprocess.Popen(["traceroute", "-n", "-m", str(max_ttl), host], stdout=subprocess.PIPE)
    return p.communicate()


def is_valid_ip(address):
    try:
        socket.inet_aton(address)
        return address.count(".") == 3
    except:
        return False

def parse_traceroute_result(website, traceroute_result):
    parsed_result = {
        website: []
    }

    result_lines = traceroute_result[0].split("\n")
    path = result_lines[1:-1] # discard first and last line
    
    for router in path:
        sanitized_data = filter(lambda i: i != "ms", filter(None, router.split(" "))[1:])

        i = 0
        address = ""
        packets = []
        while i < len(sanitized_data):
            if is_valid_ip(sanitized_data[i]):
                address = sanitized_data[i]

                packets.append({
                    "latency": sanitized_data[i + 1],
                    "address": sanitized_data[i]
                })

                i += 2
            elif sanitized_data[i] == "*":
                packets.append({
                    "latency": "*",
                    "address": "*"
                })

                i += 1
            else:
                packets.append({
                    "latency": sanitized_data[i],
                    "address": address
                })

                i += 1
        
        parsed_result[website].append(packets)
    
    return parsed_result


# main
# load data
first_n = 100
last_n = 100
max_hops = 30

with open("top-1m.csv", "r") as read_file:
    reader = csv.reader(read_file, delimiter=",")
    websites_from_csv = list(reader)

websites_to_analyze = map(lambda i: i[1], websites_from_csv[:first_n]) + map(lambda i: i[1], websites_from_csv[-last_n:])

stats = []
for index, website in enumerate(websites_to_analyze):
    print "> running traceroute to " + website + " (" + str(index + 1) + "/" + str(first_n + last_n) + ")"

    traceroute_result = traceroute(max_hops, website)
    route = parse_traceroute_result(website, traceroute_result)
    stats.append(route)

print "> finished"

# store stats in json
with open("parsed-traceroute.json", "w") as write_file:
    json.dump(stats, write_file)
