import asyncio
import threading
import time

from socket import *
from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout
from prompt_toolkit.widgets import Frame
from prompt_toolkit.layout.containers import Window, Float, HSplit, VSplit
from prompt_toolkit.layout.controls import FormattedTextControl

host = '222.73.120.40'
port = 9794
data2 = "{(len=92)MARKET01@@@+T@1@@@@@@@0@&LME,CA3M;SGXQ,NK2412;BMD,FCPO2501;KRX,101VC;SGXQ,UC2412;SGXQ,CN2410}"
keys = ['LME@CA3M', 'SGXQ@NK2412', 'BMD@FCPO2501', 'KRX@101VC', 'SGXQ@UC2412', 'SGXQ@CN2410']
table_heads = ['Last Price', 'Last Qty', 'Volume', 'High', 'Low', 'Open', 'PreSettlement', "Bid Price", "Ask Price", 'Bid Qty', "Ask Qty"]
real_data = {}
parseIndex = {
	# 'LME@CA3M': {
	# 	'Last Price': 8,
	# 	'Last qty': 9,
	# 	'Bid Price': 4,
	# 	'Ask Price': 6,
	# 	'Bid Qty': 5,
	# 	'Ask Qty': 7,
	# 	'Volume': 10
	# },
	# 'SGXQ@CN2410': {
		'Last Price': 8,
		'Last qty': 9,
		'Bid Price': 4,
		'Ask Price': 6,
		'Bid Qty': 5,
		'Ask Qty': 7,
		'Volume': 10
	# },
}

thread_status = True

symbols = ["LME@CA3M", "SGXQ@NK2412", "BMD@FCPO2501", "KRX@101VC", "SGXQ@UC2412", "SGXQ@CN2410"]

staticText = "name\nLast Price\nLast Qty\nBid Price\nBid Qty\nAsk Price\nAsk Qty\nVolume\nPreSettlement\nHigh\nLow\nOpen"

kb = KeyBindings()

@kb.add("c-c")
@kb.add("c-q")
def _(event):
	thread_status = False
	# event.app.thread.kill()
	event.app.exit()

data = {'LME@CA3M': {'Last Price': '', 'Last Qty': '', 'Volume': '', 'High': '', 'Low': '', 'Open': '', 'PreSettlement': '', "Bid Price": "", "Ask Price": "", 'Bid Qty': '', "Ask Qty": ''}, 'SGXQ@NK2412': {'Last Price': '', 'Last Qty': '', 'Volume': '', 'High': '', 'Low': '', 'Open': '', 'PreSettlement': '', "Bid Price": "", "Ask Price": "", 'Bid Qty': '', "Ask Qty": ''}, 'BMD@FCPO2501': {'Last Price': '', 'Last Qty': '', 'Volume': '', 'High': '', 'Low': '', 'Open': '', 'PreSettlement': '', "Bid Price": "", "Ask Price": "", 'Bid Qty': '', "Ask Qty": ''}, 'KRX@101VC': {'Last Price': '', 'Last Qty': '', 'Volume': '', 'High': '', 'Low': '', 'Open': '', 'PreSettlement': '', "Bid Price": "", "Ask Price": "", 'Bid Qty': '', "Ask Qty": ''}, 'SGXQ@UC2412': {'Last Price': '', 'Last Qty': '', 'Volume': '', 'High': '', 'Low': '', 'Open': '', 'PreSettlement': '', "Bid Price": "", "Ask Price": "", 'Bid Qty': '', "Ask Qty": ''}, 'SGXQ@CN2410': {'Last Price': '', 'Last Qty': '', 'Volume': '', 'High': '', 'Low': '', 'Open': '', 'PreSettlement': '', "Bid Price": "", "Ask Price": "", 'Bid Qty': '', "Ask Qty": ''}}


def update_data(real_data):
	for key in keys:
		for head in table_heads:
			try:
				if real_data[key][head] == "":
					pass
				else:
					data[key][head] = real_data[key][head]
			except Exception:
				pass
	print("_______data_________")
	print(data)
		

