#!/usr/bin/python

import time #sleep
import sys #exit
import signal #signal
import netServer
import RPi.GPIO as GPIO

def signal_handler(signal, frame):
    app.exit()

class App():
    def main(self):
        print("Raspi template v1.0")
        signal.signal(signal.SIGINT, signal_handler)

        #to disable RuntimeWarning: This channel is already in use
        GPIO.setwarnings(False)
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(4, GPIO.OUT)
        GPIO.setup(17, GPIO.IN)
            
        self.server = netServer.netServer()   
        self.server.onMsg = self.onMsg

        but = not GPIO.input(17)
        while True:
            b = not GPIO.input(17)
            if b != but:
                but = b
                self.server.send("Button ON" if but else "Button OFF")
            time.sleep(.1)
    
    def onMsg(self, cmd):
        if cmd[0:3] == "log":
            self.server.log = True if cmd[3] == "1" else False       
        elif cmd[0] == "l":
            GPIO.output(4, cmd[1] == "1")
        elif cmd[0] == "b":
            b = not GPIO.input(17)
            self.server.send("Button ON" if b else "Button OFF")
        
    def exit(self):
        print("\rYou pressed Ctrl+C!")
        self.server.exit()
        sys.exit(0)
        
if __name__ == '__main__':
    app = App()
    app.main()
    