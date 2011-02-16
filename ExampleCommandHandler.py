import re

from CommandHandler import CommandHandler

class ExampleCommandHandler(CommandHandler):
    def __init__(self, callback, nickname, globalCommandDictionary, directCommandDictionary):
        """This method should store the callback and nickname as neccessary.

        Keyword arguments:
        callback -- A function which takes a target (such as a user or channel)
                    and a message. It is expected that this method will send
                    the supplied message to the supplied target.
        nickname -- The current nickname of the bot. This is necessary to be able
                    to distinguish between general messages and direct messages.
        globalCommandDictionary -- A dictionary mapping regular expression strings
                                   to functions. A function will be called iff
                                   the regular expression evaluates to true on
                                   any message received by the bot.
        directCommandDictionary -- A dictionary mapping regular expression strings
                                   to functions. A function will be called iff
                                   the regular expression evaluates to true on
                                   any message sent directly to the bot.
        """
        self.callback = callback
        self.direct_prefix = nickname + ":"
        self.globalCommandDictionary = globalCommandDictionary
        self.directCommandDictionary = directCommandDictionary

    def handle(self, username, channel, message):
        """This method will be called on each message received.

        Keyword arguments:
        username -- The username of the user sending the message.
        channel -- The channel that the message was sent in.
        message -- The message which was received.
        """
        if message.startswith(self.direct_prefix):
            message = message[len(self.direct_prefix):].lstrip()

            self.handleDictionary(self.directCommandDictionary, username, channel, message)
        else:
            self.handleDictionary(self.globalCommandDictionary, username, channel, message)

    def handleDictionary(self, dictionary, username, channel, message):
        for pattern, handler in dictionary.items():
            if re.match(pattern, message):
                self.processActions(handler(username, channel, message))        

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
                self.callback(action.get("target"), message)
        else:
            self.callback(action.get("target"), action.get("message"))



