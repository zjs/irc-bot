from BasicBotFactory import BasicBotFactory
from CommandBot import CommandBot

class CommandBotFactory(BasicBotFactory):
    """A basic factory for CommandBots.

    Simply creates CommandBots.
    """

    protocol = CommandBot

    def __init__(self, channel, nickname, filename, commandHandlerFactory):
        """
        Keyword arguments:
        channel -- The channel the bot should try to join.
        nickname -- The nickname the bot should try to use.
        filename -- The file to use for logging.
        commandHandlerFactory -- The factory to use to generate CommandHandlers
        """
	BasicBotFactory.__init__(self, channel, nickname, filename)
	self.commandHandlerFactory = commandHandlerFactory

