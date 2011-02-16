from CommandHandlerFactory import CommandHandlerFactory
from ExampleCommandHandler import ExampleCommandHandler

class ExampleCommandHandlerFactory(CommandHandlerFactory):
    """A factory for instances of ExampleCommandHandler"""
    def __init__(self, nickname):
	self.commands = Commands()
	self.counter = Counter()
        self.nickname = nickname

    def create(self, callback):
	return ExampleCommandHandler(callback, self.nickname, {"help$": self.commands.help, "next$": self.counter.incrementAndPrint},  {"help": self.commands.help},)

class Commands:
    """A container class for commands used by ExampleCommandHandlerFactory"""

    def help(self, user, channel, input):
        message = ["Available commands:","  help - display this message"]
        return {"target": user, "message": message}


class Counter:
    def __init__(self):
        self.counter = 0

    def incrementAndPrint(self, user, channel, input):
        self.counter = self.counter + 1
        message = "Count is now %d" % self.counter
        return [{"target": channel, "message": message}, {"target": user, "message": "You've incremented the counter"}]

