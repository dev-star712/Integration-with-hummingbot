from math import sqrt
from scipy.stats import norm
import numpy as np
import matplotlib.pyplot as plt

import threading
import time
import math

from socket import *

host = '222.73.120.40'
port = 9794

# data2 = "{(len=92)MARKET01@@@+T@1@@@@@@@0@&LME,CA3M;SGXQ,NK2412;BMD,FCPO2501;KRX,101VC;SGXQ,UC2412;SGXQ,CN2410}"
data2 = "{(len=38)MARKET01@@@+T@1@@@@@@@0@&LME,CA3M;SGXQ}"

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

cnt = 1

thread_status = True

symbols = ["LME@CA3M", "SGXQ@NK2412", "BMD@FCPO2501", "KRX@101VC", "SGXQ@UC2412", "SGXQ@CN2410"]

staticText = "name\nLast Price\nLast Qty\nBid Price\nBid Qty\nAsk Price\nAsk Qty\nVolume\nPreSettlement\nHigh\nLow\nOpen"


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




def brownian(x0, n, dt, delta, out=None):
    """
    Generate an instance of Brownian motion (i.e. the Wiener process):

        X(t) = X(0) + N(0, delta**2 * t; 0, t)

    where N(a,b; t0, t1) is a normally distributed random variable with mean a and
    variance b.  The parameters t0 and t1 make explicit the statistical
    independence of N on different time intervals; that is, if [t0, t1) and
    [t2, t3) are disjoint intervals, then N(a, b; t0, t1) and N(a, b; t2, t3)
    are independent.
    
    Written as an iteration scheme,

        X(t + dt) = X(t) + N(0, delta**2 * dt; t, t+dt)


    If `x0` is an array (or array-like), each value in `x0` is treated as
    an initial condition, and the value returned is a numpy array with one
    more dimension than `x0`.

    Arguments
    ---------
    x0 : float or numpy array (or something that can be converted to a numpy array
         using numpy.asarray(x0)).
        The initial condition(s) (i.e. position(s)) of the Brownian motion.
    n : int
        The number of steps to take.
    dt : float
        The time step.
    delta : float
        delta determines the "speed" of the Brownian motion.  The random variable
        of the position at time t, X(t), has a normal distribution whose mean is
        the position at time t=0 and whose variance is delta**2*t.
    out : numpy array or None
        If `out` is not None, it specifies the array in which to put the
        result.  If `out` is None, a new numpy array is created and returned.

    Returns
    -------
    A numpy array of floats with shape `x0.shape + (n,)`.
    
    Note that the initial value `x0` is not included in the returned array.
    """

    x0 = np.asarray(x0)

    print(x0)

    # For each element of x0, generate a sample of n numbers from a
    # normal distribution.
    r = norm.rvs(size=x0.shape + (n,), scale=delta*sqrt(dt))

    # If `out` was not given, create an output array.
    if out is None:
        out = np.empty(r.shape)

    # This computes the Brownian motion by forming the cumulative sum of
    # the random samples. 
    np.cumsum(r, axis=-1, out=out)

    # Add the initial condition.
    out += np.expand_dims(x0, axis=-1)

    return out


f = plt.figure(figsize = (15, 4))
t = [1]
        
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
q = [0]
        
        # Max of quality
q_max = 10
        
        # PnL
pnl = [0]
exchange = "LME@CA3M"
thread_sock = threading.Thread(target=self.start)
thread_disp = threading.Thread(target=self.display)
        
    
def setPram():
    print(
        "Input a number between 1 to 6.",
        "1.",
        "2.",
        "3.",
        "4.",
        "5.",
        "6.",
    )
        
    exchange = eval(input("Exchange: "))
    
    def run(self):
        pass
    
def refresh(self):
    x = [0]
    r = [0]
    rb = [0]
    ra = [0]
    s = [self.s[-1]]
    q = [0]
    q_max = 10
    cnt = 0
        
        
