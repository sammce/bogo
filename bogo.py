import random
import statistics
from math import factorial
from time import perf_counter, sleep

from samutil.formatting import Formatter as fmt

LIST_LENGTH = 4

SEPARATOR_LEN = 40

PERMS_PER_SECOND = 200
FAST_THRESHOLD_WITHOUT_DELAY = (factorial(LIST_LENGTH // 2)) * (1 / PERMS_PER_SECOND)
FAST_THRESHOLD_WITH_DELAY = FAST_THRESHOLD_WITHOUT_DELAY * 50

BAR_CHART_DELAY = 0.1 # Seconds
BAR_CHART_CHAR = "bogo"

ITERATIONS = 20
ROUND_TO = 4  # Decimal places

print(f"list length = {LIST_LENGTH}, iterations = {ITERATIONS}, delay = {BAR_CHART_DELAY}")

def clear_n_lines(n: int):
    for _ in range(n):
        print("\033[A                             \033[A")

def colored_time(time: float | int, threshold = FAST_THRESHOLD_WITH_DELAY):
    """
    Determine whether or not a time is 'fast' using the threshold, and format
    the color of the time accordingly.
    """
    return fmt.success(time) if time <= threshold else fmt.error(time)

def output_barchart_from(items: list):
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

    print("\n" * LIST_LENGTH)
    attempts = 0

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
        
        print(f"Pass {iteration + 1}:               {colored_time(res)} seconds")
        print(f"Real time:           ~{colored_time(real_time, FAST_THRESHOLD_WITHOUT_DELAY)} seconds")
        print(f"Permutations:         {fmt.magenta(permutations)}")
        print(f"Permutations/second: ~{fmt.info(round(permutations / real_time))}")
        print("-" * SEPARATOR_LEN)

    stdev = round(statistics.stdev(results), ROUND_TO)

    print(f"Total time             {round(sum(results), ROUND_TO)} seconds")
    print(f"Average                {round(sum(results) / len(results), ROUND_TO)} seconds")
    print(f"Standard deviation     {stdev} seconds")

