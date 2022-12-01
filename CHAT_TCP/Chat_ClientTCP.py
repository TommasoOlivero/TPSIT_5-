import socket
from threading import Thread

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
stringa = ""

s.bind(("0.0.0.0", 8000))
s.connect(("192.168.0.131", 8000))  #INSERIRE IP SERVER

class Receiver(Thread):
    def __init__(self, s):
        Thread.__init__(self)
        self.s = s
        self.running = True

    def run(self):
        while self.running:
            dati = self.s.recv(4096)
            print(f"\n{dati.decode()}")

    def stop(self):
        self.running = False
      
def main():
    t1 = Receiver(s)
    t1.start()

    while True:
        dest = input("DESTINATARIO: ")
        messaggio = input("MESSAGGIO: ")

        stringa = messaggio + "|" + dest

        s.sendall(stringa.encode())

    s.close()

if __name__ == "__main__":
    main()