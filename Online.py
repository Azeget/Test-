from duty.objects import dp, MySignalEvent
from duty.api_utils import set_online_privacy

@dp.longpoll_event_register('+вечныйонлайн')
@dp.my_signal_event_register('+вечныйонлайн')
def set_eternal_online(event: MySignalEvent):
    result = set_online_privacy(event.db, 'all')
    if 'response' in result and 'category' in result['response'] and result['response']['category'] == 'all':
        msg = '🌟 Вечный онлайн активирован'
    else:
        msg = '🦊 Произошла ошибка'
    event.msg_op(2, msg)
    return "ok"

@dp.longpoll_event_register('-вечныйонлайн')
@dp.my_signal_event_register('-вечныйонлайн')
def unset_eternal_online(event: MySignalEvent):
    result = set_online_privacy(event.db, 'none')
    if 'response' in result and 'category' in result['response'] and result['response']['category'] == 'none':
        msg = '🙁 Вечный онлайн деактивирован'
    else:
        msg = '🦊 Произошла ошибка'
    event.msg_op(2, msg)
    return "ok"
