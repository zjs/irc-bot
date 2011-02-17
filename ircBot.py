"""
Example invocation for IRC Bot

To customize commands, simply create a subclass of CommandHandlerFactory.
ExampleCommandHandlerFactory is an example of such a subclass.

To customize types of commands, create a subclass of CommandHandler as well.
ExampleCommandHandler is an example of such a subclass.
"""

from twisted.internet import reactor
from twisted.python import log

import sys

from CommandBotFactory import CommandBotFactory
from ExampleCommandHandlerFactory import ExampleCommandHandlerFactory

if __name__ == '__main__':
    host = "irc.freenode.net"
    port = 6667
    channel = "#zjs-testing"
    nickname = "zjs-bot"
    logfile = "/tmp/zjs-bot.log"

    log.startLogging(sys.stdout)
    
    f = CommandBotFactory(channel, nickname, logfile, ExampleCommandHandlerFactory(nickname, channel))

    reactor.connectTCP(host, port, f)

    reactor.run()
