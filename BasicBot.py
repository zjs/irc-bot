from twisted.words.protocols import irc

import time

from MessageLogger import MessageLogger

class BasicBot(irc.IRCClient):
    """A basic IRC bot.

    Simply connects to the channel specified by its factory using the nick
    specified by the factory, logging connection information to the file
    specified by the factory.
    """

    def connectionMade(self):
        irc.IRCClient.connectionMade(self)
        self.setNick(self.factory.nickname)
        self.logger = MessageLogger(open(self.factory.filename, "a"))
        self.logger.log("[connected at %s]" % 
                        time.asctime(time.localtime(time.time())))

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)
        self.logger.log("[disconnected at %s]" % 
                        time.asctime(time.localtime(time.time())))
        self.logger.close()

    def signedOn(self):
        self.join(self.factory.channel)

