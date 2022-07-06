# Creates two CPU-Utilization-Entries. One at start_timee and one at end_time.
# Both timestamps are converted from microseconds to seconds (and cut to give an integer number)
# Both set to 0.5
def get_default_cpu_utilization(start_time: int, end_time: int) -> list[tuple[int, float]]:
    default_cpu_utilization = 0.5
    cpu_utilization = list[tuple[int, float]]()
    formatted_start_time = int(start_time / 10**6)
    formatted_end_time = int(end_time / 10**6)
    cpu_utilization.append((formatted_start_time, default_cpu_utilization))
    cpu_utilization.append((formatted_end_time, default_cpu_utilization))
    return cpu_utilization
