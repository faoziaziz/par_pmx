import socket
import json

# Konfigurasi server Zabbix
ZABBIX_SERVER = "localhost"  # Ganti dengan IP Zabbix Server Andai
ZABBIX_PORT = 10051

# Data yang akan dikirim
data = {
    "request": "sender data",
    "data": [
        {
            "host": "TestHost",  # Nama host di Zabbix
            "key": "test.key",   # Key dari item di Zabbix
            "value": "42"        # Nilai yang ingin dikirim
        }
    ]
}

# Serialize data ke JSON
json_data = json.dumps(data)

# Buat header Zabbix dengan panjang data 16-bit
header = b"ZBXD\x01"  # Header Zabbix
data_length = len(json_data).to_bytes(2, byteorder="big")  # Panjang data 16-bit (big-endian)
packet = header + data_length + json_data.encode("utf-8")

# Kirim paket melalui UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(packet, (ZABBIX_SERVER, ZABBIX_PORT))

print(f"Data sent to Zabbix Server {ZABBIX_SERVER}:{ZABBIX_PORT}")
sock.close()

