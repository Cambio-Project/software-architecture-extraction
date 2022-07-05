# Creates two CPU-Utilization-Entries. One at start_timee and one at end_time.
# Both set to 0.5
def get_default_cpu_utilization(start_time: int, end_time: int) -> list[tuple[int, float]]:
    default_cpu_utilization = 0.5
    cpu_utilization = list[tuple[int, float]]()
    cpu_utilization.append((start_time, default_cpu_utilization))
    cpu_utilization.append((end_time, default_cpu_utilization))
    return cpu_utilization
