import asyncio
import socket
import argparse
from datetime import datetime
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
import sys
import ipaddress

# Constants
MAX_THREADS = 100
COMMON_PORTS = {
    20: "FTP Data", 21: "FTP Control", 22: "SSH", 23: "Telnet", 
    25: "SMTP", 53: "DNS", 80: "HTTP", 443: "HTTPS",
    3306: "MySQL", 5432: "PostgreSQL", 27017: "MongoDB"
}

async def scan_port(host, port, results, timeout=1):
    try:
        # Using asyncio.open_connection instead of raw sockets for better async support
        _, writer = await asyncio.wait_for(
            asyncio.open_connection(host, port),
            timeout=timeout
        )
        results[port] = {"status": "open", "service": COMMON_PORTS.get(port, "Unknown")}
        writer.close()
        await writer.wait_closed()
    except (asyncio.TimeoutError, ConnectionRefusedError):
        results[port] = {"status": "closed"}
    except Exception as e:
        results[port] = {"status": "error", "error": str(e)}

async def scan_ports(host, start_port, end_port, start_from_port=0):
    try:
        # Validate IP address
        ipaddress.ip_address(host)
    except ValueError:
        try:
            host = socket.gethostbyname(host)
        except socket.gaierror:
            print(f"Could not resolve hostname: {host}")
            return 0

    print(f"\nStarting port scan on {host} from port {start_port} to {end_port}...")
    start_time = datetime.now()
    
    results = {}
    tasks = []
    
    # Create chunks of ports for batch processing
    chunk_size = min(1000, end_port - start_from_port + 1)
    
    for port in range(start_from_port, end_port + 1, chunk_size):
        chunk_end = min(port + chunk_size, end_port + 1)
        for p in range(port, chunk_end):
            task = asyncio.create_task(scan_port(host, p, results))
            tasks.append(task)
        
        # Process chunk with progress bar
        with tqdm(total=len(tasks), desc=f"Scanning Ports {port}-{chunk_end-1}") as pbar:
            for coro in asyncio.as_completed(tasks):
                await coro
                pbar.update(1)
        tasks.clear()

    # Print results in an organized way
    print("\nScan Results:")
    print("-" * 60)
    print(f"{'Port':<10} {'Status':<10} {'Service':<20}")
    print("-" * 60)
    
    open_ports = 0
    for port in sorted(results.keys()):
        result = results[port]
        if result["status"] == "open":
            open_ports += 1
            service = result.get("service", "Unknown")
            print(f"{port:<10} {'OPEN':<10} {service:<20}")
    
    end_time = datetime.now()
    total_time = end_time - start_time
    
    print("\nScan Summary:")
    print(f"Total ports scanned: {len(results)}")
    print(f"Open ports found: {open_ports}")
    print(f"Scan completed in {total_time.total_seconds():.2f} seconds.")
    return len(results)

def save_results(results, filename):
    with open(filename, 'w') as f:
        for port, data in results.items():
            f.write(f"Port {port}: {data['status']}\n")

def main():
    parser = argparse.ArgumentParser(description="Advanced Port Scanner Tool")
    parser.add_argument("host", type=str, help="Target host (IP address or domain)")
    parser.add_argument("-s", "--start-port", type=int, help="Start port number (default: 1)", default=1)
    parser.add_argument("-e", "--end-port", type=int, help="End port number (default: 65535)", default=65535)
    parser.add_argument("-o", "--output", type=str, help="Output file for results")
    parser.add_argument("-t", "--timeout", type=float, default=1.0, help="Timeout for each port scan")
    parser.add_argument("--common", action="store_true", help="Scan only common ports")
    
    args = parser.parse_args()
    
    if args.common:
        ports_to_scan = sorted(COMMON_PORTS.keys())
        args.start_port = min(ports_to_scan)
        args.end_port = max(ports_to_scan)
    
    if args.start_port < 1 or args.end_port > 65535:
        print("Port range must be between 1 and 65535.")
        return
    if args.start_port > args.end_port:
        print("Start port must be less than or equal to end port.")
        return
    
    current_port = args.start_port
    
    try:
        asyncio.run(scan_ports(args.host, args.start_port, args.end_port))
    except KeyboardInterrupt:
        print("\nScan interrupted.")
        while True:
            try:
                user_input = input("\nDo you want to quit (q) or continue (c)? ").strip().lower()
                if user_input == "q":
                    print("Exiting scan.")
                    sys.exit(0)
                elif user_input == "c":
                    print("Resuming scan...")
                    asyncio.run(scan_ports(args.host, current_port, args.end_port, current_port))
                    break
                else:
                    print("Invalid input, please enter 'q' to quit or 'c' to continue.")
            except KeyboardInterrupt:
                print("\nForced exit.")
                sys.exit(1)

if __name__ == "__main__":
    main()

#usage: scanner.py [-h] [-s START_PORT] [-e END_PORT] [-o OUTPUT] [-t TIMEOUT]