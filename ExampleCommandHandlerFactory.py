from twisted.internet import task

from CommandHandlerFactory import CommandHandlerFactory
from ExampleCommandHandler import ExampleCommandHandler

class ExampleCommandHandlerFactory(CommandHandlerFactory):
    """A factory for instances of ExampleCommandHandler"""
    def __init__(self, nickname, channel):
	self.commands = Commands()
        self.nickname = nickname
        self.channel = channel
        self.status = None

    def create(self, callback):
	if self.status is None:
            self.status = StatusChecker(callback, self.channel)

	return ExampleCommandHandler(callback, self.nickname, {"help$": self.commands.help},  {"help": self.commands.help, "start": self.status.start, "stop": self.status.stop},)

class Commands:
    """A container class for commands used by ExampleCommandHandlerFactory"""
    def help(self, user, channel, input):
        message = ["Available commands:","  help - display this message"]
        return {"target": user, "message": message}

class StatusChecker:
    def __init__(self, callback, channel):
        self.callback = callback
        self.channel = channel
        self.loopingCall = task.LoopingCall(self.check)
        self.started = None
        self.user = None
        self.lastStatus = None

    def start(self, user, channel, input):
        print "Starting"
        if self.started:
            return {"target": user, "message": "Error: Task already started by %s" % self.user}
        else:
            self.loopingCall.start(1.0)
            self.started = True
            self.user = user
            return {"target": user, "message": "Task scheduled"}

    def stop(self, user, channel, input):
        print "Stopping"
        if self.started is None:
            return {"target": user, "message": "Error: Task has not ever been run"}            
        elif not self.started:
            return {"target": user, "message": "Error: Task already stopped by %s" % self.user}
        else:
            self.loopingCall.stop()
            self.started = False
            self.user = user
            return {"target": user, "message": "Task stopped"}

    def check(self):
        newStatus = self._check()
        if not newStatus == self.lastStatus:
            self.callback(self.channel, "Status changed from %s to %s" % (self.lastStatus, newStatus))
            self.lastStatus = newStatus

    def _check(self):
        return "Changeme"

        