def display(self):
    f.add_subplot(1,3, 1)
    plt.plot(self.t, self.s, color='black', label='Mid-market price')
    plt.plot(self.t, self.r, color='blue', linestyle='dashed', label='Reservation price')
    plt.plot(self.t, self.ra, color='red', linestyle='', marker='.', label='Price asked', markersize='4')
    plt.plot(self.t, self.rb, color='lime', linestyle='', marker='o', label='Price bid', markersize='2')
    plt.xlabel('Time', fontsize=16)
    plt.ylabel('Price [USD]', fontsize=16)
    plt.grid(True)
    plt.legend()

    f.add_subplot(1,3, 2)
    plt.plot(self.t, self.pnl, color='black', label='P&L')
    plt.xlabel('Time', fontsize=16)
    plt.ylabel('PnL [USD]', fontsize=16)
    plt.grid(True)
    plt.legend()

    f.add_subplot(1,3, 3)
    plt.plot(self.t, self.q, color='black', label='Stocks held')
    plt.xlabel('Time', fontsize=16)
    plt.ylabel('Inventory', fontsize=16)
    plt.grid(True)
    plt.legend()

    plt.pause(5)
    
def calculate(self, isFirst):
        if isFirst:
            self.s.append(data[self.exchange]["Last Price"])
        else:
            self.s.append(data[self.exchange]["Last Price"])
            
            bid_price = data[self.exchange]["Bid Price"]
            ask_price = data[self.exchange]["Ask Price"]
            bid_qty = data[self.exchange]["Bid Qty"]
            ask_qty = data[self.exchange]["Ask Qty"]
            
            self.r.append(self.s[-1] - q[-1] * self.gamma * self.sigma**2*(1 - cnt * 0.001))
            r_spead = 2 / self.gamma * math.log(1 + self.gamma / k)
            
            self.ra.append(self.r[-1] + r_spead / 2)
            self.rb.append(self.r[-1] - r_spead / 2)
            self.t.append(1)
            
            dNa = 0
            dNb = 0
            if self.ra[-1] < ask_price:
                dNa = 1
            
            if self.rb[-1] > bid_price:
                dNb = 1
            
            qty = self.q[-1] - dNa + dNb
            if(qty < self.q_max and qty > - self.q_max):
                self.pnl.append(self.pnl[-1] + self.ra[-1] * dNa - self.rb[-1] * dNb - self.s[-1](dNa - dNb))
                self.q.append(qty)
                self.x.append(x[-1] + self.ra[-1] * dNa - self.rb[-1] * dNb)
            else:
                self.pnl.append(self.pnl[-1])
                self.q.append(self.q[-1])
                self.x.append(self.x[-1])
            
            if cnt == 1000:
                self.refresh()
            else:
                cnt = cnt + 1
        
        
    def start(self):
        try:
            client = socket(AF_INET, SOCK_STREAM)
            # self.display()
            client.connect((host, port))
            client.send(data2.encode())

            while thread_status:
                # self.display()
                data = client.recv(5000)
                data1 = decoder(data)
                print("________data__________")
                print(data1)

                # print(data1)
        #         if len(data1) >= 1024:
        #             real_data = interpreter_first_data(data1)
        #             update_data(real_data)
        #             self.calculate(True)
        #         else:

        #             if '}{' in data1:
        #                 _data1 = data1.split('}{')
        #             else:
        #                 _data1 = [ data1 ]
        #             for data in _data1:
        #                 tmp = data.split('@')
        #                 for key in keys:
        #                     if key in data:
        #                         for idx_key, idx in parseIndex.items():
        #                             try:
        #                                 if len(tmp[idx]) <= 7:
        #                                     real_data[key][idx_key] = tmp[idx].replace('{','').replace('}', '')
        #                             except:
        #                                 pass
        #             update_data(real_data)
        #             self.calulate(False)
        #         print(real_data)
        except Exception as err:
            client.close()
            time.sleep(2)
            self.start()
            
            
    def stop(self):
        thread_status = False
        
    def run(self):
        self.thread_sock.start()
        # self.thread_disp.start()
        
if __name__ == "__main__":
    dabot = DABot()
    dabot.start()
    
        