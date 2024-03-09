import os
import subprocess
from platform import system

# Добавляем новые импорты
from commands.admin_commands import grant_admin_status, grant_agent_status
from project_management import admins

cwd = os.getcwd()

# Учитывая, что у вас есть папка ICADS, приспосабливаем путь к ней
path = os.path.join(cwd, 'ICADS')
runner = 'python3' if system() == 'Linux' else 'py'

def start_update():
    print('⏱ Начинаю процесс обновления...')
    check_status('сверить')
    
    # Сохраняем изменения и данные
    subprocess.run("git add .", shell=True, cwd=path)
    subprocess.run("git stash", shell=True, cwd=path)
    
    # Получаем изменения с GitHub
    subprocess.run("git fetch origin", shell=True, cwd=path)
    subprocess.run("git merge origin/master-beta", shell=True, cwd=path)
    
    # Применяем сохраненные изменения обратно
    subprocess.run("git stash pop", shell=True, cwd=path)
    print('код сверен, все хорошо')

    with open(os.path.join(path, "updater.py"), 'w', encoding="utf-8") as data:
        data.write(get_updater())
    out = subprocess.run(f"{runner} {path}/updater.py", shell=True, cwd=path, capture_output=True)
    with open(os.path.join(os.getcwd(), "update.log"), 'w', encoding="utf-8") as data:
        data.write(str(out))

def check_status(message):
    print(f'сверяю код и вношу изменения ({message})')

def get_updater():
    return """
import os
import requests
import subprocess

# Добавленные функции и команды
from commands.admin_commands import show_admins

def edit(text):
    requests.post(f'https://api.vk.com/method/messages.edit?v=5.100&lang=ru&access_token='+'%s',
                  data = {'message_id': %s, 'message': text, 'peer_id': %s})

commands = [
    'git fetch --all',
    'git reset --hard origin/master-beta'
]

fail = False
for cmd in commands:
    if subprocess.run(cmd, shell=True).returncode != 0:
        fail = True

if fail:
    edit('❌ Помянем (скинь update.log из рабочей директории)')
else:
    edit('')
"""

if __name__ == "__main__":
    start_update()
