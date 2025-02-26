Approach-1
the first approach is to search for linear search on the file completely to find out the logs for a particular day but the problem here is the file size so we use streaming processing to read file line by line.
use the efficient string matching for the logs extraction and then writing the logs in output file.
pros:
-> not using whole file to process at a time 
cons:
-> searching the whole file for logs.

Approch-2
since the log file is contionously generated the logs in the file be in the sorted manner we can use binary search for the following task and extract the log details for the same.
so we read the number of line and then compare the mid line date to our date and then search for the matching date.

note: the filepath in the solution should be replaced by the actual file path of the logs file
