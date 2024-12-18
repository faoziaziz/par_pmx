from pyzabbix import ZabbixAPI
import time

# Konfigurasi Zabbix API
ZABBIX_URL = "http://192.168.100.79/zabbix"  # Ganti dengan URL server Zabbix Anda
ZABBIX_USER = "Admin"  # Ganti dengan username Zabbix Anda
ZABBIX_PASSWORD = "zabbix"  # Ganti dengan password Zabbix Anda

# Membuat koneksi ke Zabbix API
zapi = ZabbixAPI(ZABBIX_URL)
zapi.login(ZABBIX_USER, ZABBIX_PASSWORD)

# Key item yang ingin Anda ambil nilainya (misalnya "sensor.temp")
item_key = "test.key"  # Ganti dengan key item yang sesuai

# Mencari item berdasarkan key
items = zapi.item.get(filter={"key_": item_key}, output=["itemid"])

if items:
    # Mengambil item ID dari hasil pencarian
    item_id = items[0]['itemid']

    # Mendapatkan data terakhir dari item berdasarkan item ID
    history = zapi.history.get(itemids=item_id, limit=1, output="extend", sortfield="clock", sortorder="DESC")

    if history:
        last_entry = history[0]
        # Menampilkan timestamp dan nilai terakhir
        print(f"Last Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(int(last_entry['clock'])))}")
        print(f"Last Value: {last_entry['value']}")
    else:
        print("No data found for this item.")
else:
    print("Item with the specified key not found.")