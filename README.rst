chatserver-refactor
###################

Files for my blog post about refactoring terrible code. Still in progress.

**Contents:**

-   test_chatserver.py - Functional tests, should pass for all chatserver
    versions if you have a recent (or probably even not-so-recent) Twisted.
    Check the top of the file for how to run it.
-   dodiff.py - Updates the diffs. Check this file to find the order in which
    to read the chatserver versions and their associated diffs.
-   chatservers/ - All of the chatserver versions so far
-   diffs/ - Unified diffs between different chatserver versions
