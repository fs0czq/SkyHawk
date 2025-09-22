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
    """Logging ayarlarını yapılandırır."""
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
    """HTTP/HTTPS bağlantısını kontrol eder ve web servisi doğrular."""
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
                        logging.info(f"{Fore.LIGHTWHITE_EX}[{Fore.LIGHTYELLOW_EX}?{Fore.LIGHTWHITE_EX}] {Fore.LIGHTCYAN_EX}{check} (Status: {response.status_code}, Potansiyel Web Servisi)")
            except requests.exceptions.RequestException:
                continue
    except Exception as e:
        logging.debug(f"Bağlantı kontrol hatası {address}:{port} - {e}")

def port_tarama(ip, port, timeout=2, no_web_check=False):
    """Belirtilen IP ve portta bağlantı kontrolü yapar."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((ip, port))
            if result == 0:
                service = port_service_map.get(port, socket.getservbyport(port, "tcp") if port in yaygin_portlar else "Bilinmeyen servis")
                logging.info(f"{Fore.LIGHTWHITE_EX}Port {Fore.LIGHTCYAN_EX}{port:<5} {Fore.LIGHTWHITE_EX}({Fore.LIGHTMAGENTA_EX}{service}{Fore.LIGHTWHITE_EX}) {Fore.LIGHTGREEN_EX}AÇIK")
                if not no_web_check:  # Web kontrolü kapalı değilse
                    check_conn(ip, port)
    except Exception as e:
        logging.debug(f"Port tarama hatası {ip}:{port} - {e}")

def port_tarama_baslat(ip, max_threads=100, timeout=2, no_web_check=False):
    """Belirtilen IP için port taramayı başlatır."""
    logging.info(f"\n{Fore.LIGHTWHITE_EX}[{Fore.LIGHTYELLOW_EX}!{Fore.LIGHTWHITE_EX}] {Fore.LIGHTGREEN_EX}{ip} için portlar taranıyor...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        for port in yaygin_portlar:
            executor.submit(port_tarama, ip, port, timeout, no_web_check)

def ag_taramasi(aralik, timeout=10, no_web_check=False):
    """Ağdaki cihazları ARP ile tarar."""
    logging.info(f"{Fore.LIGHTWHITE_EX}[{Fore.LIGHTYELLOW_EX}!{Fore.LIGHTWHITE_EX}] {Fore.LIGHTGREEN_EX}{aralik} ağında cihazlar taranıyor...")
    arp = ARP(pdst=aralik)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    paket = ether / arp

    try:
        sonuc = srp(paket, timeout=timeout, verbose=0)[0]
        cihazlar = []

        for _, alınan in sonuc:
            try:
                hostname = socket.gethostbyaddr(alınan.psrc)[0].replace("-adli-kisiye-ait-", " ").replace("-", " ")
            except socket.herror:
                hostname = "Bilinmeyen Host"

            cihazlar.append({
                "HostName": hostname,
                "IP": alınan.psrc,
                "MAC": alınan.hwsrc
            })

        for cihaz in cihazlar:
            logging.info("\n" + Fore.LIGHTBLACK_EX + "-" * 45)
            for k, v in cihaz.items():
                logging.info(f"{Fore.LIGHTWHITE_EX}[{Fore.LIGHTCYAN_EX}{k}{Fore.LIGHTWHITE_EX}]: {Fore.LIGHTCYAN_EX}{v}")
            if not no_web_check:  # Varsayılan portlar için web kontrolü
                check_conn(cihaz["IP"], None)
            port_tarama_baslat(cihaz["IP"], no_web_check=no_web_check)
            logging.info(Fore.LIGHTBLACK_EX + "-" * 45)

        return cihazlar
    except Exception as e:
        logging.error(f"Ağ tarama hatası: {e}")
        return []

def main():
    """Ana fonksiyon: Argümanları parse eder ve taramayı başlatır."""
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

    # Kullanıcı uyarısı
    logging.warning(f"\n{Fore.LIGHTRED_EX}UYARI: {Fore.LIGHTMAGENTA_EX}Bu araç yalnızca yetkili olduğunuz ağlarda kullanılmalıdır. Yasal sorumluluk kullanıcıya aittir.\n" + Fore.RESET)

    # Argümanları parse et
    parser = argparse.ArgumentParser(description="SkyHawk ~ Cihazları ve portları keşfeder.")
    parser.add_argument("--target", default=f"{netifaces.gateways()['default'][netifaces.AF_INET][0]}/24", help="Taranacak IP aralığı (ör: 192.168.1.0/24)")
    parser.add_argument("--timeout", type=float, default=2, help="Port tarama timeout süresi (saniye)")
    parser.add_argument("--threads", type=int, default=100, help="Maksimum thread sayısı")
    parser.add_argument("--no-web-check", action="store_true", help="Web kontrolünü devre dışı bırakın")
    args = parser.parse_args()

    # Ağ taramasını başlat
    ag_taramasi(args.target, timeout=args.timeout, no_web_check=args.no_web_check)

if __name__ == "__main__":
    if is_root():
        main()
    else:
        print(Fore.LIGHTRED_EX + "[!] Bu işlemi gerçekleştirmek için lütfen betiği root yetkileriyle başlatın." + Fore.RESET)
