# Creates a default cpu_utilization-representation with every entry representing the utilization of <default_cpu_utilization>
def get_default_cpu_utilization(start_time: int, end_time: int) -> list[tuple[int, int]]:
    default_cpu_utilization = 1000
    time_granularity = 100
    cpu_utilization = list[tuple[int, int]]()
    current_time = start_time
    while current_time <= end_time:
        cpu_timestamp = (current_time, default_cpu_utilization)
        cpu_utilization.append(cpu_timestamp)
        current_time += time_granularity
    return cpu_utilization
