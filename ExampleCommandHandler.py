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
        self._callback = callback
        self._direct_prefix = nickname + ":"
        self._globalCommandDictionary = globalCommandDictionary
        self._directCommandDictionary = directCommandDictionary

    def handle(self, username, channel, message):
        """This method will be called on each message received.

        Keyword arguments:
        username -- The username of the user sending the message.
        channel -- The channel that the message was sent in.
        message -- The message which was received.
        """
        if message.startswith(self._direct_prefix):
            message = message[len(self._direct_prefix):].lstrip()

            self._handleDictionary(self._directCommandDictionary, username, channel, message)
        else:
            self._handleDictionary(self._globalCommandDictionary, username, channel, message)

    def _handleDictionary(self, dictionary, username, channel, message):
        for pattern, handler in dictionary.items():
            if re.match(pattern, message):
                self._processActions(handler(username, channel, message))        

    def _processActions(self, actions):
        if isinstance(actions, list):
            for action in actions:
                self._processAction(action)
        else:
            self._processAction(actions)

    def _processAction(self, action):
        target = action.get("target")
        if isinstance(action.get("message"), list):
            for message in action.get("message"):
                self._callback(action.get("target"), message)
        else:
            self._callback(action.get("target"), action.get("message"))



