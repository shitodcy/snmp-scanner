# Simple SNMP Misconfiguration Scanner

Alat otomatisasi berbasis Python untuk mendeteksi kerentanan kesalahan konfigurasi pada protokol SNMPv1 (Information Disclosure via default community string). Skrip ini dirancang untuk mempermudah pekerjaan IT Support dan Security Researcher dalam memetakan keamanan infrastruktur jaringan secara efisien.

## Fitur Utama

- **Mode Interaktif:** Memindai satu IP target secara langsung melalui antarmuka terminal.
- **Mode Massal (Bulk Scan):** Membaca daftar ratusan IP dari file teks untuk pemindaian otomatis berskala besar.
- **Smart Logging:** Hanya menyimpan output log dari target yang terbukti rentan ke dalam direktori `snmp-scanner/result/`. Target yang berstatus aman atau ditolak oleh firewall tidak akan menghasilkan file log.
- **CLI UX:** Tampilan antarmuka command line yang dilengkapi pewarnaan indikator status untuk mempercepat identifikasi visual.
- **Dependency Checker:** Otomatis mendeteksi ketersediaan utilitas `snmpwalk` pada sistem operasi pengguna sebelum dijalankan.

## Prasyarat

Skrip ini berjalan pada lingkungan Python 3.x. Tidak ada pustaka eksternal Python yang dibutuhkan. Namun, alat ini mewajibkan adanya program `snmpwalk` yang terinstal di sistem operasi Anda.

**Cara Instalasi Dependensi OS:**
- Arch Linux / EndeavourOS: `sudo pacman -S net-snmp`
- Ubuntu / Debian: `sudo apt install snmp`
- RHEL / CentOS: `sudo yum install net-snmp-utils`

## Instalasi

Kloning repositori ini ke dalam mesin lokal Anda:

```bash
git clone [https://github.com/username-github-anda/snmp-scanner.git](https://github.com/username-github-anda/snmp-scanner.git)
cd snmp-scanner
