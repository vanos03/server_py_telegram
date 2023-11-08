import socket
import time
import threading
import telebot
import sqlite3 as sql
from config.server_config import ids, token, black_list, port


flag_bot = False
msg = ''
clients = []
dangerous_masters = []
mess = ['', '']


def send_sin():
    try:
        global flag_bot
        while True:
            if flag_bot:
                global dangerous_masters, bot, itsatime, ids, mess, cur
                for id in ids:
                    bot.send_message(id,
                                     'ALERT!!!\n User '
                                     + mess[0]
                                     + 'Write is "'
                                     + mess[1]
                                     + '"\nin '
                                     + itsatime)
                    bot.send_message(id, '\nWould you like to see him logs? (Y/N)')
                flag_bot = False

                @bot.message_handler(content_types=['text'])
                def get_text_messages(message):
                    if message.text.lower() == "y":
                        cur.execute("SELECT * FROM `log`")
                        rows = cur.fetchall()

                        for name in dangerous_masters:
                            for line in rows:
                                if name in line[0]:
                                    bot.send_message(message.chat.id,
                                                     f'{line[0]}: '
                                                     + f' "{line[1]}"   in'
                                                     + line[2])

    except:
        pass

def work_bot():
    bot.polling()


con = sql.connect('log.db', uri=True, check_same_thread=False)

with con:
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS `log` (`name` STRING, `Message` STRING, `Time` STRING, `ID` STRING) ")

bot = telebot.TeleBot(token)
host = socket.gethostbyname(socket.gethostname())

itsatime = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))

print("[ Server Started ]")
print('You server adress >>> ', host + '\n')

bot_worker = threading.Thread(target=work_bot)
filtering = threading.Thread(target=send_sin)

bot_worker.start()
filtering.start()

quit = False
flag = True

while not quit:
    try:

        data, addr = s.recvfrom(500 * 1024)

        if addr not in clients:
            clients.append(addr)

        msg = str(data.decode("utf-8"))
        print('[' + addr[0] + "]=[" + str(addr[1]) + "]/", end="")
        print("[" + itsatime + "] " + data.decode("utf-8"))
        data_for_write = str(data.decode('utf-8'))

        if '] => join chat' not in data_for_write:
            Name = data_for_write.split('::')[0]
            Message = data_for_write.split('::')[1]
            Time = itsatime
            ID = str(addr[1])
            cur.execute(f"INSERT INTO `log` VALUES ('{Name}', '{Message}', '{Time}', '{ID}')")
            con.commit()

        msg_trash = msg.lower()
        msg_trash = msg_trash.replace(' ', '')
        mess = msg.split('::')

        for i in black_list:
            if i in msg_trash:
                dangerous_masters.append(mess[0])
                flag_bot = True

        for client in clients:
            if addr != client:
                s.sendto(data, client)



    except:
        print("\n[ ERROR ON SERVER ]\n")
        pass

bot_worker.join()
con.close()
s.close()
