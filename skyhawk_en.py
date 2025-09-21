import argparse
import logging
import socket
import netifaces
import requests
import ctypes
import concurrent.futures 
from scapy.all import ARP, Ether, srp
from colorama import Fore, init
from os import getuid, name
from ports import yaygin_portlar, port_service_map
from time import sleep


def is_root(user = name):
    if name == "nt":
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    else:
        try:
            return getuid() == 0
        except:
            return False

def setup_logging():
    """Configure logging settings."""
    logging.basicConfig(
        filename="scan_results.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter("%(message)s"))
    logging.getLogger().addHandler(console)

def check_conn(address, port):
    """Check HTTP/HTTPS connection and verify if it's a web service."""
    try:
        checkurls = [f"https://{address}:{port}", f"http://{address}:{port}"]
        for check in checkurls:
            try:
                response = requests.get(check, timeout=2, allow_redirects=True)
                if response.status_code in {200, 301, 302, 401, 403, 404}:
                    content_type = response.headers.get("Content-Type", "")
                    if "text/html" in content_type or "application/json" in content_type:
                        logging.info(f"{Fore.LIGHTWHITE_EX}[{Fore.LIGHTGREEN_EX}+{Fore.LIGHTWHITE_EX}] {Fore.LIGHTCYAN_EX}{check} (Status: {response.status_code})")
                    else:
                        logging.info(f"{Fore.LIGHTWHITE_EX}[{Fore.LIGHTYELLOW_EX}?{Fore.LIGHTWHITE_EX}] {Fore.LIGHTCYAN_EX}{check} (Status: {response.status_code}, Potential Web Service)")
            except requests.exceptions.RequestException:
                continue
    except Exception as e:
        logging.debug(f"Connection check error {address}:{port} - {e}")

def port_scan(ip, port, timeout=2, no_web_check=False):
    """Check connection on the specified IP and port."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((ip, port))
            if result == 0:
                service = port_service_map.get(port, socket.getservbyport(port, "tcp") if port in yaygin_portlar else "Unknown service")
                logging.info(f"{Fore.LIGHTWHITE_EX}Port {Fore.LIGHTCYAN_EX}{port:<5} {Fore.LIGHTWHITE_EX}({Fore.LIGHTMAGENTA_EX}{service}{Fore.LIGHTWHITE_EX}) {Fore.LIGHTGREEN_EX}OPEN")
                if not no_web_check:  # If web check is not disabled
                    check_conn(ip, port)
    except Exception as e:
        logging.debug(f"Port scan error {ip}:{port} - {e}")

def start_port_scan(ip, max_threads=100, timeout=2, no_web_check=False):
    """Start port scan for the specified IP."""
    logging.info(f"\n{Fore.LIGHTWHITE_EX}[{Fore.LIGHTYELLOW_EX}!{Fore.LIGHTWHITE_EX}] {Fore.LIGHTGREEN_EX}Scanning ports for {ip}...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        for port in yaygin_portlar:
            executor.submit(port_scan, ip, port, timeout, no_web_check)

def network_scan(ip_range, timeout=10, no_web_check=False):
    """Scan devices on the network using ARP."""
    logging.info(f"{Fore.LIGHTWHITE_EX}[{Fore.LIGHTYELLOW_EX}!{Fore.LIGHTWHITE_EX}] {Fore.LIGHTGREEN_EX}Scanning devices on network {ip_range}...")
    arp = ARP(pdst=ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp

    try:
        result = srp(packet, timeout=timeout, verbose=0)[0]
        devices = []

        for _, received in result:
            try:
                hostname = socket.gethostbyaddr(received.psrc)[0].replace(".modem.turktelekom", "").replace("-adli-kisiye-ait-", " ").replace("-", " ")
            except socket.herror:
                hostname = "Unknown Host"

            devices.append({
                "HostName": hostname,
                "IP": received.psrc,
                "MAC": received.hwsrc
            })

        for device in devices:
            logging.info("\n" + Fore.LIGHTBLACK_EX + "-" * 45)
            for k, v in device.items():
                logging.info(f"{Fore.LIGHTWHITE_EX}[{Fore.LIGHTCYAN_EX}{k}{Fore.LIGHTWHITE_EX}]: {Fore.LIGHTCYAN_EX}{v}")
            if not no_web_check:  # Default web check for common ports
                check_conn(device["IP"], None)
            start_port_scan(device["IP"], no_web_check=no_web_check)
            logging.info(Fore.LIGHTBLACK_EX + "-" * 45)

        return devices
    except Exception as e:
        logging.error(f"Network scan error: {e}")
        return []

def main():
    """Main function: parse arguments and start scanning."""
    init(autoreset=True)
    setup_logging()
    
    print(
f"""{Fore.LIGHTBLACK_EX}                                                                           
███████╗██╗  ██╗██╗   ██╗██╗  ██╗ █████╗ ██╗    ██╗██╗  ██╗
██╔════╝██║ ██╔╝╚██╗ ██╔╝██║  ██║██╔══██╗██║    ██║██║ ██╔╝
███████╗█████╔╝  ╚████╔╝ ███████║███████║██║ █╗ ██║█████╔╝ 
╚════██║██╔═██╗   ╚██╔╝  ██╔══██║██╔══██║██║███╗██║██╔═██╗ 
███████║██║  ██╗   ██║   ██║  ██║██║  ██║╚███╔███╔╝██║  ██╗
╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝

{Fore.LIGHTYELLOW_EX}created by @fs0czq{Fore.RESET}                                                            
"""
)
    sleep(1.5)

    # User warning
    logging.warning(f"\n{Fore.LIGHTRED_EX}WARNING: {Fore.LIGHTMAGENTA_EX}This tool must only be used on networks you are authorized to test. Legal responsibility lies with the user.\n" + Fore.RESET)

    # Parse arguments
    parser = argparse.ArgumentParser(description="SkyHawk ~ Discover devices and scan ports.")
    parser.add_argument("--target", default=f"{netifaces.gateways()['default'][netifaces.AF_INET][0]}/24", help="Target IP range (e.g., 192.168.1.0/24)")
    parser.add_argument("--timeout", type=float, default=2, help="Port scan timeout (seconds)")
    parser.add_argument("--threads", type=int, default=100, help="Maximum number of threads")
    parser.add_argument("--no-web-check", action="store_true", help="Disable web check")
    args = parser.parse_args()

    # Start network scan
    network_scan(args.target, timeout=args.timeout, no_web_check=args.no_web_check)

if __name__ == "__main__":
    if is_root():
        main()
    else:
        print(Fore.LIGHTRED_EX + "[!] Please run this script with root privileges." + Fore.RESET)
