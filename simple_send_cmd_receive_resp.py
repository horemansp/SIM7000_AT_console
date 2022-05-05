# simple program to send AT commands for testing purposes
# includes +++ with delay of 1 sec before command and 1 sec after command, before sending \r\n
# special commands:
#    CTRL-START will restart the module (power off/on etc) = initialisation
#    CTRL-Z will send \x1A (EOF)
#

import _thread  as thread
import time
from machine import Pin, UART

# init outputs
pwr_key = 4
led = 12
pwr_key = Pin(4, Pin.OUT)
led_blue = Pin(12, Pin.OUT)

data = ""
msg = b''
send = True

# TX2 op pin IO27 naar GSM-RT, RX2 op pin IO26 naar GSM-TX
uart2=UART(2, baudrate=115200, rx=26, tx=27, timeout=10)
uart2.init(115200, bits=8, parity=None , stop=1)

def SIM_start():
    print("Switch SIM module off/on.. wait for 10 seconds please")
    print("switch off and wait 5 seconds")
    led_blue.off()
    pwr_key.on()
    time.sleep(1.5)
    pwr_key.off()
    time.sleep(5)
    print("switch on and wait 5 seconds")
    led_blue.on()
    pwr_key.on()
    time.sleep(1)
    pwr_key.off()
    time.sleep(5)
    
def get_input():
    global data 
    while 1:
        data = input()
        #print("data entered = :",data)
    
get_input_thread = thread.start_new_thread(get_input, ())  #upython versie  lege tuple indien geen argumenten worden doorgegeven

def write_command(data_to_send):
    if(data_to_send == "CTRL-START"):
        SIM_start()
    else:
        if(data_to_send == "CTRL-Z"):
            end_to_send = '\x1A'+'\r\n'
        else:
            end_to_send = '\r\n'
        print("write to UART:",data_to_send)
        time.sleep(1) #make sure there is 1 sec of not sending anything
        uart2.write((data_to_send).encode())
        time.sleep(1) #make sure there is 1 sec delay before end is sent. (used with +++)
        uart2.write((end_to_send).encode())
        time.sleep(1)

while 1:
    while uart2.any() > 0 :
        try:
            msg = uart2.readline().decode()
            print("received:",msg)
        except Exception as e:
            print("exception in receive_from_gsm =",e)
            
    if data != "":
        #print("new data=" , data)
        write_command(data)
        data =""
        
            
        
    