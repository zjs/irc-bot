class CommandHandlerFactory:
    """A class defining the command handling interface.

    A CommandHandlerFactory implementing this interface must be provided to a
    CommandBotFactory.
    """

    def create(self, callback):
        """This method must return a CommandHandler

        Keyword arguments:
        callback -- A function which takes a target (such as a user or channel)
                    and a message. It is expected that this method will send
                    the supplied message to the supplied target.
        """
	pass
