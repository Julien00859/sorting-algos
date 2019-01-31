Sorting algorithms
==================

This project implements some sorting algorithms in python.

[Wikipedia](https://en.wikipedia.org/wiki/Sorting_algorithm)

	usage: sorting_algo [-h] [-a ALGOS] [-s NOTALGOS] [-i] [--linear] [--bounded]
	                    [--save] [--array ARRAY] [-v]
	                    [sizes [sizes ...]]
	
	positional arguments:
	  sizes                 Array sizes (default: [128])
	
	optional arguments:
	  -h, --help            show this help message and exit
	  -a ALGOS, --algo ALGOS
	                        Sorting algorithms to use (default: all)
	  -s NOTALGOS, --notalgo NOTALGOS
	                        Sorting algorithms to not use (default: none)
	  -i, --integer         Use intergers instead of strings
	  --linear              Shuffle a range of elements
	  --bounded             Randomly select values from -size/2 to size/2
	  --save                Save times on disk
	  --array ARRAY         Use this specific json array instead of a random one
	  -v, --verbose         Increase verbosity

Implemented so far:
-------------------

* Bogo
* Time
* Bubble
* Selection
* Insertion
  * Shifting
  * Swapping
* Shell
* Merge
  * Recursive
  * Iterative
* Quick
  * Recursive
* Heap
* Counting


Planned
-------

* Radix
