from duty.objects import dp, MySignalEvent

@dp.my_signal_event_register('нз')
def change_nickname(event: MySignalEvent) -> str:
    user_id = event.obj.from_id  
    new_nickname = event.payload.args

    if new_nickname:
        vk = event.api.get_pure_api()
        try:
            vk.account.saveProfileInfo(screen_name=new_nickname)
            return "ок"
        except Exception as e:
            return f"Ошибка при изменении ника: {e}"
    else:
        return "Новый ник не указан"
