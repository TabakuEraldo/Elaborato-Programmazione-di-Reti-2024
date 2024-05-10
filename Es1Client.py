import socket
import threading
import tkinter as tk
import sys

def riceviMessaggi():
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            if not message:
                break
            chat_box.insert(tk.END, message + '\n')
        except Exception as e:
            print("Si e' verificato un errore durante la ricezione del messaggio")
            break

def inviaMessaggi(event=None):
    try:
        message = message_entry.get()
        chat_box.insert(tk.END, aggiungiMittente(message) + '\n')
        chat_box.see(tk.END) 
        client_socket.send(message.encode("utf-8"))
        message_entry.delete(0, tk.END)
    except Exception as e:
        print("Si e' verificato un errore durante l'invio del messaggio")

def chiusura():
    client_socket.close()
    root.destroy()
    sys.exit()

def aggiungiMittente(message):
    return f"Client: {message}"

# Indirizzo e porta del server
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5555

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect((SERVER_HOST, SERVER_PORT))
except Exception as e:
    print("Si e' verificato un errore durante la connessione al server")
    exit()

# GUI
root = tk.Tk()
root.title("Chatroom")
root.protocol("WM_DELETE_WINDOW", chiusura)

chat_frame = tk.Frame(root)
chat_frame.pack(pady=10)

scrollbar = tk.Scrollbar(chat_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

chat_box = tk.Text(chat_frame, height=20, width=50, yscrollcommand=scrollbar.set)
chat_box.pack(side=tk.LEFT, fill=tk.BOTH)
scrollbar.config(command=chat_box.yview)

message_entry = tk.Entry(root, width=50)
message_entry.pack(pady=10)
message_entry.bind("<Return>", inviaMessaggi)

send_button = tk.Button(root, text="Invia", command=inviaMessaggi)
send_button.pack()

# Thread per la ricezzione dei messaggi
receive_thread = threading.Thread(target=riceviMessaggi)
receive_thread.start()

root.mainloop()
