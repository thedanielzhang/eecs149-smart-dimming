from bluepy import btle

class BLEDelegate(btle.DefaultDelegate):
	def __init__(self, params=None):
		super().__init__()
	def handleNotification(self, cHandle, data):
		print("got notification")
		print(cHandle)
		print(data)

class BucklerBT:
	def __init__(self, mac, write_on_change=False):
		self.mac = mac
		self.char = None

	def connect(self):
		if self.char:
			print("already connected. try reconnect()")
			return
		try:
			device = btle.Peripheral(self.mac, btle.ADDR_TYPE_RANDOM).withDelegate(BLEDelegate())
			chars = device.getCharacteristics(uuid="0000BEEF1212EFDE1523785FEF13D123")
			if len(chars) != 1:
				print("did not have 1 char")
				device.disconnect()
				return
			print("Connected!")
			self.char = chars[0]
			handle = self.char.getHandle() + 1
			device.writeCharacteristic(handle, b'\x01\x00')
		except btle.BTLEException as e:
			print("Unable to connect. Error:")
			print(e)

	def disconnect(self):
		if self.char:
			self.char.peripheral.disconnect()
			self.char = None

	def reconnect(self):
		self.disconnect()
		self.connect()

	def read(self):
		if not self.char:
			print("not connected!")
			return
		char_data = self.char.read()
		print("recieved data:")
		print(char_data)
		if len(char_data) == 4:
			print("data valid")
			return char_data[0] | (char_data[1] << 8)
		return None

	def write(self, char_value):
		if not self.char:
			print("not connected!")
			return
		self.char.write(bytes([char_value & 0xFF, (char_value >> 8) & 0xFF, 0, 0]))

class LightManager:
	LIGHT_SERVICE_UUID = "0000f00d-1212-efde-1523-785fef13d123"
	def __init__(self):
		self.scanned = {}
		self.connected = {}
	def scan(self, duration=4):
		scanner = btle.Scanner()
		scanned = scanner.scan(duration)
		for device in scanned:
			if device.getValueText(7) == LightManager.LIGHT_SERVICE_UUID:
				print("Found buckler! Name: " + device.getValueText(9))
				self.scanned[device.addr] = BucklerBT(device.addr, write_on_change=True)
				if device.addr in self.connected:
					del self.connected[device.addr]

	def connect(self):
		for mac, device in list(self.scanned.items()):
			device.connect()
			if device.char:
				self.connected[mac] = device
				del self.scanned[mac]

