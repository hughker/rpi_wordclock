
import threading
from monotonic import monotonic as _time

class event_handler:
    EVENT_INVALID = -1

    EVENT_BUTTON_LEFT = 0
    EVENT_BUTTON_RIGHT = 1
    EVENT_BUTTON_RETURN = 2
    EVENT_EXIT_PLUGIN = 3

    def __init__(self):
        self.condition = threading.Condition()
        self.event = self.EVENT_INVALID
        self.lock_time = 0.1

    def waitForEvent(self, seconds = None):
        self.condition.acquire()
        self.__wait_for(lambda: self.event != self.EVENT_INVALID, seconds)
        evt = self.event
        self.event = self.EVENT_INVALID
        self.condition.release()
        return evt

    def setEvent(self, evt):
        self.condition.acquire()
        if self.event != self.EVENT_EXIT_PLUGIN:
            self.event = evt
        self.condition.notifyAll()
        self.condition.release()

    def waitForExit(self, seconds = None):
        self.condition.acquire()
        self.__wait_for(lambda: self.event == self.EVENT_EXIT_PLUGIN, seconds)
        self.event = self.EVENT_INVALID
        self.condition.release()

    def __wait_for(self, predicate, timeout=None):
        """Wait until a condition evaluates to True.

        predicate should be a callable which result will be interpreted as a
        boolean value.  A timeout may be provided giving the maximum time to
        wait.
        """
        endtime = None
        waittime = timeout
        result = predicate()
        while not result:
            if waittime is not None:
                if endtime is None:
                    endtime = _time() + waittime
                else:
                    waittime = endtime - _time()
                    if waittime <= 0:
                        break
            self.condition.wait(waittime)
            result = predicate()
        return result

