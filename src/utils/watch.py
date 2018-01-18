import time

from utils.logging import logging

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


class MyHandler(PatternMatchingEventHandler):
    def __init__(self, fun):
        super().__init__(ignore_directories=True)
        self.fun = fun

    def process(self, event):
        logging.info('Watching event: %s : %s',
                     event.src_path, event.event_type)
        if self.fun is not None:
            self.fun()

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)


class Watcher(object):
    fun = None
    __observers = []

    def set_fun(self, fun):
        self.fun = fun

    def add_watch(self, dir):
        if self.fun is not None:
            logging.info('Adding watcher for : %s', dir)
            observer = Observer()
            observer.schedule(MyHandler(self.fun), path=dir, recursive=True)
            self.__observers.append(observer)

    def start(self):
        for observer in self.__observers:
            observer.start()

        # noinspection PyBroadException
        try:
            while True:
                time.sleep(1)
        except Exception:
            for observer in self.__observers:
                observer.stop()
        for observer in self.__observers:
            observer.join()


watcher = Watcher()
