#This should run continuously in background

import sqlite3
from lights import LightManager
import time

light_db = '/home/pi/eecs149-smart-dimming/api/lights.db'

light_manager = LightManager()

conn = sqlite3.connect(light_db)
c = conn.cursor()
c.execute("UPDATE lights SET write_flag = 0, connected = 0")
c.execute("UPDATE write_mode SET enabled = 0")
while True:
    c.execute("SELECT enabled FROM write_mode")
    write_mode = c.fetchone()[0] == 1
    if write_mode:
        #continuously write new changes to the buckler
        #no longer scanning or reading as to not freeze up
        #access to the ble device when we need to write fast
        for entry in c.execute("SELECT mac, char_value FROM lights WHERE write_flag = 1 AND connected = 1"):
            mac = entry[0]
            char_value = entry[1]
            light_manager.connected[mac].write(char_value)
            c.execute("UPDATE lights SET write_flag = 0 WHERE mac = ?", (mac,))
        conn.commit()
        #tune this interval to optimize performance
        time.sleep(0.2)
    else:
        #check for new data from the bluetooth and scan for new devices
        light_manager.scan(4)
        light_manager.connect()
        c.execute("SELECT mac FROM lights")
        db_macs = [entry[0] for entry in c.fetchall() if entry and entry[0]]
        for mac in db_macs:
            connected = 1 if mac in light_manager.connected else 0
            c.execute("UPDATE lights SET connected = ?1 WHERE mac = ?2", (connected, mac))
        for mac in light_manager.connected:
            if mac not in db_macs:
                c.execute("INSERT INTO lights (mac, connected, write_flag) VALUES(?, 1, 0)", (mac,))
        for entry in c.execute("SELECT mac, char_value FROM lights WHERE write_flag = 0 AND connected = 1"):
            mac = entry[0]
            if mac in light_manager.connected:
                char_value = light_manager.connected[mac].read()
                if char_value != entry[1]:
                    c.execute("UPDATE lights SET char_value = ?1 WHERE mac = ?2", (char_value, mac))
        conn.commit()



#@app.task
#def scan_and_connect():
#    light_manager.scan()
#    light_manager.connect()
#    conn = sqlite3.connect(light_db)
#    c = conn.cursor()
#    c.execute("SELECT mac FROM lights")
#    db_macs = c.fetchall()
#    for mac in db_macs:
#        c.execute("UPDATE lights SET connected = ?1 WHERE mac = ?2", (1 if (mac in light_manager.connected) else 0, mac))
#    for mac in light_manager.connected:
#        if mac not in db_macs:
#            c.execute("INSERT INTO lights (mac, connected) VALUES(?, 1)", (mac,))
#    conn.commit()

#Reads data from the buckler. If anything is different in the
#new data from what is in the database, and the write flag is
#not enabled in the database row (which would indicate that the
#difference is a change on the pi side that needs to be written),
#it updates the database with the new data
#@app.task
#def read_data():
#    conn = sqlite3.connect(light_db)
#   c = conn.cursor()
#    for entry in c.execute("SELECT mac, char_value FROM lights WHERE write_flag = 0 AND name IS NOT NULL AND connected = 1"):
#        mac = entry[0]
#        char_value = light_manager.connected[mac].read()
#        if char_value != entry[1]:
#            c.execute("UPDATE lights SET char_value = ?1 WHERE mac = ?2", (char_value, mac))
#    conn.commit()

#Checks the database for a rows with the write flag set, and
#if it is set, it uploads the data to the database and clears the write flag
#@app.task
#def write_data():
#    conn = sqlite3.connect(light_db)
#    c = conn.cursor()
#    for entry in c.execute("SELECT mac, char_value FROM lights WHERE write_flag = 1 AND connected = 1"):
#        mac = entry[0]
#        char_value = entry[1]
#        light_manager.connected[mac].write(char_value)
#        c.execute("UPDATE lights SET write_flag = 0 WHERE mac = ?", (mac,))
#    conn.commit()

#def flash(mac):
#    conn = sqlite3.connect(light_db)
#    c = conn.cursor()
#    for i in range(10):
#        c.execute("UPDATE lights SET char_value = ?1, write_flag = 1 WHERE connected = 1 AND mac = ?2", ((0x05FF if (i%2 == 0) else 0x0500), mac))
#        time.sleep(1)
