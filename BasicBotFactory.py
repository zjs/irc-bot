from twisted.internet import reactor, protocol

from BasicBot import BasicBot

class BasicBotFactory(protocol.ClientFactory):
    protocol = BasicBot

    def __init__(self, channel, nickname, filename):
        self.channel = channel
        self.nickname = nickname
        self.filename = filename

    def clientConnectionLost(self, connector, reason):
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "connection failed:", reason
        reactor.stop()
