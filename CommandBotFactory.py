from BasicBotFactory import BasicBotFactory
from CommandBot import CommandBot

class CommandBotFactory(BasicBotFactory):
    protocol = CommandBot

    def __init__(self, channel, nickname, filename, commandHandlerFactory):
	BasicBotFactory.__init__(self, channel, nickname, filename)
	self.commandHandlerFactory = commandHandlerFactory

