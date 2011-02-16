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


# twisted imports
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log

# system imports
import time, sys, re

class MessageLogger:
    """
    An independent logger class (because separation of application
    and protocol logic is a good thing).
    """
    def __init__(self, file):
        self.file = file

    def log(self, message):
        """Write a message to the file."""
        timestamp = time.strftime("[%H:%M:%S]", time.localtime(time.time()))
        self.file.write('%s %s\n' % (timestamp, message))
        self.file.flush()

    def close(self):
        self.file.close()


class LogBot(irc.IRCClient):
    """An IRC bot."""

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


    # callbacks for events

    def signedOn(self):
        """Called when bot has succesfully signed on to server."""
        self.join(self.factory.channel)

    def joined(self, channel):
        """This will get called when the bot joins the channel."""
        self.logger.log("[I have joined %s]" % channel)

    def privmsg(self, user, channel, msg):
        """This will get called when the bot receives a message."""
        user = user.split('!', 1)[0]
        self.logger.log("<%s> %s" % (user, msg))
        
    def action(self, user, channel, msg):
        """This will get called when the bot sees someone do an action."""
        user = user.split('!', 1)[0]
        self.logger.log("* %s %s" % (user, msg))

    # irc callbacks

    def irc_NICK(self, prefix, params):
        """Called when an IRC user changes their nickname."""
        old_nick = prefix.split('!')[0]
        new_nick = params[0]
        self.logger.log("%s is now known as %s" % (old_nick, new_nick))


    # For fun, override the method that determines how a nickname is changed on
    # collisions. The default method appends an underscore.
    def alterCollidedNick(self, nickname):
        """
        Generate an altered version of a nickname that caused a collision in an
        effort to create an unused related name for subsequent registration.
        """
        return nickname + '^'



class LogBotFactory(protocol.ClientFactory):
    """A factory for LogBots.

    A new protocol instance will be created each time we connect to the server.
    """

    # the class of the protocol to build when new connection is made
    protocol = LogBot

    def __init__(self, channel, nickname, filename):
        self.channel = channel
        self.nickname = nickname
        self.filename = filename

    def clientConnectionLost(self, connector, reason):
        """If we get disconnected, reconnect to server."""
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "connection failed:", reason
        reactor.stop()



class CommandBot(LogBot):

    def privmsg(self, user, channel, msg):
        """This will get called when the bot receives a message."""
        user = user.split('!', 1)[0]

        direct_prefix = self.nickname + ":"
        if msg.startswith(direct_prefix):
            msg = msg[len(direct_prefix):].lstrip()

            self.handleDictionary(self.factory.directCommandDictionary(), user, channel, msg)
        else:
            self.handleDictionary(self.factory.globalCommandDictionary(), user, channel, msg)

    def handleDictionary(self, dictionary, user, channel, msg):
        for pattern, handler in dictionary.items():
            if re.match(pattern, msg):
                self.processActions(handler(user, channel, msg))        

    def processActions(self, actions):
        if isinstance(actions, list):
            for action in actions:
                self.processAction(action)
        else:
            self.processAction(actions)

    def processAction(self, action):
        target = action.get("target")
        if isinstance(action.get("message"), list):
            for message in action.get("message"):
                self.msg(action.get("target"), message)
        else:
            self.msg(action.get("target"), action.get("message"))



class CommandBotFactory(LogBotFactory):
    protocol = CommandBot

    def globalCommandDictionary(self):
        return {"help$": self.help}

    def directCommandDictionary(self):
        return {"help": self.help}

    def help(self, user, channel, input):
        message = ["Available commands:","  help - display this message"]
        return {"target": user, "message": message}



if __name__ == '__main__':
    host = "irc.freenode.net"
    port = 6667
    channel = "#zjs-testing"
    nickname = "zjs-bot"
    logfile = "/tmp/zjs-bot.log"

    log.startLogging(sys.stdout)
    
    f = CommandBotFactory(channel, nickname, logfile)

    reactor.connectTCP(host, port, f)

    reactor.run()