def interpreter_first_data(total_data):
	total_interpreter_data = {}
	blocks = total_data.split('X@1A')
	for item in blocks:
		for key in keys:
			if key in item:
				if key == "LME@CA3M":
					each_data = item.split(key)
					total_data = {}
					each_data_1 = each_data[1].split("@")
					each_data_2 = each_data[2].split("@")
					total_data['Last Price'] = each_data_1[6]
					total_data['Last Qty'] = each_data_1[7]
					total_data['Volume'] = each_data_1[8]
					total_data['High'] = each_data_2[1]
					total_data['Low'] = each_data_2[2]
					total_data['Open'] = each_data_2[3]
					total_data['PreSettlement'] = each_data_2[5]
					total_interpreter_data['LME@CA3M'] = total_data
				elif key == 'SGXQ@NK2412':
					each_data = item.split(key)
					total_data = {}
					each_data_1 = each_data[1].split("@")
					each_data_2 = each_data[2].split("@")
					# print(each_data_1)
					# print(each_data_2)
					total_data['Last Price'] = each_data_1[6]
					total_data['Last Qty'] = each_data_1[7]
					total_data['Volume'] = each_data_1[8]
					total_data['High'] = each_data_2[1]
					total_data['Low'] = each_data_2[2]
					total_data['Open'] = each_data_2[3]
					total_data['PreSettlement'] = each_data_2[5]
					total_interpreter_data['SGXQ@NK2412'] = total_data
					# print(total_data)
				elif key == 'BMD@FCPO2501':
					each_data = item.split(key)
					total_data = {}
					each_data_1 = each_data[1].split("@")
					each_data_2 = each_data[2].split("@")
					total_data['Last Price'] = each_data_1[6]
					total_data['Last Qty'] = each_data_1[7]
					total_data['Volume'] = each_data_1[8]
					total_data['High'] = each_data_2[1]
					total_data['Low'] = each_data_2[2]
					total_data['Open'] = each_data_2[3]
					total_data['PreSettlement'] = each_data_2[5][0]
					total_interpreter_data['BMD@FCPO2501'] = total_data
					# print(each_data_1)
					# print(each_data_2)
					# print(total_data)
				elif key == 'KRX@101VC':
					each_data = item.split(key)
					total_data = {}
					each_data_1 = each_data[1].split("@")
					each_data_2 = each_data[2].split("@")
					total_data['Last Price'] = each_data_1[6]
					total_data['Last Qty'] = each_data_1[7]
					total_data['Volume'] = each_data_1[8]
					total_data['High'] = each_data_2[1]
					total_data['Low'] = each_data_2[2]
					total_data['Open'] = each_data_2[3]
					total_data['PreSettlement'] = each_data_2[5]
					total_interpreter_data['KRX@101VC'] = total_data
					# print(each_data_1)
					# print(each_data_2)
					# print(total_data)
				elif key == 'SGXQ@UC2412':
					each_data = item.split(key)
					total_data = {}
					each_data_1 = each_data[1].split("@")
					each_data_2 = each_data[2].split("@")
					# print(each_data_1)
					# print(each_data_2)
					total_data['Last Price'] = each_data_1[6]
					total_data['Last Qty'] = each_data_1[7]
					total_data['Volume'] = each_data_1[8]
					total_data['High'] = each_data_2[1]
					total_data['Low'] = each_data_2[2]
					total_data['Open'] = each_data_2[3]
					total_data['PreSettlement'] = each_data_2[5]
					total_interpreter_data['SGXQ@UC2412'] = total_data
					# print(total_data)
				elif key == 'SGXQ@CN2410':
					each_data = item.split(key)
					total_data = {}
					each_data_1 = each_data[1].split("@")
					each_data_2 = each_data[2].split("@")
					# print(each_data_1)
					# print(each_data_2)
					total_data['Last Price'] = each_data_1[6]
					total_data['Last Qty'] = each_data_1[7]
					total_data['Volume'] = each_data_1[8]
					total_data['High'] = each_data_2[1]
					total_data['Low'] = each_data_2[2]
					total_data['Open'] = each_data_2[3]
					total_data['PreSettlement'] = each_data_2[5]
					total_interpreter_data['SGXQ@CN2410'] = total_data
					# print(total_data)
	return total_interpreter_data

def decoder(data):
	ascii_parts = []
	for byte in data:
		if 32 <= byte <= 126:  # ASCII printable characters
			ascii_parts.append(chr(byte))
		else:
			ascii_parts.append('.')
	decoded_string = ''.join(ascii_parts)
	return decoded_string

def create_socket():
	client = socket(AF_INET, SOCK_STREAM)
	client.connect((host, port))

	return client

def start():
	try:
		client = socket(AF_INET, SOCK_STREAM)
		client.connect((host, port))
		client.send(data2.encode())

		while thread_status:
			data = client.recv(5000)
			data1 = decoder(data)

			# print(data1)
			if len(data1) >= 1024:
				real_data = interpreter_first_data(data1)
			else:

				if '}{' in data1:
					_data1 = data1.split('}{')
				else:
					_data1 = [ data1 ]
				for data in _data1:
					tmp = data.split('@')
					for key in keys:
						for idx_key, idx in parseIndex.items():
							try:
								real_data[key][idx_key] = tmp[idx]
							except:
								pass
			update_data(real_data)
	except Exception as err:
		client.close()
		time.sleep(2)
		start()

start()