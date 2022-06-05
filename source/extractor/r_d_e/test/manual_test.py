import json

from extractor.r_d_e.LibReDE_Host import LibReDE_Host, get_hosts_with_default_cpu_utilization
from extractor.r_d_e.LibReDE_Service import LibReDE_Service, get_services

trace = json.loads(open("trace_stub.json", "r").read())
hosts: list[LibReDE_Host] = get_hosts_with_default_cpu_utilization(trace)
services: dict[str, list[LibReDE_Service]] = get_services(trace, hosts)

for host in hosts:
    print("host: " + str(host))
print("----------------------")
for service_key in services.keys():
    print("services of operation <" + service_key + ">:")
    for single_service in services[service_key]:
        print(single_service)
    print()
