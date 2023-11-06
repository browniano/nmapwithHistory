import nmap
import sqlite3
from prettytable import PrettyTable
from datetime import datetime

def create_connection():
    conn = sqlite3.connect('network_history.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS hosts_history
                      (ip_address TEXT PRIMARY KEY, mac_address TEXT, vendor TEXT, timestamp TEXT)''')
    conn.commit()
    return conn

def save_to_database(conn, ip_address, mac_address, vendor):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor = conn.cursor()
    # Try to update the existing record, if not present, insert a new record
    cursor.execute('INSERT OR REPLACE INTO hosts_history (ip_address, mac_address, vendor, timestamp) VALUES (?, ?, ?, ?)',
                   (ip_address, mac_address, vendor, timestamp))
    conn.commit()

def scan_local_network():
    nm = nmap.PortScanner()
    nm.scan(hosts='192.168.1.0/24', arguments='-sn', sudo=True)

    hosts_table = PrettyTable()
    hosts_table.field_names = ["IP Address", "MAC Address", "Vendor"]

    conn = create_connection()

    for host in nm.all_hosts():
        if 'mac' in nm[host]['addresses']:
            ip_address = host
            mac_address = nm[host]['addresses']['mac']
            vendor = nm[host]['vendor'].get(mac_address, "Unknown Vendor")
            hosts_table.add_row([ip_address, mac_address, vendor])
            save_to_database(conn, ip_address, mac_address, vendor)
        
    # Add the footnote row
    footnote1 = "Espressif = Shelly"
    footnote2 = "Sichuan = cameras and doorbell"
    footnote3 = "Winstars = Wavelink AP"
    footnote4 = "Tuya = Smart plug"
    hosts_table.add_row(["", "", footnote1])  # Add an empty row before the footnote
    hosts_table.add_row(["", "", footnote2]) 
    hosts_table.add_row(["", "", footnote3]) 
    hosts_table.add_row(["", "", footnote4]) 
 
    
    conn.close()
    return hosts_table

if __name__ == "__main__":
    result_table = scan_local_network()
    print("Current Connected Hosts:")
    print(result_table)

    # Retrieve and print historical data with only the last detected time of connections
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM hosts_history')
    historical_data = cursor.fetchall()

    historical_table = PrettyTable()
    historical_table.field_names = ["IP Address", "MAC Address", "Vendor", "Timestamp"]

    for record in historical_data:
        historical_table.add_row(record[0:3] + (record[3],))

    print("\nHistorical Connected Hosts:")
    print(historical_table)

    conn.close()
