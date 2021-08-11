"""
util.py

Contains helper functions and classes
primarily used by project.py



"""


__all__ = [
    'Util', 'Timer'
]

import time


class Util:
    """
    Wrapper between runtime and project.py
    Contains useful objects and functions to
    interface with project.py where needed.

    timer - Handles the Timer
    inputs - Handles keyboard/mouse input
    sprites - Provides sprite lookup and stage

    display - Used to get display info
    events - Used to send events to sprites
    runtime - The current Runtime instance
    """

    def __init__(self, runtime):
        self.timer = Timer()
        self.inputs = runtime.inputs
        self.sprites = runtime.sprites
        self.display = runtime.display
        self.events = runtime.events
        self.runtime = runtime

    def send_event(self, event, restart=False):
        """Send an event"""
        self.events.send(self, self.sprites, event, restart)

    async def send_wait(self, event, restart=False):
        """Send an event"""
        await self.events.send_wait(self, self.sprites, event, restart)

    def send_broadcast(self, event):
        """Sends a broadcast"""
        return self.events.broadcast(self, self.sprites, event)

    async def send_broadcast_wait(self, event):
        """Sends a broadcast"""
        await self.events.broadcast_wait(self, self.sprites, event)

    def stop_all(self):
        """Ends execution of the main loop"""
        print("Stop")
        self.runtime.running = False


class Timer:
    """
    Handles a timer using time.monotonic

    TODO Make timer like a property with __get__
    """

    def __init__(self):
        self._timer = time.monotonic()

    def __call__(self):
        return time.monotonic() - self._timer

    def reset(self):
        """Reset the timer"""
        self._timer = time.monotonic()
