import random
import threading
import time

from ogame import OGame
import buildings


class Credentials:
    def __init__(self, universe, username, password):
        self.universe = universe
        self.username = username
        self.password = password


running = True
bot_queue: list[Credentials] = []


def bot(creds: Credentials):
    empire = OGame(creds.universe, creds.username, creds.password)
    ids = empire.planet_ids()
    for ID in ids:
        for order in buildings.queue(ID, empire):
            print(order.condition, order.build)
            if order.condition:
                empire.build(
                    what=order.build,
                    id=ID
                )
                break
    del empire


def scheduler():
    print('Starting up Barakis Scheduler')
    while running:
        for creds in bot_queue:
            try:
                bot(creds)
            except Exception as e:
                print(e)
            time.sleep(random.randint(20, 120))


thread = threading.Thread(target=scheduler)


def add(uni, username, password) -> bool:
    if active(uni, username):
        return False
    bot_queue.append(
        Credentials(
            uni,
            username,
            password
        )
    )
    return True


def remove(universe, username) -> bool:
    for i, creds in enumerate(bot_queue):
        if creds.universe == universe and creds.username == username:
            del bot_queue[i]
            return True
    return False


def stop() -> bool:
    global bot_queue
    bot_queue = []
    return True


def active(universe, username) -> bool:
    for i, creds in enumerate(bot_queue):
        if creds.universe == universe and creds.username == username:
            return True
    return False
