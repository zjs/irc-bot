from CommandHandlerFactory import CommandHandlerFactory
from ExampleCommandHandler import ExampleCommandHandler

class ExampleCommandHandlerFactory(CommandHandlerFactory):
    """A factory for instances of ExampleCommandHandler"""
    def __init__(self, nickname):
	self.commands = Commands()
        self.nickname = nickname

    def create(self, callback):
	return ExampleCommandHandler(callback, self.nickname, {"help$": self.commands.help},  {"help": self.commands.help},)

class Commands:
    """A container class for commands used by ExampleCommandHandlerFactory"""
    def help(self, user, channel, input):
        message = ["Available commands:","  help - display this message"]
        return {"target": user, "message": message}
