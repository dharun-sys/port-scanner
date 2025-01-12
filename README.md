# Port Scanner

A lightweight and efficient port scanner that allows you to scan a range of ports on a target system. It provides options for specifying port ranges, timeout settings, and saving results to a file.

---

## Usage

```
python scanner.py [-h] [-s START_PORT] [-e END_PORT] [-o OUTPUT] [-t TIMEOUT]
```

### Options:
- `-h, --help`  
  Display the help message and exit.
  
- `-s START_PORT, --start-port START_PORT`  
  Specify the starting port number for the scan.
  
- `-e END_PORT, --end-port END_PORT`  
  Specify the ending port number for the scan.
  
- `-o OUTPUT, --output OUTPUT`  
  Save the scan results to the specified output file.
  
- `-t TIMEOUT, --timeout TIMEOUT`  
  Set the timeout (in seconds) for each port scan.

---

### Example Commands

1. Scan ports 20 to 80 with a timeout of 1 second:
   ```
   python scanner.py -s 20 -e 80 -t 1
   ```

2. Save the scan results to a file named `results.txt`:
   ```
   python scanner.py -s 20 -e 80 -t 1 -o results.txt
   ```

3. Get help:
   ```
   python scanner.py -h
   ```

---

### Installation

1. Clone this repository:
   ```
   git clone https://github.com/dharun-sys/port-scanner.git
   ```

2. Navigate to the project folder and install requirements:
   ```
   cd port-scanner
   pip install -r requirements.txt
   ```

3. Run the script using the usage command shown above.

---

### License

This project is licensed under the [MIT License](LICENSE).

---

### Contributing

Feel free to fork the repository, open issues, or submit pull requests for improvements!
