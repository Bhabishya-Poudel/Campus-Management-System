CAMPUS SERVICE MANAGEMENT SYSTEM
================================

OVERVIEW
--------
A console-based Python program for managing campus service requests
(e.g. maintenance, IT help, facilities issues). Users can submit normal
and urgent requests, process them in the correct order, search for a
request by ID, and review pending and completed work.

The project is a CSCI 3 assignment that demonstrates core data
structures: a queue, a binary min-heap, a binary search tree, and a stack-
style history list.


REQUIREMENTS
------------
- Python 3 (standard library only; no extra packages needed)


HOW TO RUN
----------
From this folder, run:

    python3 main.py

A menu appears. Enter a number from 1 to 8 and follow the prompts.


MENU OPTIONS
------------
1. Add Normal Request     Enter ID, name, category, description.
2. Add Urgent Request     Same as above, plus a priority from 1 to 5
                          (1 = most urgent).
3. Process Next Request   Completes the next request and shows it.
4. Search for Request     Look up any request by its ID.
5. View Pending Requests  Lists pending normal and urgent requests.
6. View Completed Requests Lists all completed requests.
7. View Statistics        Shows total, pending, and completed counts,
                          plus pending normal vs. urgent counts.
8. Exit


HOW REQUESTS ARE PROCESSED
--------------------------
- Urgent requests are always processed before normal requests.
- Among urgent requests, the lowest priority number goes first. Ties are
  broken by arrival order (earlier request first).
- Normal requests are processed first-in, first-out (FIFO).
- Request IDs must be unique across both normal and urgent requests.
  Adding a duplicate ID is rejected.


DATA STRUCTURES USED
--------------------
- service_Request class   Holds one request: ID, name, category,
                          description, priority, and status
                          ("Pending" or "Completed").
- Queue (collections.deque)
                          Stores normal requests in arrival order (FIFO).
- Binary min-heap         Stores urgent requests as tuples
                          (priority, counter, request). The counter is a
                          unique, increasing number that breaks priority
                          ties so earlier requests come first. The heap
                          (insert and remove with sift up / sift down)
                          is written by hand in insertUrgent and
                          removeUrgent.
- Binary search tree      Indexes every request by ID for searching and
                          duplicate-ID detection (addToBST and
                          searchRequest).
- Pending list            Tracks all requests still waiting.
- Completed list          Keeps completed requests in the order they were
                          finished, tagged "normal" or "urgent". The most
                          recent entry is the one shown after processing.
                          (undoCompleted can restore an urgent request.)


FILE OVERVIEW
-------------
main.py                   The full program: classes plus the menu loop.
done.md / remaining.md    Working notes on design decisions and progress.
artifacts/                Supporting Word documents (data structure
                          tables) for the assignment.


EXAMPLE SESSION
---------------
1. Add a normal request (ID 1, "Leaky tap").
2. Add an urgent request (ID 2, "Power outage", priority 1).
3. Choose "Process Next Request": request 2 is completed first because it
   is urgent, then request 1 on the next process.
4. Choose "View Statistics" to see the updated counts.


NOTES AND LIMITATIONS
---------------------
- Data is stored in memory only. All requests are lost when the program
  exits.
- Request IDs must be positive whole numbers.
- Input is validated for numbers (ID and priority), but text fields may
  be left empty.
