[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=ipeternella_algorithms&metric=alert_status)](https://sonarcloud.io/dashboard?id=ipeternella_algorithms)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=ipeternella_algorithms&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=ipeternella_algorithms)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=ipeternella_algorithms&metric=security_rating)](https://sonarcloud.io/dashboard?id=ipeternella_algorithms)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=ipeternella_algorithms&metric=reliability_rating)](https://sonarcloud.io/dashboard?id=ipeternella_algorithms)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=ipeternella_algorithms&metric=bugs)](https://sonarcloud.io/dashboard?id=ipeternella_algorithms)
[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=ipeternella_algorithms&metric=sqale_index)](https://sonarcloud.io/dashboard?id=ipeternella_algorithms)

# Algorithms and Data Structures

🔬 A repo with Pythonic implementations of some algorithms and their underlying data structures. 🧪

## Table of Contents

The following classical algorithms are covered by this repo and written in modern Python, which includes the use of type hints and generic types support. Also, `pytest` is the main testing framework used to guarantee that the algorithms are operating as expected:

- [Fundamental Algorithms](#fundamental-algorithms)
  - [Singly Linked List](#singly-linked-List)
  - [Queues](#queues)
  - [Stacks](#stacks)
- [Searching Algorithms](#searching-algorithms)
  - [Binary Search For Lists](#binary-search-for-lists)

## Fundamental Algorithms

The following fundamental algorithms are considered fundamental as they are the basis for many other more complex algorithms and data structures.

### Singly Linked List

Singly linked lists are covered and are built on top of a [single reference node](algorithms/data_containers/node_single_reference.py) which is used as a basic data container. By single reference node we mean a node that only holds one reference which is the to the next node in the list. Moreover, we consider linked lists that sustain a reference to the first and last nodes of the list which can be very useful to allow efficient operations on both edges of the list (this is the base for queues and stacks as well).

Algorithm implementation [here](algorithms/linked_lists/singly.py)

### Queues

Queues (FIFO -- First in, first Out -- data structures) are built here on top of the [singly linked list](#singly-linked-list) implementation because singly linked lists allows the following efficient operations:

- O(1) time complexity for insertions at the **end** of the list
- O(1) time complexity for removal (pop) of the first element of the list

Such efficient operations are required by FIFO data structures.

Algorithm implementation [here](algorithms/queues/fifo.py)

### Stacks

Stacks (LIFO -- Last in, first out -- data structures) are also built here on top of the [singly linked list](#singly-linked-list) data structures due to the efficient operations of the following operations:

- O(1) time complexity for insertions at the **beginning** of the list;
- O(1) time complexity for removal (pop) of the first element of the list

Such efficient operations are requried by LIFO data structures.

Algorithm implementation [here](algorithms/stacks/lifo.py)

## Searching Algorithms

We begin the section of algorithms by considering the classic binary search and move on to more complex data structures that are required by efficient implementations of **symbol tables** or **dictionaries**.

### Binary Search For Lists

The efficient searching algorithm for sorted lists is covered here.

Algorithm implementation [here](algorithms/searching/binary_search.py)
