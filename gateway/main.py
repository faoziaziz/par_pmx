# main.py
from fastapi import FastAPI
from pyzabbix import ZabbixAPI
from pydantic import BaseModel
import time 

# Konfigurasi Zabbix
ZABBIX_URL = "http://192.168.100.79/zabbix"
ZABBIX_USER = "Admin"
ZABBIX_PASSWORD = "zabbix"
# ITEM_KEY = "test.item"

class Item(BaseModel):
    name: str

    
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World"}



@app.post("/itemszab")
def getpost_item(item_id: str, items: Item, q: str = None):
    # Membuat koneksi ke Zabbix API
    zapi = ZabbixAPI(ZABBIX_URL)
    zapi.login(ZABBIX_USER, ZABBIX_PASSWORD)
    # Mencari item berdasarkan key
    itemz = zapi.item.get(filter={"key_": items.name}, output=["itemid"])

    if itemz:
        # Mengambil item ID dari hasil pencarian
        item_id = itemz[0]['itemid']

        # Mendapatkan data terakhir dari item berdasarkan item ID
        history = zapi.history.get(itemids=item_id, limit=1, output="extend", sortfield="clock", sortorder="DESC")

        if history:
            last_entry = history[0]
            # Menampilkan timestamp dan nilai terakhir
            print(f"Last Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(int(last_entry['clock'])))}")
            print(f"Last Value: {last_entry['value']}")
            return {"status": 1, "lastdata": last_entry["value"] }
        else:
            print("No data found for this item.")
            return {"status": 0 }
    else:
        print("Item with the specified key not found.")
        return {"status": 0 }

    return {"status": 0 }
