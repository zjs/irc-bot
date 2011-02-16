from twisted.internet import reactor, protocol

from BasicBot import BasicBot

class BasicBotFactory(protocol.ClientFactory):
    """A basic factory for basic IRC bots.

    Simply creates basic IRC bots, specifying channel, nickname, and filename.

    If the connection is lost, a new bot is created.

    Is a connection fails, the factory aborts. No retries are attempted.
    """

    protocol = BasicBot

    def __init__(self, channel, nickname, filename):
        """
        Keyword arguments:
        channel -- The channel the bot should try to join.
        nickname -- The nickname the bot should try to use.
        filename -- The file to use for logging.
        """
        self.channel = channel
        self.nickname = nickname
        self.filename = filename

    def clientConnectionLost(self, connector, reason):
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "connection failed:", reason
        reactor.stop()
