import socket
import threading
import time
from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox

server_port = 9090
chisla = '0123456789'
host_ip = ''


def receving(name, sock):
    global txt, shutdown
    while not shutdown:
        try:
            while True:
                data, addr = sock.recvfrom(1024)
                txt.insert(INSERT, data.decode('utf-8') + '\n')
                window.mainloop()
                time.sleep(0.2)
        except:
            pass


def CheckIP(IP):
    global chisla
    flag = True
    for i in IP:
        if i != '.':
            if i not in chisla:
                flag = False
                break
    return flag


def CheckPort(port):
    try:
        port = int(port)
        return True
    except:
        return False


def clickedIP():
    global host_ip
    if not CheckIP(txtIP.get()):
        messagebox.showinfo('ERROR', 'Error format of server address')

    else:
        host_ip = txtIP.get()
        resIP = "Server IP: " + txtIP.get()
        lblIP.configure(text=resIP)


def clickedPort():
    global server_port
    if not CheckPort(txtPort.get()):
        messagebox.showinfo('ERROR', 'Error format of server port')
    else:
        server_port = int(txtPort.get())
        resPort = "Server Port: " + txtPort.get()
        lblPort.configure(text=resPort)


def clickedName():
    global server, server_port, message, join, host_ip, alias
    server = ['', 0]
    if host_ip == '' or CheckPort(server_port) == False:
        messagebox.showinfo('ERROR', 'Incorrect address or port\n')
    else:
        server[0] = host_ip
        server[1] = server_port
        server = tuple(server)
        alias = txtName.get()
        resName = "Your Name: " + txtName.get()
        lblName.configure(text=resName)
        if join == False:
            s.sendto(("[" + alias + "] => join chat ").encode('utf-8'), server)
            txt.insert(INSERT, 'Success conection\n')
            join = True


def clickedMessage():
    global server, server_port, message, shutdown, host_ip, alias, s
    server = ['', '']
    message = txtMess.get()
    server[0] = host_ip
    server[1] = server_port
    server = tuple(server)

    try:
        if message != "":
            # print(message)
            s.sendto(("[" + alias + "] :: " + message).encode('utf-8'), server)
            txt.insert(INSERT, message + '\n')

        time.sleep(0.1)
    except:

        s.sendto(("[" + alias + "] <= left chat ").encode('utf-8'), server)
        shutdown = True


window = Tk()
window.title("Welcome to the Chat")
window.geometry('466x270')

message = ''
host_ip = ''

lblIP = Label(window, text="Server IP: ")
lblIP.grid(column=0, row=0)

lblName = Label(window, text="Your Name: ")
lblName.grid(column=0, row=2)

lblPort = Label(window, text="Server Port: ")
lblPort.grid(column=0, row=1)
lblPort.configure(text="Server Port: " + str(server_port))

txtIP = Entry(window, width=10)
txtIP.grid(column=1, row=0)
txtIP.focus()

txtPort = Entry(window, width=10)
txtPort.grid(column=1, row=1)

txtName = Entry(window, width=10)
txtName.grid(column=1, row=2)

txtMess = Entry(window, width=51)
txtMess.grid(column=0, row=4)

txt = scrolledtext.ScrolledText(window, width=40, height=10)
txt.grid(column=0, row=3)

btnIP = Button(window, text="Set IP", command=clickedIP)
btnIP.grid(column=2, row=0)

btnPort = Button(window, text="Set Port", command=clickedPort)
btnPort.grid(column=2, row=1)

btnName = Button(window, text="Set Name", command=clickedName)
btnName.grid(column=2, row=2)

btnMess = Button(window, text="Send", command=clickedMessage)
btnMess.grid(column=1, row=4)

shutdown = False
join = False

host = socket.gethostbyname(socket.gethostname())

port = 0

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(0)

rT = threading.Thread(target=receving, args=("RecvThread", s))
rT.start()

window.after(0, clickedMessage)
window.mainloop()
rT.join()

s.close()
