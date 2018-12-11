from channels.generic.websocket import WebsocketConsumer
import json
import sqlite3
from django.conf import settings
import os

light_db = os.path.join(settings.BASE_DIR, 'lights.db')

class LightSocketConsumer(WebsocketConsumer):
	def connect(self):
		print("connected light socket")
		self.accept()
		self.buckler_id = self.scope["url_route"]["kwargs"]["id"]
		print("id:", self.buckler_id)
		self.char_value = None
		conn = sqlite3.connect(light_db)
		c = conn.cursor()
		c.execute('SELECT char_value FROM lights WHERE id = ? AND char_value IS NOT NULL', (self.buckler_id,))
		entry = c.fetchone()
		print(entry)
		if entry:
			self.char_value = int(entry[0])
			c.execute('UPDATE write_mode SET enabled = 1')
			conn.commit()
		else:
			print("no entry or char_value")

	def disconnect(self, close_code):
		print("disconnected light socket")
		conn = sqlite3.connect(light_db)
		c = conn.cursor()
		c.execute('UPDATE write_mode SET enabled = 0')
		conn.commit()
		pass

	def receive(self, text_data):
		if self.char_value == None:
			print("no char_value, skipping")
			return
		data = json.loads(text_data)
		if 'motion_tracking' in data:
			self.char_value = (self.char_value & 0b0111111111111) | ((1 if data['motion_tracking'] else 0) << 12)
		if 'light_tracking' in data:
			self.char_value = (self.char_value & 0b1011111111111) | ((1 if data['light_tracking'] else 0) << 11)
		if 'dim_level' in data:
			self.char_value = (self.char_value & 0b1100000000000) | (5 << 8) | (data['dim_level'] & 0xFF)
		conn = sqlite3.connect(light_db)
		c = conn.cursor()
		c.execute('UPDATE lights SET char_value = ?1, write_flag = 1 WHERE id = ?2', (self.char_value, self.buckler_id))
		conn.commit()

class LightNameConsumer(WebsocketConsumer):
	def connect(self):
		print("light naming socket connected")
		self.accept()

	def disconnect(self, close_code):
		print('light naming socket disconnected')
		conn = sqlite3.connect(light_db)
		c = conn.cursor()
		c.execute("UPDATE write_mode SET enabled = 0")
		conn.commit()
		pass

	def receive(self, text_data):
		data = json.loads(text_data)
		print('received ' + str(data))
		conn = sqlite3.connect(light_db)
		c = conn.cursor()
		if 'name' in data and 'mac' in data:
			c.execute("SELECT id FROM lights WHERE id IS NOT NULL ORDER BY id DESC")
			current_id = c.fetchone()
			next_id = (current_id[0] + 1) if current_id else 0
			c.execute("UPDATE lights SET name = ?1, id = ?2 WHERE mac = ?3", (data['name'], next_id, data['mac']))
			self.send(text_data=json.dumps({'name_set':True}))
		elif 'flash' in data and 'mac' in data:
			c.execute("UPDATE write_mode SET enabled = 1")
			c.execute("UPDATE lights SET char_value = ?1, write_flag = 1 WHERE mac = ?2", (0x0500 if data['flash'] else 0x05FF, data['mac']))
		conn.commit()
