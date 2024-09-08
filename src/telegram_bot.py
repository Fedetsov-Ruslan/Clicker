from notifiers import get_notifier


token = ''
chat_id_list = []
with open('id_list.txt','r') as file:
    chat_id_list = file.readlines()
chat_id_list = [id_str.split('#')[0].strip() for id_str in chat_id_list if id_str.split('#')[0].strip()]
token = chat_id_list[0].split(' ')[1]
del chat_id_list[0]

# '746828525'#-мой id       #'5093303797'-id заказчика
name_computer = ''
telegram = get_notifier('telegram')

def send_massage_print(message, is_print = True):
    for id in chat_id_list:
        telegram.notify(token=token, chat_id=id, message=name_computer + ' : ' + message)
        if is_print:
            print(name_computer + ' : ' + message)

