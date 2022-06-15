# Creates a default cpu_utilization-representation with every entry
# representing the utilization of <default_cpu_utilization>
# Creates ((<end_time> - <start_time>) / <time_granularity>)-many entries.
def get_default_cpu_utilization(start_time: int, end_time: int) -> list[tuple[int, float]]:
    default_cpu_utilization: float = 0.5
    time_granularity: int = 10
    cpu_utilization = list[tuple[int, float]]()
    current_time: int = start_time
    while current_time <= end_time:
        cpu_timestamp = (current_time, default_cpu_utilization)
        cpu_utilization.append(cpu_timestamp)
        current_time += time_granularity
    return cpu_utilization