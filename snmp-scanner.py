import subprocess
import datetime
import sys
import shutil
import os
import argparse

class Color:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_banner():
    banner = fr"""{Color.CYAN}{Color.BOLD}
   _____ _   ____  __  ___   ____                                 
  / ___// | / /  |/  |/ _ \ / __/_________ _____  ____  ___  _____
  \__ \/  |/ / /|_/ / /_/ /_\ \/ ___/ __ `/ __ \/ __ \/ _ \/ ___/
 ___/ / /|  / /  / / ____/___/ / /__/ /_/ / / / / / / /  __/ /    
/____/_/ |_/_/  /_/_/    /____/\___/\__,_/_/ /_/_/ /_/\___/_/     
{Color.YELLOW}By: shitodcy{Color.END}"""
    print(banner)
    print(f"{Color.YELLOW}[*] Alat Pengecekan Keamanan Router (SNMP Misconfiguration){Color.END}")

def check_dependencies():
    if shutil.which("snmpwalk") is None:
        print(f"{Color.RED}[!] ERROR: Program pendukung 'snmpwalk' belum terinstal di komputer ini.{Color.END}")
        print(f"{Color.YELLOW}[i] Solusi: Silakan instal terlebih dahulu.{Color.END}")
        print("    - Pengguna Arch/EndeavourOS : sudo pacman -S net-snmp")
        print("    - Pengguna Ubuntu/Debian    : sudo apt install snmp")
        sys.exit(1)

def scan_snmp(target_ip, output_dir, community="public"):
    output_file = os.path.join(output_dir, f"{target_ip}.txt")
    
    print(f"{Color.CYAN}>>> Memindai IP: {target_ip} <<<{Color.END}")
    
    command = ["snmpwalk", "-v", "1", "-c", community, target_ip, "1.3.6.1.2.1.1"]
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=5)

        if result.returncode == 0 and result.stdout:
            with open(output_file, 'w') as f:
                f.write("=== LAPORAN HASIL PENGECEKAN SNMP ===\n")
                f.write(f"Target IP  : {target_ip}\n")
                f.write(f"Waktu Cek  : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("-" * 37 + "\n")
                f.write("[STATUS] : Konfigurasi Terbuka!\n\n")
                f.write("Data yang berhasil ditarik dari router:\n")
                f.write(result.stdout)
                
            print(f"{Color.RED}{Color.BOLD}[!] RENTAN: Akses terbuka! Log disimpan ke: {output_file}{Color.END}\n")
            
        else:
            print(f"{Color.GREEN}[+] AMAN: Akses tertutup.{Color.END}\n")
                
    except subprocess.TimeoutExpired:
        print(f"{Color.YELLOW}[-] TIMEOUT: Diblokir Firewall.{Color.END}\n")
        
    except Exception as e:
        print(f"{Color.RED}[!] Terjadi kesalahan pada {target_ip}: {e}{Color.END}\n")

if __name__ == "__main__":
    check_dependencies()

    parser = argparse.ArgumentParser(description="Simple SNMP Misconfiguration Scanner")
    parser.add_argument("-l", "--list", help="File teks berisi daftar IP target (satu IP per baris)")
    args = parser.parse_args()

    output_directory = os.path.join("snmp-scanner", "result")
    os.makedirs(output_directory, exist_ok=True)

    print_banner()
  
    if args.list:
        if not os.path.isfile(args.list):
            print(f"{Color.RED}[!] File daftar target '{args.list}' tidak ditemukan!{Color.END}")
            sys.exit(1)
            
        print(f"{Color.CYAN}[*] Memuat target dari file: {args.list}{Color.END}")
        print(f"{Color.CYAN}[*] Folder penyimpanan hasil : {output_directory}/{Color.END}\n")
        
        with open(args.list, 'r') as file:
            target_ips = [line.strip() for line in file if line.strip()]
            
        print(f"{Color.BOLD}Ditemukan {len(target_ips)} target. Memulai pemindaian...{Color.END}\n")
        
        for ip in target_ips:
            scan_snmp(ip, output_directory)
            
        print(f"{Color.CYAN}{Color.BOLD}[v] Semua target selesai dipindai!{Color.END}")
      
    else:
        print(f"{Color.CYAN}[*] Folder penyimpanan hasil : {output_directory}/{Color.END}\n")
        try:
            while True:
                target_input = input(f"Masukkan IP Router (atau ketik 'q' untuk keluar) \n{Color.BOLD}IP Target > {Color.END}").strip()
                
                if target_input.lower() in ['q', 'quit', 'exit']:
                    print("\nTerima kasih telah menggunakan tools ini. Tetap aman!")
                    break
                elif target_input:
                    scan_snmp(target_input, output_directory)
                else:
                    print(f"{Color.YELLOW}IP tidak boleh kosong. Silakan coba lagi.{Color.END}\n")
        except KeyboardInterrupt:
            print(f"\n\n{Color.YELLOW}Aplikasi dihentikan paksa oleh pengguna. Keluar...{Color.END}")
            sys.exit()
