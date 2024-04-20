# Masscan and Nmap Integration Script

## Description
This Python script automates the process of conducting a quick port scan with Masscan, followed by a detailed service scan with Nmap on open ports. It is designed to run Masscan at high speed to quickly identify open ports, then uses Nmap to detect services running on these ports. Results from Nmap are saved to a text file for further analysis.

## Requirements
- Masscan: Must be installed and properly configured on your system.
- Nmap: Must also be installed and properly configured on your system.
- Python Version: 3.8 or higher.
- Python Libraries: `nmap`, `os`, `json`, `multiprocessing`.

Ensure that both Masscan and Nmap are in the system's PATH or specify the path in the script configuration.

## Usage
To use this script, you need to have administrative privileges to perform scans using Masscan and Nmap. Run the script with sudo to ensure it has the necessary permissions:

```bash
sudo python3.8 masscan_nmap.py
```

## Configuration
1.  IP File: The script reads IP addresses from a file named ips.txt, which should contain one IP address per line.
2. Output Files:
   - masscan_results.json: This file stores the raw output from Masscan.
   - nmap_results.txt: This file stores the formatted output from Nmap scans.
## Script Functions
- run_masscan(): Executes the Masscan scan with predefined parameters.
- extract_masscan(): Processes the output from Masscan, removes timestamps, and prepares data for the Nmap scan.
- nmap_scan(ip_port): Conducts an Nmap scan on each IP and port combination provided by the Masscan results.
- run_nmap(task_list): Manages multiprocessing to handle multiple Nmap scans simultaneously.
- save_results(results): Saves the results from Nmap scans to a text file.
## Important Notes
- The script should be run as root to ensure it can perform network scans.
- Modify the script parameters like IP file path, Masscan execution path, and output file names as per your system setup.
