import threading
import time

from container import container, Container


def thread_1(user):                
    while True:
        user.x += 1
        print(user.x)
        time.sleep(2)


user_service1 = container.user_service_provider()

T = threading.Thread(target=thread_1, args=[user_service1])
T.daemon = True

T.start()     

time.sleep(1)

import main