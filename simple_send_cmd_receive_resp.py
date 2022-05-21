# simple program to send AT commands for testing purposes
# includes +++ with delay of 1 sec before command and 1 sec after command, before sending \r\n
# special commands:
#    CTRL-START will restart the module (power off/on etc) = initialisation
#    <eof> will send \x1A (EOF)
#    <ncr> at the end of command will prevent from sending '\r' at end of line
#    <cr> will only send '\r' and ignore all the rest on the line

import _thread  as thread
import time
from machine import Pin, UART

# init outputs
#pwr_key = 4
#led = 12
pwr_key = Pin(4, Pin.OUT)
led_blue = Pin(12, Pin.OUT)

data = ""
msg = b''
received_msg = ""
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

    
def get_input():
    global data 
    while 1:
        data = input()
        #print("data entered = :",data)
    


def write_command(data_to_send):
    if(data_to_send == "CTRL-START"):
        SIM_start()
    else:
        if(data_to_send == "<eof>"):
            print("write to UART: EOF")
            uart2.write(b'\x1A')
        if("<ncr>" in data_to_send): #no CR at the end
            data_to_send = data_to_send.replace("<ncr>","")
            print("write to UART:",data_to_send, " without CR")
            uart2.write((data_to_send).encode())
        elif ("<cr>" in data_to_send): #only CR
            print("write to UART: only CR")
            uart2.write(b'\r')         
        else:
            print("write to UART:",data_to_send,"<CR> (with CR)")
            time.sleep(1) #some command require a 1 sec delay before \r is send
            uart2.write((data_to_send + "\r").encode())


get_input_thread = thread.start_new_thread(get_input, ())  #upython versie  lege tuple indien geen argumenten worden doorgegeven


while 1:
    while uart2.any() > 0 :
        try:
            msg = uart2.read(1).decode("utf-8")
            if msg == "\r":
                print('\033[32m',"<CR>",'\033[0m',sep="",end="")
            elif msg == "\n":
                print('\033[32m',"<LF>",'\033[0m',sep="")
            else:
                print(msg,end="")           
        except Exception as e:
            print("exception in receive_from_gsm =",e)
            
            
    if data != "":
        #print("new data=" , data)
        write_command(data)
        data =""
