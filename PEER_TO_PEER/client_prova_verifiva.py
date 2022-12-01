import socket
from threading import Thread

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

def menu():
    print("\n1- controllare se un file è presente")
    print("2- numero di frammenti di un file")
    print("3- ip dell'Host di un file e di un frammento")
    print("4- ip degli Host di un file\n")

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("192.168.1.9", 5000))    

    menu()

    while True:
        scelta, messaggio = int(input("come vuoi procedere(inserire comando da svolgere): ")), ""

        if(scelta == 1):
            param_1 = input("Inserisci nome del file: ")
            messaggio += str(scelta) + "|" + param_1 + "|0"
        elif(scelta == 2):
            param_1 = input("Inserisci nome del file: ")
            messaggio += str(scelta) + "|" + param_1 + "|0"
        elif(scelta == 3):
            param_1 = input("Inserisci nome del file: ")
            param_2 = input("Inserisci numero del frammento: ")
            messaggio += str(scelta) + "|" + param_1 + "|" + param_2
        elif(scelta == 4):
            param_1 = input("Inserisci nome del file: ")
            messaggio += str(scelta) + "|" + param_1 + "|0"

        s.sendall(messaggio.encode())

        risposta = s.recv(4096)
        print(risposta.decode())


if __name__ == "__main__":
    main()