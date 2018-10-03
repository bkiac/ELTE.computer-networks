import subprocess
import json
import csv
import datetime
import platform

# Helpers
def traceroute(max_ttl, host):
    return subprocess.Popen(["traceroute", "-n", "-m", str(max_ttl), host], stdout=subprocess.PIPE)


def ping(count, destination):
    return subprocess.Popen(["ping", "-c", str(count), destination], stdout=subprocess.PIPE)


# Main
first_n = 100
last_n = 100
max_hops = 30
ping_count = 10
max_processes = 10
date = datetime.datetime.now().strftime("%Y%m%d")
system = platform.system()

## Load data
with open("top-1m.csv", "r") as f:
    reader = csv.reader(f, delimiter=",")
    websites_from_csv = list(reader)
websites = [w[1] for w in websites_from_csv[:first_n]] + [w[1] for w in websites_from_csv[-last_n:]]

## Init stats
traceroute_stats = {
    "date": date,
    "system": system,
    "traces": []
}
ping_stats = {
    "date": date,
    "system": system,
    "pings": []
}

## Start processes
for i in range(0, len(websites), max_processes):
    traceroute_processes = []
    ping_processes = []

    for j in range(i, i + max_processes):
        print "> trace routing to " + websites[j] + " (" + str(j + 1) + "/" + str(len(websites)) + ")"
        traceroute_processes.append({
            "target": websites[j],
            "process": traceroute(max_hops, websites[j])
        })

        print "> pinging " + websites[j] + " (" + str(j + 1) + "/" + str(len(websites)) + ")"
        ping_processes.append({
            "target": websites[j],
            "process": ping(ping_count, websites[j])
        })

    for p in traceroute_processes:
        result = p["process"].communicate()
        traceroute_stats["traces"].append({
            "target": p["target"],
            "output": result[0]
        })

    for p in ping_processes:
        result = p["process"].communicate()
        ping_stats["pings"].append({
            "target": p["target"],
            "output": result[0]
        })

print "> dumping json"

## Store stats in json
with open("traceroute.json", "w") as f:
    json.dump(traceroute_stats, f)

with open("ping.json", "w") as f:
    json.dump(ping_stats, f)
