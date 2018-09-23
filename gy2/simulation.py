# 1. find possible circuits
# 2. find available circuits from possible circuits
#   2.1. a circuit is available if all of the links are free
# 3. build flow
#   3.1. reserve all of the links in the circuit
# 4. teardown flow if enough time has passed

import json

# helpers
def find_possible_circuits(demand):
    start = demand["end-points"][0]
    end = demand["end-points"][1]
    possible_circuits = []

    for circuit in topology["possible-circuits"]:
        if circuit[0] == start and circuit[-1] == end:
            possible_circuits.append(circuit)

    return possible_circuits


def find_link(start, end):
    for link in topology["links"]:
        if link["points"][0] == start and link["points"][1] == end:
            return link


def find_first_available_circuit(possible_circuits):
    for circuit in possible_circuits:
        is_circuit_available = True

        for i in range(len(circuit) - 1):
            link = find_link(circuit[i], circuit[i + 1])
            if link["reserved"]:
                is_circuit_available = False
                break

        if is_circuit_available:
            return circuit

    return None


def build_flow(circuit, start_time):
    for i in range(len(circuit) - 1):
        link = find_link(circuit[i], circuit[i + 1])
        link["reserved"] = True

    print "foglalas: " + circuit[0] + "<->" + \
        circuit[-1] + " st: " + str(start_time) + " - sikeres"


def teardown_flow(circuit, start_time):
    for i in range(len(circuit) - 1):
        link = find_link(circuit[i], circuit[i + 1])
        link["reserved"] = False

    print "felszabaditas: " + circuit[0] + \
        "<->" + circuit[-1] + " st: " + str(start_time)


# load data
with open("cs1.json", "r") as read_file:
    topology = json.load(read_file)

# main
duration = topology["simulation"]["duration"]
demands = topology["simulation"]["demands"]

for link in topology["links"]:
    link["reserved"] = False

for i in range(duration):
    print str(i)

    for demand in demands:
        if i == demand["end-time"] and "circuit-in-use" in demand:
            teardown_flow(demand["circuit-in-use"], demand["start-time"])
            demand.pop("circuit-in-use")
        elif i == demand["start-time"]:
            possible_circuits = find_possible_circuits(demand)
            available_circuit = find_first_available_circuit(possible_circuits)
            
            if available_circuit is not None:
                demand["circuit-in-use"] = available_circuit
                build_flow(available_circuit, demand["start-time"])
