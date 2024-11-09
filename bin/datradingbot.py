import asyncio
import threading
import time
import math

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

		# The wiener process parameter of Brownian Motion
sigma = 2
		
		# Cash
x = [0]
		
		# Risk Factor (->0: high risk  ->1: low risk) 
gamma = 0.1
		
		# Limit Horizon
limit_horizon = True
		
		# Market Model
k = 1.5
		
		# Reserve Price
r = [0]
		
		# Bid price
rb = [0]
		
		# Ask price
ra = [0]
		
		# Last Price - mid-price
s = [0]
		
		# Quality of stocks
q = [0,0]
		
		# Max of quality
q_max = 10
		
		# PnL
pnl = [0,0]
exchange = "LME@CA3M"


thread_status = True

cnt = 0

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

def calculate(): # param: isFirst
	if False:
		s.append(data[exchange]["Last Price"])
	else:
		s.append(eval(data[exchange]["Last Price"]))
			
		bid_price = eval(data[exchange]["Bid Price"])
		ask_price = eval(data[exchange]["Ask Price"])
		bid_qty = eval(data[exchange]["Bid Qty"])
		ask_qty = eval(data[exchange]["Ask Qty"])
			
		r.append(s[-1] - q[-1] * gamma * sigma**2*(1 - len(s) * 0.001))
		# print(r)
		r_spead = 2 / gamma * math.log(1 + gamma / k)
			
		ra.append(r[-1] + r_spead / 2)
		rb.append(r[-1] - r_spead / 2)
		# t.append(1)
		
		dNa = 0
		dNb = 0
		if ra[-1] < ask_price:
			dNa = 1
			
		if rb[-1] > bid_price:
			dNb = 1
		
		qty = q[-1] - dNa + dNb
		if(qty < q_max and qty > - q_max):
			pnl.append(pnl[-1] + ra[-1] * dNa - rb[-1] * dNb - s[-1] * (dNa - dNb))
			q.append(qty)
			x.append(x[-1] + ra[-1] * dNa - rb[-1] * dNb)
		else:
			pnl.append(pnl[-1])
			q.append(q[-1])
			x.append(x[-1])
		# print(pnl)
			
		# if cnt == 1000:
		# 	refresh()
		# else:
		# 	cnt = cnt + 1

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
	# print("__data__\n" , data)
	calculate()
	# print("__data_s__")
	# print(s)
	# print("__data__")
	# print(data)
		

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
					# print(each_data_1)
					each_data_2 = each_data[2].split("@")
					total_data['Bid Price'] = each_data_1[2]
					total_data['Ask Price'] = each_data_1[4]
					total_data['Ask Qty'] = each_data_1[3]
					total_data['Bid Qty'] = each_data_1[5]
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
					# print(each_data_1)
					each_data_2 = each_data[2].split("@")
					# print(each_data_1)
					# print(each_data_2)
					total_data['Bid Price'] = each_data_1[2]
					total_data['Ask Price'] = each_data_1[4]
					total_data['Ask Qty'] = each_data_1[3]
					total_data['Bid Qty'] = each_data_1[5]
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
					# print(each_data_1)
					each_data_2 = each_data[2].split("@")
					total_data['Bid Price'] = each_data_1[2]
					total_data['Ask Price'] = each_data_1[4]
					total_data['Ask Qty'] = each_data_1[3]
					total_data['Bid Qty'] = each_data_1[5]
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
					# print(each_data_1)
					each_data_2 = each_data[2].split("@")
					total_data['Bid Price'] = each_data_1[2]
					total_data['Ask Price'] = each_data_1[4]
					total_data['Ask Qty'] = each_data_1[3]
					total_data['Bid Qty'] = each_data_1[5]
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
					# print(each_data_1)
					each_data_2 = each_data[2].split("@")
					# print(each_data_1)
					# print(each_data_2)
					total_data['Bid Price'] = each_data_1[2]
					total_data['Ask Price'] = each_data_1[4]
					total_data['Ask Qty'] = each_data_1[3]
					total_data['Bid Qty'] = each_data_1[5]
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
					# print(each_data_1)
					each_data_2 = each_data[2].split("@")
					# print(each_data_1)
					# print(each_data_2)
					total_data['Bid Price'] = each_data_1[2]
					total_data['Ask Price'] = each_data_1[4]
					total_data['Ask Qty'] = each_data_1[3]
					total_data['Bid Qty'] = each_data_1[5]
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
			# print("hello")
			recv_data = client.recv(5000)
			data1 = decoder(recv_data)

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
						if key in data:
							for idx_key, idx in parseIndex.items():
								try:
									if len(tmp[idx]) <= 7:
										real_data[key][idx_key] = tmp[idx].replace('{','').replace('}', '')
								except:
									pass
				# print("__data__")
				# print(real_data)
				# if real_data['LME@CA3M']["Bid Price"] < 100:
				# # print("____data_____")
				# # print(data1)
				# 	pass
		
			# print(data)
			update_data(real_data)
	except Exception as err:
		client.close()
		time.sleep(2)
		# print(err)
		start()
	 


