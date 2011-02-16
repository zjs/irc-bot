from BasicBotFactory import BasicBotFactory
from CommandBot import CommandBot

class CommandBotFactory(BasicBotFactory):
    protocol = CommandBot

    def __init__(self, channel, nickname, filename, commandHandler):
	BasicBotFactory.__init__(self, channel, nickname, filename)
	self.commandHandler = commandHandler

