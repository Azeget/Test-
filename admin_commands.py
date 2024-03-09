

from duty.objects import dp, MySignalEvent

@dp.longpoll_event_register('админы')
def show_admins(event: MySignalEvent):
    admins_list = [user for user in event.db if user.get('status') in admins]
    
    if admins_list:
        message = 'Список администраторов:\n'
        message += '\n'.join([f"{user['first_name']} {user['last_name']}" for user in admins_list])
    else:
        message = 'Нет администраторов'
    
    event.msg_op(2, message)
    return "ok"
