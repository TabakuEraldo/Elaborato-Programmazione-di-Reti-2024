import socket
import threading

# Questa funzione gestisce la connessione dei client al server
def gestisciConnessione(client_socket, client_address):
    print(f"Connessione con: {client_address} accettata")
    try:
        while True:
            # Vengono ricevuti messaggi dal client
            message = client_socket.recv(1024).decode("utf-8")
            if not message:
                break
            print(f"Client {client_address}: {message}")
            
            # Rimozione dei client disconnessi dalla lista dei client ancora connessi
            
            disconnected_clients = []
            for c in clients:
                if c.fileno() == -1:
                    disconnected_clients.append(c)
            for dc in disconnected_clients:
                clients.remove(dc)
            
            message_with_sender = f"{client_address[0]}:{client_address[1]} - {message}"
            
            # Indirizzamento del messaggio a tutti i client connessi
            for c in clients:
                if c != client_socket:
                    try:
                        c.send(message_with_sender.encode("utf-8"))
                    except Exception as e:
                        print(f"Errore durante l'invio del messaggio a {c}: {e}")
                        # Rimuovi il client dalla lista dei client ancora connessi
                        clients.remove(c)
    except Exception as e:
        print(f"Si è verificato un errore durante la comunicazione con il client: {client_address}")
    finally:
        # viene chiusa la connessione con il client disconnesso
        client_socket.close()
        print(f"ATTENZIONE : Connessione con il client {client_address} chiusa")



# Indirizzo e porta per connessione al server

HOST = '0.0.0.0'
PORT = 5555

clients = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))

server_socket.listen(5)
print(f"In attesa di connessioni da parte dei client...")

# Accetta e gestisci le connessioni dei client in modo concorrente
while True:
    
    client_socket, client_address = server_socket.accept()

    clients.append(client_socket)

    client_thread = threading.Thread(target=gestisciConnessione, args=(client_socket, client_address))
    client_thread.start()
