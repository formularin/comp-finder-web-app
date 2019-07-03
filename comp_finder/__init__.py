"""Checks WCA competitions (in the USA) and records information about ones in specified states.

Dependencies:
Python 3.x

Usage:
comp_finder.sh /path/to/output_file.txt current_location /path/to/states_file.txt

Current location should be an address or coordinates (or any other acceptable input to google maps).
Spaces in current location should be replaced by '-' chars
ex.
1600-Pennsylvania-Ave-NW,-Washington,-DC-20500

States File should contain the names of states separated by newline characters.
"""