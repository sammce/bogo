import random
import statistics
from math import factorial
from time import perf_counter, sleep

from samutil.formatting import Formatter as fmt

# ---- Important constants ----
LIST_LENGTH = 4
ITERATIONS = 20
BAR_CHART_DELAY = 0.1 # Seconds
BAR_CHART_CHAR = "bogo" # The chart is made up of this string
# -----------------------------

# --- Less important, but configurable -----------------------
ROUND_TO = 4  # Decimal places
SEPARATOR_LEN = 40 # Length of horizontal divider printed after each pass
PERMS_PER_SECOND = 220 # Rough estimate for analytical purposes
# ------------------------------------------------------------

# If the pass completes in less than (n / 2)!, it counts as fast.
fast_threshold_without_delay = factorial(LIST_LENGTH // 2) * (1 / PERMS_PER_SECOND)
fast_threshold_with_delay = factorial(LIST_LENGTH // 2) * BAR_CHART_DELAY + fast_threshold_without_delay

print(f"list length = {LIST_LENGTH}, iterations = {ITERATIONS}, delay = {BAR_CHART_DELAY}")
print("-" * SEPARATOR_LEN)
# Output expected time to sort
expected_duration = round(factorial(LIST_LENGTH) * BAR_CHART_DELAY, ROUND_TO)
print("Expected duration of each pass (n! x delay):")
print("  - " + fmt.info(fmt.bold(expected_duration)), "seconds")
print("  - " + fmt.info(fmt.bold(round(expected_duration / 60, ROUND_TO))), "minutes")
print("  - " + fmt.info(fmt.bold(round(expected_duration / 3600, ROUND_TO))), "hours")

def clear_n_lines(n: int):
    """
    Clears n lines from the terminal.
    """
    for _ in range(n):
        print("\033[A                             \033[A")

def colored_time(time: float | int, threshold = fast_threshold_with_delay):
    """
    Determine whether or not a time is 'fast' using the threshold, and format
    the color of the time accordingly.
    """
    return fmt.success(time) if time <= threshold else fmt.error(time)

def output_barchart_from(items: list):
    """
    Outputs a bar chart from a list of items.
    """
    bars = []
    # Because the bar chart is vertical, we have to 
    # loop from N -> 1 and add a bar character if the item is >= i.
    for i in range(LIST_LENGTH, 0, -1):
        string = ""
        for item in items:
            string += (
                " " + (BAR_CHART_CHAR if item >= i else " " * len(BAR_CHART_CHAR)) + " "
            )

        bars.append(string)

    clear_n_lines(LIST_LENGTH)

    for bar in bars:
        print(fmt.info(bar))

    sleep(BAR_CHART_DELAY)

def bogo_sort():
    """
    Bogo sort is a simple sorting algorithm that works by repeatedly shuffling
    the list of items until it is in the correct order.
    """
    # Setup list of random numbers
    items = list(range(1, LIST_LENGTH + 1))
    sorted_items = sorted(items)
    random.shuffle(items)

    # If the initial shuffle is bang on, the time taken is 0, which causes errors.
    sleep(BAR_CHART_DELAY)

    print("\n" * LIST_LENGTH)
    attempts = 1

    # Actual sorting
    while items != sorted_items:
        random.shuffle(items)
        output_barchart_from(items)
        attempts += 1

    # Clears the bar chart
    clear_n_lines(LIST_LENGTH + 1)
    return attempts

if __name__ == "__main__":
    print("-" * SEPARATOR_LEN)

    results = []
    for iteration in range(ITERATIONS):
        t1 = perf_counter()
        permutations = bogo_sort()
        t2 = perf_counter()

        res = round(t2 - t1, ROUND_TO)
        real_time = round(res - (BAR_CHART_DELAY * permutations), ROUND_TO)
        results.append(res)
        backspace = '\b'
        print(f"Pass {iteration + 1}:              {backspace * len(str(iteration + 1))}  {colored_time(res)} seconds")
        print(f"Real time:           ~{colored_time(real_time, fast_threshold_without_delay)} seconds")
        print(f"Permutations:         {fmt.magenta(permutations)}")

        if permutations == 1:
            print(fmt.bold(fmt.success("First try!")))
        else:
            print(f"Permutations/second: ~{fmt.info(round(permutations / real_time))}")
        print("-" * SEPARATOR_LEN)

    stdev = round(statistics.stdev(results), ROUND_TO)

    print(f"Total time             {fmt.bold(round(sum(results), ROUND_TO))} seconds")
    print(f"Average                {fmt.bold(round(sum(results) / len(results), ROUND_TO))} seconds")
    print(f"Expected average       {fmt.bold(round(expected_duration, ROUND_TO))} seconds")
    print(f"Standard deviation     {fmt.bold(stdev)} seconds")

