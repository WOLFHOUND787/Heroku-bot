import vk_api, json
from vk_api import VkUpload             #PHOTO
from vk_api.longpoll import VkLongPoll, VkEventType

token = 'e80c77b8275cdba34be0c72b99359fe486b453d35d90bb3db4423a945c75c55d2899dfb01ed21de3986be'  #Маме о главном
# token = 'cde38555e51d8d7c8fedfa1bd34520a253781adae25fd9e2314e121cb2e1cc0252a6350f2e684e838c926'   #Тест бот


vk_session = vk_api.VkApi(token = token)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)
upload = VkUpload(vk_session)           #PHOTO

class User():

    def __init__(self, id, mode, cash):
        self.id = id
        self.mode = mode


def get_keyboard(buts):
    nb = []
    color = ''
    for i in range(len(buts)):
        nb.append([])
        for k in range(len(buts[i])):
            nb[i].append(None)
            #print(nb[i])
            #print(len(nb))
    for i in range(len(buts)):
        for k in range(len(buts[i])):
            text = buts[i][k][0]
            #print(text)
            # print(list(buts[1][0]))
            #print([main_list[buts] for buts in indexes])
            color = {'зеленый' : 'positive', 'красный' : 'negative', 'синий' : 'primary', 'белый' : 'secondary'}[buts[i][k][1]]
            nb[i][k] = {"action" : {"type": "text", "payload": "{\"button\": \"" + "1" + "\"}", "label": f"{text}"}, "color": f"{color}"}
            #print(list(buts[2]))
    first_keyboard = {'one_time': False, 'buttons': nb}
    first_keyboard = json.dumps(first_keyboard, ensure_ascii=False).encode('utf-8')
    first_keyboard = str(first_keyboard.decode('utf-8'))
    #print(nb[i][k])
    #print(first_keyboard)
    # ak = len(list(buts[0][0]))
    # print(ak)

    # print(list(nb[0]))

    return first_keyboard

#print(nb[i][k][1])
start_key = get_keyboard([
    [('Да, я знаю о раке молочной железы', 'зеленый')],
    [('Хочу узнать', 'синий')]
])


yes_key = get_keyboard([
    [('Как провести самообследование', 'синий')],
    [('Как проходит профилактический осмотр', 'синий')],
    [('Где можно пройти обследование груди', 'синий')],
    [('Вернуться', 'красный')]
])


no_key = get_keyboard([
    [('Рак молочной железы', 'синий')],
    [('Факторы риска', 'синий')],
    [('Возможные признаки', 'синий')],
    [('Вернуться', 'красный')]
])


def sender(id, text, key):
    vk_session.method('messages.send', {'user_id' : id, 'message' : text, 'random_id' : 0, 'keyboard': key})   #'attachment': ','.join(attachments)

def send_photo(id, text, key, attachment):
    vk_session.method('messages.send', {'user_id' : id, 'message' : text, 'random_id' : 0, 'keyboard': key, 'attachment': ','.join(attachments)})   #'attachment': ','.join(attachments)

image1 = "multfilm.jpg"         #PHOTO


users = []
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:

            id = event.user_id
            msg = event.text.lower()
            attachments = []            #PHOTO
            upload_image = upload.photo_messages(photos=image1)[0]          #PHOTO
            attachments.append('photo{}_{}'.format(upload_image['owner_id'], upload_image['id']))           #PHOTO
            if msg == 'начать':
                flag1 = 0
                for user in users:
                    if user.id == id:
                        sender(id, 'Знаете ли вы о раке молочной железы?', start_key)
                        #sender(id, 'Выберите действие', start_key)
                        user.mode = 'start'
                        flag1 = 1
                if flag1 == 0:
                    users.append(User(id, 'start', 0))
                    sender(id, 'Знаете ли вы о раке молочной железы?', start_key)
                    #sender(id, 'Выберите действие:', start_key)

            for user in users:
                if user.id == id:

                    if user.mode == 'start':

                        if msg == 'да, я знаю о раке молочной железы':
                            sender(id, 'Хотите ли вы узнать?', yes_key)
                            user.mode = 'yes'

                        if msg == 'хочу узнать':
                            sender(id, 'Какую информацию о раке молочной железы Вы хотели бы узнать?', no_key)
                            user.mode = 'no'


                    if user.mode == 'yes':
                        yes1_key = yes_key
                        if msg == 'как провести самообследование':
                            sender(id, 'Информация о том, как проводить самообследование....', yes1_key)



                        if msg == 'как проходит профилактический осмотр':
                            sender(id, 'Информация о том, как проходит профилактический осмотр....', yes1_key)


                        if msg == 'где можно пройти обследование груди':
                            send_photo(id, 'Информация о том, где можно пройти обследование груди....', yes1_key, ','.join(attachments))


                        if msg == 'вернуться':
                            sender(id, 'Знаете ли вы о раке молочной железы?', start_key)
                            user.mode = 'start'


                    if user.mode == 'no':

                        if msg == 'рак молочной железы':
                            sender(id, 'Информация о раке молочной железы', no_key)



                        if msg == 'факторы риска':
                            sender(id, 'Факторы риска', no_key)


                        if msg == 'возможные признаки':
                            sender(id, 'Возможные признаки', no_key)


                        if msg == 'вернуться':
                            sender(id, 'Знаете ли вы о раке молочной железы?', start_key)
                            user.mode = 'start'
