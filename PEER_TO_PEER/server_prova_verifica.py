import socket
from threading import Thread
import sqlite3

class Receiver(Thread):
    def __init__(self, s, connection, address):
        Thread.__init__(self)
        self.s = s
        self.connection = connection
        self.address = address
        self.running = True

    def run(self):
        while self.running:
            con = sqlite3.connect("file.db")
            cur = con.cursor()
            dati = self.connection.recv(4096).decode()
            print(dati)

            parametri = dati.split("|")
            print(parametri[0])
            print(parametri[1])
            print(parametri[2])

            if(int(parametri[0]) == 1):
                res = cur.execute("SELECT nome FROM files WHERE nome LIKE \"" + str(parametri[1]) + "%\"")
                ris = res.fetchone()
                #print(ris[0].split(".")[0])
                
                if ris is None:
                    self.connection.sendall("File inesistente nel database".encode())
                elif ris[0].split(".")[0] == parametri[1] :
                    self.connection.sendall("File esistente nel database".encode())
                
            elif(int(parametri[0]) == 2):
                res = cur.execute("SELECT tot_frammenti FROM files WHERE nome LIKE \"" + str(parametri[1]) + "%\"")
                ris = res.fetchone()
                
                if ris is None:
                    self.connection.sendall("file non trovato o non presenza di frammenti".encode())
                elif ris[0] >= 0:
                    risposta = "numero frammneti: " + str(ris[0])
                    self.connection.sendall(risposta.encode())

            elif(int(parametri[0]) == 3):
                res = cur.execute("SELECT host FROM files,frammenti WHERE files.id_file = frammenti.id_file AND nome LIKE \"" + str(parametri[1]) + "%\" AND n_frammento = " + str(parametri[2]))
                ris = res.fetchone()
                
                if ris is None:
                    self.connection.sendall("host non trovato".encode())
                elif ris[0] is not None:
                    risposta = "host: " + str(ris[0])
                    self.connection.sendall(risposta.encode())

            elif(int(parametri[0]) == 4):
                res = cur.execute("SELECT host FROM files,frammenti WHERE files.id_file = frammenti.id_file AND nome LIKE \"" + str(parametri[1]) + "%\"")
                ris = res.fetchall()
                print(ris)
                
                if ris is None:
                    self.connection.sendall("host non trovato".encode())
                elif ris is not None:
                    risposta = "lista host: " + str(ris)
                    self.connection.sendall(risposta.encode())



def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("192.168.1.9", 5000))
    dispositivi = []

    while(True):
        s.listen()
        connection, address = s.accept()

        r = Receiver(s, connection, address)
        dispositivi.append(r.start())
        #r.start()
        
if __name__ == "__main__":
    main()
