# nmapwithHistory

A simple python script to keep track of the devices connected to our domestic LAN

The following python modules should be installed: sqlite3, nmap, PrettyTable, datetime.

The IP range of your LAN should be set up in line 24:

nm.scan(hosts='192.168.1.0/24', arguments='-sn', sudo=True)

The script should be run with sudo permissions.

The script prints out two tables, the first one with the current list of connected devices
arranged as:

Current Connected Hosts:

      │ +---------------+-------------------+-------------------------------------+
      │ |   IP Address  |    MAC Address    |                Vendor               |
      │ +---------------+-------------------+-------------------------------------+


and the second one with a list of devices with the last connection times:
 
 Historical Connected Hosts:
 
     │ +---------------+-------------------+-------------------------------------+---------------------+
     │ |   IP Address  |    MAC Address    |                Vendor               |      Timestamp      |
     │ +---------------+-------------------+-------------------------------------+---------------------+

The user may add some information footnotes to the first table to locate the devices (see lines 40 to 47):


     
  footnote1 = "Espressif = Shelly"

  footnote2 = "Sichuan = cameras and doorbell"
  
  footnote3 = "Winstars = Wavelink AP"
  
  footnote4 = "Tuya = Smart plug"
  
  hosts_table.add_row(["", "", footnote1]) 
  
  hosts_table.add_row(["", "", footnote2]) 
  
  hosts_table.add_row(["", "", footnote3]) 
  
  hosts_table.add_row(["", "", footnote4]) 

  
