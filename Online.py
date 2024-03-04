from duty.objects import dp, MySignalEvent
from duty.api_utils import set_online_privacy

@dp.longpoll_event_register('+онлайн')
@dp.my_signal_event_register('+онлайн')
def set_eternal_online(event: MySignalEvent):
    if set_online_privacy(event.db, 'all'):  # Устанавливаем вечный онлайн статус
        msg = '🌟 Вечный онлайн активирован'
    else:
        msg = '🦊 Произошла ошибка'
    event.msg_op(2, msg)
    return "ok"

@dp.longpoll_event_register('-онлайн')
@dp.my_signal_event_register('-онлайн')
def unset_eternal_online(event: MySignalEvent):
    if set_online_privacy(event.db, 'none'):  # Отключаем вечный онлайн статус
        msg = '🙁 Вечный онлайн деактивирован'
    else:
        msg = '🦊 Произошла ошибка'
    event.msg_op(2, msg)
    return "ok"
