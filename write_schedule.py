import sqlite3
import argparse

parser = argparse.ArgumentParser(description='Write min and max to buckler')
parser.add_argument('--id', type=int, help='ID of buckler', required=True)
parser.add_argument('--min', type=int, help='Min light', required=True)
parser.add_argument('--max', type=int, help='Max light', required=True)
args = vars(parser.parse_args())

max_dim_level = 255 - (args['min'] * 2.55)
min_dim_level = 255 - (args['max'] * 2.55)
light_id = args['id']

conn = sqlite3.connect('/home/pi/eecs149-smart-dimming/api/lights.db')
c = conn.cursor()
c.execute("SELECT char_value FROM lights WHERE id = ?", (id,))
entry = c.fetchone()
if entry:
    char_value = entry[0]
    dim_level = (char_value & 0xFF)
    if dim_level < min_dim_level:
        print("raising lights")
        new_char = (char_value & 0xFF00) | min_dim_level
        c.execute("UPDATE lights SET char_value = ?1, write_flag = 1 WHERE id = ?2", (new_char, id))
        conn.commit()
    elif dim_level > max_dim_level:
        print("lowering lights")
        new_char = (char_value & 0xFF00) | max_dim_level
        c.execute("UPDATE lights SET char_value = ?1, write_flag = 1 WHERE id = ?2", (new_char, id))
        conn.commit()
