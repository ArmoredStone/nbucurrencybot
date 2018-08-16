import os
from time import sleep
if os.popen("pip list").read().find("pyTelegramBotAPI") != -1:
    pass
else:
    os.popen("pip install pyTelegramBotAPI")
    sleep(10)
