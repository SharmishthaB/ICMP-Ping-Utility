# ICMP-Ping-Utility

This project implements a simple ICMP-based ping utility using Python. The utility allows users to test network reachability and measure response times for a specified hostname or IP address. This project was developed as part of a computer networks course to demonstrate the basics of ICMP and network programming.

Features
- Sends ICMP echo request packets to a specified hostname or IP address
- Measures response times and calculates packet loss statistics
- Displays results in a user-friendly format, including minimum, maximum, and average round-trip times
- Simple graphical user interface (GUI) built using tkinter

Requirements
- Python 3.x
- tkinter library (for GUI)
- socket library (for network programming)
- struct library (for packet creation)

Usage
1. Clone the repository or download the code.
2. Run the script using Python (e.g., python icmp.py).
3. Enter a hostname or IP address in the GUI and click "Start Ping".
4. The utility will display the results, including response times and packet loss statistics.