class DATradingBot:
	def __init__(self):
		# self.f = plt.figure(figsize = (15, 4))
  
		# self.t = [1]
  		# # The wiener process parameter of Brownian Motion
		# self.sigma = 2
		
		# # Cash
		# self.x = [0]
		
		# # Risk Factor (->0: high risk  ->1: low risk) 
		# self.gamma = 0.1
		
		# # Limit Horizon
		# self.limit_horizon = True
		
		# # Market Model
		# self.k = 1.5
		
		# # Reserve Price
		# self.r = [0]
		
		# # Bid price
		# self.rb = [0]
		
		# # Ask price
		# self.ra = [0]
		
		# # Last Price - mid-price
		# self.s = [0]
		
		# # Quality of stocks
		# self.q = [0]
		
		# # Max of quality
		# self.q_max = 10
		
		# # PnL
		# self.pnl = [0]
		# self.exchange = "LME@CA3M"
		
		
		self.static_windows = [Window(content = FormattedTextControl(text=staticText), height = 12)]
		for i in range(6):
			self.static_windows.append(Window(content = FormattedTextControl(text=f"value\n\n\n\n\n\n\n\n\n\n"), height = 12)) 
		
		self.result_window = Window(content = FormattedTextControl(text="\n\n\n\n\n"), height = 12)
		
		self.container = HSplit(
			[
				VSplit(
					[
						self.generate_frame(1),
						self.generate_frame(2),
						self.generate_frame(3)
					]
				),
				VSplit(
					[
						self.generate_frame(4),
						self.generate_frame(5),
						self.generate_frame(6)
					]
				),
				VSplit(
					[
						Frame(
							body = VSplit(
								[
									Window(content = FormattedTextControl(text="mid-price\nask-price\nbid-price\npnl\ncash\nQty"), height = 12),
									self.result_window
								]
							)
						)
					]
				)
			]
		)
		
		self.frame = Frame(
			title = "DA Trader( https://directaccess.com.hk)",
			body = self.container,
		)

		self.app= Application(
			layout=Layout(self.frame),
			key_bindings=kb,
			mouse_support=True,
			full_screen=True,
			refresh_interval = 1
		)   
		
		self.app.create_background_task(self.refresh())
		
		self.thread = threading.Thread(target = start)
		self.thread.start()
	
	def generate_frame(self, index):
		return Frame(
			title = symbols[index - 1],
			body = VSplit(
				[
					self.static_windows[0],
					self.static_windows[index]
				]
			)
		)
	
	async def refresh(self):
		while True:
			# data1 = data['LME@CA3M']["Bid Price"]
			data1 = data['LME@CA3M']
			data2 = data['SGXQ@NK2412']
			data3 = data['BMD@FCPO2501']
			data4 = data['KRX@101VC']
			data5 = data['SGXQ@UC2412']
			data6 = data['SGXQ@CN2410']
			
			self.static_windows[1].content.text = f'value\n{data1["Last Price"]}\n{data1["Last Qty"]}\n{data1["Bid Price"]}\n{data1["Bid Qty"]}\n{data1["Ask Price"]}\n{data1["Ask Qty"]}\n{data1["Volume"]}\n{data1["PreSettlement"]}\n{data1["High"]}\n{data1["Low"]}\n{data1["Open"]}'
			self.static_windows[2].content.text = f'value\n{data2["Last Price"]}\n{data2["Last Qty"]}\n{data2["Bid Price"]}\n{data2["Bid Qty"]}\n{data2["Ask Price"]}\n{data2["Ask Qty"]}\n{data2["Volume"]}\n{data2["PreSettlement"]}\n{data2["High"]}\n{data2["Low"]}\n{data2["Open"]}'
			self.static_windows[3].content.text = f'value\n{data3["Last Price"]}\n{data3["Last Qty"]}\n{data3["Bid Price"]}\n{data3["Bid Qty"]}\n{data3["Ask Price"]}\n{data3["Ask Qty"]}\n{data3["Volume"]}\n{data3["PreSettlement"]}\n{data3["High"]}\n{data3["Low"]}\n{data3["Open"]}'
			self.static_windows[4].content.text = f'value\n{data4["Last Price"]}\n{data4["Last Qty"]}\n{data4["Bid Price"]}\n{data4["Bid Qty"]}\n{data4["Ask Price"]}\n{data4["Ask Qty"]}\n{data4["Volume"]}\n{data4["PreSettlement"]}\n{data4["High"]}\n{data4["Low"]}\n{data4["Open"]}'
			self.static_windows[5].content.text = f'value\n{data5["Last Price"]}\n{data5["Last Qty"]}\n{data5["Bid Price"]}\n{data5["Bid Qty"]}\n{data5["Ask Price"]}\n{data5["Ask Qty"]}\n{data5["Volume"]}\n{data5["PreSettlement"]}\n{data5["High"]}\n{data5["Low"]}\n{data5["Open"]}'
			self.static_windows[6].content.text = f'value\n{data6["Last Price"]}\n{data6["Last Qty"]}\n{data6["Bid Price"]}\n{data6["Bid Qty"]}\n{data6["Ask Price"]}\n{data6["Ask Qty"]}\n{data6["Volume"]}\n{data6["PreSettlement"]}\n{data6["High"]}\n{data6["Low"]}\n{data6["Open"]}'
			self.result_window.content.text = f'{s[-1]}\n{ra[-1]}\n{rb[-1]}\n{pnl[-1]}\n{x[-1]}\n{q[-1]}'
			# print(f'{s[-1]}\n{ra[-1]}\n{rb[-1]}\n{pnl[-1]}\n{x[-1]}\n{q[-1]}')
			await asyncio.sleep(1)
	
	# def redraw(self):
	#	 self.app.invalidate()
	
	def run(self):
		self.app.run()
	
  
  
if __name__ == "__main__":
	start()
		

