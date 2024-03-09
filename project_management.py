

from duty.objects import dp, MySignalEvent

admins = ['Разработчик', 'Администратор']  # Список статусов администраторов

@dp.longpoll_event_register('+адм')
def grant_admin_status(event: MySignalEvent):
    user_status = event.db.get('status', None)
    
    if user_status == 'Разработчик' or user_status == 'Администратор':
        event.msg_op(2, 'Статус админа выдан')
        return "ok"
    else:
        event.msg_op(2, 'Недостаточно прав для выдачи статуса')
        return "error"

@dp.longpoll_event_register('+аг')
def grant_agent_status(event: MySignalEvent):
    user_status = event.db.get('status', None)
    
    if user_status == 'Разработчик' or user_status == 'Администратор':
        event.msg_op(2, 'Статус агента выдан')
        return "ok"
    else:
        event.msg_op(2, 'Недостаточно прав для выдачи статуса')
        return "error"
