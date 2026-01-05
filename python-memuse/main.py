import os
import sys
import psutil
import random
import string
from datetime import datetime


def get_memory_usage():
    """Returns the current memory usage of the process in MB."""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024)


def generate_random_string(length):
    """Generates a random string of a given length."""
    letters = string.ascii_letters + string.digits
    return "".join(random.choice(letters) for _ in range(length))


def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <N>")
        sys.exit(1)

    try:
        n_items = int(sys.argv[1])
    except ValueError:
        print("Error: N must be an integer.")
        sys.exit(1)

    # 1. Print initial memory usage
    initial_memory = get_memory_usage()
    print(f"Initial memory usage: {initial_memory:.2f} MB")

    # 2. Create and populate the dictionary
    data_dict = {}
    print(f"Inserting {n_items} items into the dictionary...")
    for _ in range(n_items):
        key = generate_random_string(128)
        value = (
            generate_random_string(32),
            generate_random_string(32),
            datetime.now(),
        )
        data_dict[key] = value

    # 3. Print final memory usage
    final_memory = get_memory_usage()
    print(f"Final memory usage:   {final_memory:.2f} MB")

    # 4. Calculate and print the dictionary's memory footprint
    dict_memory = final_memory - initial_memory
    print(f"Dict memory usage:    {dict_memory:.2f} MB")


if __name__ == "__main__":
    main()
