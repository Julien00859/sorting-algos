#!/usr/bin/env python3

import json
import logging
from collections import defaultdict, ChainMap
from random import randrange, shuffle
from time import time
from sys import argv
from copy import copy
from os.path import isfile
from argparse import ArgumentParser
from pprint import pformat
from math import floor

from sorting_algorithms import algorithms, is_sorted, is_permutation_of


def main():
    # Get options from the command line
    parser = ArgumentParser()
    parser.add_argument("sizes", type=int, nargs="*", default=[128], help="Array sizes (default: 128)")
    parser.add_argument("-a", "--algo", dest="algos", action="append", help="Sorting algorithms to use (default: all)")
    parser.add_argument("--no-duplicates", dest="allow_duplicates", action="store_false", default=True, help="Force different values")
    parser.add_argument("--no-negatives", dest="allow_negatives", action="store_false", default=True, help="Force positives values")
    parser.add_argument("--save", action="store_true", default=False, help="Save times on disk")
    parser.add_argument("--array", action="store")
    parser.add_argument("-v", "--verbose", dest="verbosity", action="count", default=0, help="Increase verbosity")
    options = parser.parse_args()

    # Setup logging
    handler = logging.StreamHandler()
    handler.terminator = ""
    logging.basicConfig(
            format="%(message)s",
            level=["WARNING", "INFO", "DEBUG"][min(2, options.verbosity)],
            handlers=[handler])
    logging.debug("Options: %s\n\n", pformat(options.__dict__))

    # Filter algorithms
    logging.info("Filtering algorithms... ")
    if options.algos:
        functions = list(filter(lambda f: f.__name__ in options.algos, algorithms))
    else:
        functions = algorithms
    logging.info("ok\n")

    if options.array:
        rnd_array = json.loads(options.array)
        options.sizes = [len(rnd_array)]

    results = defaultdict(dict)
    for size in options.sizes:
        # Create and shuffle the array using given length and options
        logging.info("\n=====\n\n")
        logging.info("Array size: %d\n", size)
        if not options.array:
            logging.info("Setting array boundaries... ")
            if options.allow_negatives:
                lower_bound = floor(-size / 2)
                upper_bound = floor(size / 2)
            else:
                lower_bound = 0
                upper_bound = size
            logging.info("ok, from %d to %d\n", lower_bound, upper_bound - 1)
            
            logging.info("Creating and shuffling array... ")
            if options.allow_duplicates:
                rnd_array = [randrange(lower_bound, upper_bound) for _ in range(size)]
            else:
                rnd_array = list(range(lower_bound, upper_bound))
                shuffle(rnd_array)
            logging.info("ok, ")
        if size >= 5:
            sample = rnd_array[:2] + ["..."] + rnd_array[-2:]
            logging.info("[%s]\n", ", ".join(map(str, sample)))
        else:
            logging.info("[%s]\n", ", ".join(map(str, rnd_array)))

        for func in functions:
            # Sort the array using selected algorithm
            logging.info("\nAlgo: %s\n", func.__name__)

            logging.info("Copying... ")
            tmp = copy(rnd_array)
            logging.info("ok\n")

            logging.info("Sorting... ")
            before = time()
            sorted_array = func(tmp, size)
            after = time()
            logging.info("done, tooks %.4f seconds\n", after - before)

            logging.info("Validating... ")
            if is_sorted(sorted_array) and is_permutation_of(rnd_array, sorted_array):
                logging.info("ok\n")
                results[func.__name__]["{: 7d}".format(size)] = after - before
            else:
                logging.info("error\n")
                with open("error.json", "a") as file:
                    json.dump({"random": rnd_array, "sorted": sorted_array}, file)
                    file.write("\n")
                logging.warning("An error occured with algo %s. A full report has been written to \"error.json\"\n", func.__name__)

    # If saving the output is not required, exit now
    if not options.save:
        return

    if isfile("results.json"):
        # Merge previous results with new ones
        logging.info("Loading previous results... ")
        with open("results.json") as jsonfile:
            old_results = json.load(jsonfile)
        logging.info("ok\n")
        logging.info("Merging new results with previous ones... ")
        for algo in results.keys() | old_results.keys():
            results[algo] = dict(ChainMap(
                results.get(algo, {}),
                old_results.get(algo, {})))
        logging.info("ok\n")
    else:
        logging.warning("File \"results.json\" not found\n")

    # Save results to disk
    logging.info("Saving to disk... ")
    with open("results.json", "w") as jsonfile:
        json.dump(results, jsonfile, indent=2, sort_keys=True)
    logging.info("ok\n")

if __name__ == "__main__":
    main()

