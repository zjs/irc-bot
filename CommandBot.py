from BasicBot import BasicBot

class CommandBot(BasicBot):

    def privmsg(self, user, channel, message):
        """This will get called when the bot receives a message."""
        user = user.split('!', 1)[0]

        commandHandler = self.factory.commandHandler(self.msg, self.nickname)
        commandHandler.handle(user, channel, message)

