import socket
from threading import Thread

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dispositivi = []

ass_nomi = {}

f = open("./ip.csv", "r")
righe = f.readlines()
for riga in righe:
    campi = riga.split(",")
    ass_nomi[campi[0]] = campi[1]

f.close()

ip_conn = {}

s.bind(("0.0.0.0", 8000))


class Receiver(Thread):
    def __init__(self, s, connection, address):
        Thread.__init__(self)
        self.s = s
        self.connection = connection
        self.address = address
        self.running = True

    def run(self):
        while self.running:
            dati = self.connection.recv(4096)
            print(f"\n{dati.decode()}")
            dati = dati.decode()
            lista = dati.split("|")
            messaggio, dest = lista[0], lista[1]

            for nome in ass_nomi:
                if nome == dest:
                    ip = ass_nomi[nome]
                    if ip in ip_conn:
                        connessione = ip_conn[ip]
                        print("trovata")
                    else:
                        connessione = self.connection

            dati = messaggio
            connessione.sendall(dati.encode())


    def stop(self):
        self.running = False

def main():

    while(True):
        print("ascolto")
        s.listen()
        connection,address = s.accept()
        ip_conn[address[0]] = connection
        r = Receiver(s, connection, address)
        dispositivi.append(r.start())  
        print(ip_conn)
    
if __name__ == "__main__":
    main()