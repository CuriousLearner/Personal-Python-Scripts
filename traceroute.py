import subprocess
import trparse
import argparse

parser = argparse.ArgumentParser(description='Traceroute parser')

parser.add_argument('-c', '--count', action="store", dest="c", type=int, required=True)
parser.add_argument('-d', '--destination', action="store", dest="d", required=True)

results = parser.parse_args()

count = results.c
dest = results.d

global_ip_list = list()
global_hop_count_list = list()


def get_ip_and_latency(count, dest_ip):
    traceroute_output = subprocess.check_output(['traceroute', dest_ip])
    traceroute_ast = trparse.loads(traceroute_output)
    hops_count = len(traceroute_ast.hops)

    latency_ip_list = list()
    latency_count_for_hops = list()
    for i in range(hops_count):
        probes = traceroute_ast.hops[i].probes
        time_list = [x.rtt for x in probes]
        ip_list = [x.ip for x in probes]
        min_latency = min(time_list)
        min_latency_ip = ip_list[time_list.index(min_latency)]
        latency_count_for_hops.append(min_latency)
        latency_ip_list.append(min_latency_ip)
        
    global_ip_list.append(latency_ip_list)
    global_hop_count_list.append(latency_count_for_hops)

for i in range(count):
    get_ip_and_latency(count, dest)

final_hop_latency = list()


for x in zip(*global_hop_count_list):
    try:
        final_hop_latency.append(sum(x)/float(len(x)))
    except TypeError:
        valid_latency_list = [a for a in x if isinstance(a, float) or isinstance(a, int)]
        if len(valid_latency_list) == 0:
            final_hop_latency.append("*")
            break
        avg_latency = sum(valid_latency_list) / float(len(valid_latency_list))
        final_hop_latency.append(avg_latency)

for i, j in zip(global_ip_list[0], final_hop_latency):
    if i and j:
        if str(j) == "*":
            print str(i) + "\t" + str(j)
        else:
            print str(i) + "\t" + str(j) + " ms"
    else:
        print "*" + "\t\t" + str(j)
