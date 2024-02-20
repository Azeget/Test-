from duty.objects import LongpollEvent, db, dp
from microvk import VkApi
from duty.utils import gen_secret
from logger import get_writer
from .app import app
from flask import request
import traceback
import json
import json,os,requests,time,asyncio
from threading import Thread
logger = get_writer('Приемник сигналов LP модуля')

def lp_create_handler():
    while not db.lp_settings['key']:
        time.sleep(3)
        continue;
    try:
        import vk_api
        from vk_api.longpoll import VkLongPoll, VkEventType
    except:
        try:
            import subprocess,sys
            try:subprocess.check_call([sys.executable, "-m", "pip", "install", "vk-api"])
            except:''
            try:subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "vk-api"])
            except:''
            import vk_api
            from vk_api.longpoll import VkLongPoll, VkEventType
        except:
            os.system('pip3.8 install --user vk-api')
            try:
                import vk_api
                from vk_api.longpoll import VkLongPoll, VkEventType
            except:
                logger('не удалось установить модуль vk-api, лп не может быть запущен!')
                return;
    vk_session = vk_api.VkApi(token=db.access_token)
    api = vk_session.get_api()
    while True:
        try:
            if not not db.lp_settings.get('key'): break;
            longpoll = VkLongPoll(vk_session)
            for event_ in longpoll.listen():
                if not not db.lp_settings.get('key'): break;
                if event_.type == VkEventType.MESSAGE_NEW:
                    try:
                        message = api.messages.getById(message_ids=event_.message_id)['items'][0]
                        if message['from_id'] in db.lp_settings['ignored_users']:
                            try: time.sleep(0.2); api.messages.delete(message_ids=message['id']);
                            except: 'обработка ошибки удаления игнора';
                        ok = False
                        for x in db.lp_settings['prefixes']:
                            if x+' ' == message['text'][len(x)+1:].lower(): message['text'] = message['text'][len(x)+1:]; ok = True; break;
                        if not ok: continue;
                        event_one = LongpollEvent({
                            'access_key': '',
                            'message': message,
                            'chat': None
                        })
                        d = dp.longpoll_event_run(event_one)
                        db.sync()
                    except: 'Ошибка, бывает';
        except Exception as e: print(e); time.sleep(2);
Thread(target=lp_create_handler).start()
@app.route('/ping', methods=["POST"])
def ping():
    return "ok"
@app.route('/longpoll/event', methods=["POST"])
def longpoll():
    event = LongpollEvent(request.json)
    if event.data['access_key'] != event.db.lp_settings['key']:
        return "?"
    d = dp.longpoll_event_run(event)
    db.sync()
    if type(d) == dict:
        return json.dumps(d, ensure_ascii=False)
    return json.dumps({"response": "ok"}, ensure_ascii=False)
class error:
    AuthFail = 0
@app.route('/longpoll/start', methods=["POST"])
def get_data():
    token = json.loads(request.data)['token']
    try:
        if VkApi(token)('users.get')[0]['id'] != db.owner_id:
            raise ValueError
    except (KeyError, IndexError, ValueError):
        return json.dumps({'error': error.AuthFail})
    db.lp_settings['key'] = gen_secret(length=20)
    db.sync()
    return json.dumps({
            'chats': db.chats,
            'deleter': db.responses['del_self'],
            'settings': db.lp_settings,
            'self_id': db.owner_id
        })
@app.route('/longpoll/sync', methods=["POST"])
def sync_settings():
    data = request.json
    if data['access_key'] != db.lp_settings['key']:
        return "?"
    db.lp_settings.update(data['settings'])
    db.sync()
    return "ok"