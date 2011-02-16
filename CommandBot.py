from BasicBot import BasicBot

class CommandBot(BasicBot):
    """An IRC bot which listens for and responds to commands.

    Handles commands using instances of a subclass of CommandHandler created by
    an instace of a subclass of CommandHandlerFactory as specified by the bot's
    factory.
    """

    def privmsg(self, user, channel, message):
        """This method will be called on each message received.

	Keyword arguments:
	user -- The user sending the message (username!ident@hostmask).
        channel -- The channel that the message was sent in.
        message -- The message which was received.
	"""
        user = user.split('!', 1)[0]

        commandHandler = self.factory.commandHandlerFactory.create(self.msg)
        commandHandler.handle(user, channel, message)

