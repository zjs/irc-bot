# Copyright (c) 2001-2009 Twisted Matrix Laboratories.
# See LICENSE for details.


"""
An example IRC log bot - logs a channel's events to a file.

If someone says the bot's name in the channel followed by a ':',
e.g.

  <foo> logbot: hello!

the bot will reply:

  <logbot> foo: I am a log bot

Run this script with two arguments, the channel name the bot should
connect to, and file to log to, e.g.:

  $ python ircLogBot.py test test.log

will log channel #test to the file 'test.log'.
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
    
    f = CommandBotFactory(channel, nickname, logfile, ExampleCommandHandlerFactory(nickname))

    reactor.connectTCP(host, port, f)

    reactor.run()
