import time

from utils.logging import logging

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


def watch(config_dir, fun):
    class MyHandler(PatternMatchingEventHandler):
        def __init__(self, fun):
            super().__init__(ignore_directories=True)
            self.fun = fun

        def process(self, event):
            logging.info('Watching event: %s : %s', event.src_path, event.event_type)
            self.fun()

        def on_modified(self, event):
            self.process(event)

        def on_created(self, event):
            self.process(event)

    observer = Observer()
    observer.schedule(MyHandler(fun), path=config_dir, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except Exception:
        observer.stop()

    observer.join()
