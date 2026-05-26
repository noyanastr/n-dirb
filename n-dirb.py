#!/usr/bin/env python3

#Google Translate was used for the English sections!

import argparse
...
#Google Translate was used for the English sections!

import argparse # used get to parameters / parametre almak için kullanıldı
import os # used for create folder ,file and run terminal / işletim sistemi işlemleri için kullanıldı
import re # used for Regular Expression / metinleri dosya adına uygun hale getirmek için kullanıldı
import socket # used for dns translation / dns çözümleme için kullanıldı
import subprocess # used for terminal / pythondan terminal komutu çalıştırmak için kullanıldı
from datetime import datetime # used for timestamp / rapora zaman damgası eklemek için kullanıldı
from pathlib import Path


def run_command(command):
    try:
        result = subprocess.run(
            command,
            shell=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        return result.stdout
    except Exception as e:
        return f"Komut çalıştırılırken hata oluştu: {e}"
#User feedback was gathered, and responses to potential errors were formulated.
#Kullanıcıdan girdi alındı ve hatalı girdilere karşı çıktılar ve işleyişler hazırlandı
def resolve_domain(domain):
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return None
#The IP address to which the domain name is pointing has been found.
#Burada alınan domainin hangi ip'ye bağlandığı bulundu ve olası hataya karşı cevap


def ping_target(domain):
    return run_command(f"ping -c 4 {domain}")
#The package was sent to the destination address 4 times.
#Hedefe 4 adet paket göndererek aktifliğini kontrol ediyoruz.


def nmap_scan(ip):
    return run_command(f"nmap -sV -f -T3 {ip}")
#A sophisticated Nmap tool was used.
#nmap kullanılarak port taraması yapıdı ayrıca -sV ile versiyon araması da yapıldı. T3 ile hızı ayarlandı.


def dir_scan(domain):
    url = domain if domain.startswith(("http://", "https://")) else f"http://{domain}"
    wordlist = "/usr/share/wordlists/dirb/common.txt"
    return run_command(f"dirb {url} {wordlist}")
#Index scanning was performed using dirb.
#dirb ile dizin taraması yapıldı bunun için common.txt kullanmayı tercih ettim.

def clean_filename(domain):
    return re.sub(r"[^a-zA-Z0-9_.-]", "_", domain)
#To remove invalid characters from the filename.
#Dosya adı için geçersiz karakterler temizlendi.


def generate_report(domain, ip, ping_result, nmap_result, dir_result):
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)

    filename = reports_dir / f"{clean_filename(domain)}_report.txt"

    report = f"""
GitHub=========================noyanastr
	  AUTO SCANNER REPORT
========================================

Target Domain : {domain}
Resolved IP   : {ip}
Scan Date     : {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

GitHub=========================noyanastr
	     PING RESULT
========================================

{ping_result}

GitHub=========================noyanastr
	 NMAP PORT SCAN RESULT
========================================

{nmap_result}

GitHub=========================noyanastr
	 DIRECTORY SCAN RESULT
========================================

{dir_result}

GitHub=========================noyanastr
	   END OF REPORT
========================================
"""

    with open(filename, "w", encoding="utf-8") as file:
        file.write(report)

    return filename
    
def banner():

    print(r"""
███╗   ██╗      ██████╗ ██╗██████╗ ██████╗ 
████╗  ██║      ██╔══██╗██║██╔══██╗██╔══██╗
██╔██╗ ██║█████╗██║  ██║██║██████╔╝██████╔╝
██║╚██╗██║╚════╝██║  ██║██║██╔══██╗██╔══██╗
██║ ╚████║      ██████╔╝██║██║  ██║██████╔╝
╚═╝  ╚═══╝      ╚═════╝ ╚═╝╚═╝  ╚═╝╚═════╝ 

        Welcome
""")

def show_menu():
    print("""
GitHub=========================noyanastr
           AUTO SCANNER TOOL
========================================

[1] Domain Scan Başlat
[2] Yardım
[0] Çıkış
""")


def start_scan():
    domain = input("[?] Domain giriniz: ").strip()

    if not domain:
        print("[-] Domain boş bırakılamaz.")
        return

    print("[+] Domain IP adresine çözümleniyor...")
    ip = resolve_domain(domain)

    if not ip:
        print("[-] Domain IP adresine çözümlenemedi.")
        return

    print(f"[+] IP bulundu: {ip}")

    print("[+] Ping atılıyor...")
    ping_result = ping_target(domain)

    print("[+] Nmap port taraması başlatılıyor...")
    nmap_result = nmap_scan(ip)

    print("[+] Alt dizin taraması başlatılıyor...")
    dir_result = dir_scan(domain)

    print("[+] Rapor oluşturuluyor...")
    report_file = generate_report(domain, ip, ping_result, nmap_result, dir_result)

    print(f"[+] Rapor oluşturuldu: {report_file}")


def show_help():
    print("""
GitHub=========================noyanastr
		 HELP
========================================

Bu araç yalnızca izinli hedeflerde kullanılmalıdır.

İşleyiş:
1. Kullanıcıdan domain alınır
2. Domain IP adresine çözümlenir
3. Hedefe ping atılır
4. Nmap ile port ve servis taraması yapılır
5. Dirb ile alt dizin taraması yapılır
6. Sonuçlar reports klasörüne TXT olarak kaydedilir
""")


def main():
    banner()
    

    while True:
        show_menu()
        choice = input("Seçim: ").strip()

        if choice == "1":
            start_scan()

        elif choice == "2":
            show_help()

        elif choice == "0":
            print("[+] Çıkış yapılıyor...")
            break

        else:
            print("[-] Geçersiz seçim.")


if __name__ == "__main__":
    main()