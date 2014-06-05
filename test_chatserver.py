"""
Functional tests for chatserver refactor.

Run it with trial, with the order=toptobottom option::

    trial --order=toptobottom test_chatserver

Assumes chatserver is running on localhost, port 6667. To specify the
name of the chatserver module at runtime::

    python -c 'import sys; __import__(sys.argv[1][:-3]).main(6667)' \
        chatservers/custom.py

"""
import re
from collections import namedtuple

from twisted.internet import reactor, defer
from twisted.internet.protocol import Factory
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.protocols.basic import LineReceiver
from twisted.trial.unittest import TestCase
from twisted.python import log


# Example session

# *** Hello! What is your nickname?
# cdunklau
# *** Type "/help" for help.
# *** cdunklau has joined.
# Hi there!
# <cdunklau> Hi there!
# /help
# *** Available commands:
# ***  /help -- get help
# ***  /quit -- disconnect
# ***  /me -- perform an action
# ***  /who -- list connected users
# ***  /nick -- change your nickname to something better
# /me waves
# * cdunklau waves
# /who
# *** Currently connected: cdunklau
# /nick colin
# *** cdunklau is now known as colin.
# /nick cdunklau
# *** colin is now known as cdunklau.
# /bogus
# *** No such command: /bogus
# /quit
# *** cdunklau has left.
# Connection closed by foreign host.


CHAT_LINE_REGEX = re.compile(r'<([a-z0-9_]+)> (.*)$', re.I)
MESSAGE_LINE_REGEX = re.compile(r'\*\*\* (.*)$')
ACTION_LINE_REGEX = re.compile(r'\* ([a-z0-9_]+) (.*)$', re.I)

NICK_CHANGED_REGEX = re.compile(
    r'([a-z0-9_]+) is now known as ([a-z0-9_]+).',
    re.I
)


class ChatserverTestCase(TestCase):
    def deferExpectedMessages(self, messages, timeout=0.5):
        """
        Connect a StateMachineClient to the chat server on localhost,
        port 6667, and allow it to run for up to ``timeout`` seconds.

        ``messages`` is a list of ``Tx`` or ``Rx`` instances
        representing the messages to send and the messages expected
        from the server, in order.

        """
        endpoint = TCP4ClientEndpoint(reactor, 'localhost', 6667)
        d = endpoint.connect(SimpleFactory(StateMachineClient, messages, self))

        # This part gets a little hairy. In order to shut down the protocol's
        # connection, reactor.callLater needs to access the protocol, so I
        # have to do it in a callback. Then I also need to access the
        # delayed call object, so I need to set up a callback inside another
        # applied to the same Deferred.
        # This Deferred will fire when the client successfully connects to
        # the server, so the timeout will begin from that point.
        @d.addCallback
        def cbSetTimeout(proto):
            delayed = reactor.callLater(
                timeout,
                proto.transport.loseConnection
            )

            # I need to make sure the delayed timeout call gets cancelled
            # so it doesn't call loseConnection twice (it might be called from
            # within the protocol).
            @d.addBoth
            def cbCancelTimeout(passthrough):
                delayed.cancel()
                return passthrough

            # Returning the protocol's Deferred from this callback implicitly
            # "chains" it onto the deferred from endpoint.connect...
            return proto.deferred

        # ...so I can return the Deferred from endpoint.connect directly, and
        # trial will wait until it fires to record success or failure.
        return d

    def test_login_and_quit(self):
        messages = sessionMessages('logintest', [])
        return self.deferExpectedMessages(messages)

    def test_chat(self):
        messages = sessionMessages(
            'chattest',
            [Tx('Hello there!'), Rx('<chattest> Hello there!')]
        )
        return self.deferExpectedMessages(messages)

    def test_help(self):
        messages = sessionMessages(
            'helptest',
            [
                Tx('/help'),
                Rx('*** Available commands:'),
                Rx('***  /help -- get help'),
                Rx('***  /quit -- disconnect'),
                Rx('***  /me -- perform an action'),
                Rx('***  /who -- list connected users'),
                Rx('***  /nick -- change your nickname to something better'),
            ]
        )
        return self.deferExpectedMessages(messages)

    def test_emote(self):
        messages = sessionMessages(
            'emotetest',
            [Tx('/me is a teapot'), Rx('* emotetest is a teapot')]
        )
        return self.deferExpectedMessages(messages)

    def test_simple_who(self):
        messages = sessionMessages(
            'whotest',
            [Tx('/who'), Rx('*** Currently connected: whotest')]
        )
        return self.deferExpectedMessages(messages)

    def test_nick(self):
        messages = sessionMessages(
            'nicktest',
            [
                Tx('/nick newnick'),
                Rx('*** nicktest is now known as newnick.'),
                Tx('do you like my new name?'),
                Rx('<newnick> do you like my new name?'),
            ],
            'newnick',
        )
        return self.deferExpectedMessages(messages)

    def test_bogus_command_error(self):
        messages = sessionMessages(
            'bogustest',
            [Tx('/bogus'), Rx('*** No such command: /bogus')]
        )
        return self.deferExpectedMessages(messages)

    def test_invalid_nick(self):
        messages = sessionMessages(
            'badnicktest',
            [Tx('/nick badnick#$%'), Rx('*** That nickname is invalid.')],
        )
        return self.deferExpectedMessages(messages)

    def test_invalid_nick_on_login(self):
        messages = [
            Rx('*** Hello! What is your nickname?'),
            Tx('badnick2#$'),
            Rx('*** That nickname is invalid.'),
            Tx('fixednick'),
            Rx('*** Type "/help" for help.'),
            Rx('*** fixednick has joined.'),
            Tx('/quit'),
            Rx('*** fixednick has left.')
        ]
        return self.deferExpectedMessages(messages)

    def test_chat_broadcast_to_all_users(self):
        alice_messages = sessionMessages(
            'alice',
            [
                Rx('*** Incoming connection!'),
                Rx('*** bob has joined.'),
                Rx('*** Incoming connection!'),
                Rx('*** charlie has joined.'),
                Rx('<charlie> Hi everyone!'),
                Rx('<charlie> Can you hear me?'),
                Tx('I can hear you, charlie'),
                Rx('<alice> I can hear you, charlie'),
                Rx('<bob> I can hear you too!'),
                Rx('*** charlie has left.'),
                Rx('*** bob has left.'),
            ]
        )
        bob_messages = sessionMessages(
            'bob',
            [
                Rx('*** Incoming connection!'),
                Rx('*** charlie has joined.'),
                Rx('<charlie> Hi everyone!'),
                Rx('<charlie> Can you hear me?'),
                Rx('<alice> I can hear you, charlie'),
                Tx('I can hear you too!'),
                Rx('<bob> I can hear you too!'),
                Rx('*** charlie has left.'),
            ]
        )
        charlie_messages = sessionMessages(
            'charlie',
            [
                Tx('Hi everyone!'),
                Rx('<charlie> Hi everyone!'),
                Tx('Can you hear me?'),
                Rx('<charlie> Can you hear me?'),
                Rx('<alice> I can hear you, charlie'),
                Rx('<bob> I can hear you too!'),
            ]
        )

        # This one is a bit tricky. Three clients involved connect 0.2 seconds
        # apart (alice, bob, then charlie), then charlie says two things,
        # alice responds, then bob responds, then they exit in the opposite
        # order they originally connected.
        alice_deferred = self.deferExpectedMessages(alice_messages, 2.0)
        reactor.callLater(
            0.2,
            lambda: alice_deferred.chainDeferred(
                self.deferExpectedMessages(bob_messages, 1.0)
            )
        )
        reactor.callLater(
            0.4,
            lambda: alice_deferred.chainDeferred(
                self.deferExpectedMessages(charlie_messages)
            )
        )
        return alice_deferred

    def test_error_nonunique_nick_on_login(self):
        notdebbie_messages = [
            Rx('*** Hello! What is your nickname?'),
            Tx('debbie'),
            Rx('*** That nickname is already in use.'),
            Tx('notdebbie'),
            Rx('*** Type "/help" for help.'),
            Rx('*** notdebbie has joined.'),
            Tx('/quit'),
            Rx('*** notdebbie has left.')
        ]
        debbie_messages = sessionMessages(
            'debbie',
            [
                Rx('*** Incoming connection!'),
                Rx('*** notdebbie has joined.'),
                Rx('*** notdebbie has left.'),
            ]
        )
        debbie_deferred = self.deferExpectedMessages(debbie_messages, 2.0)
        reactor.callLater(
            0.5,
            lambda: debbie_deferred.chainDeferred(
                self.deferExpectedMessages(notdebbie_messages)
            )
        )
        return debbie_deferred

    def test_error_nonunique_nick(self):
        wannabeevan_messages = sessionMessages(
            'wannabeevan',
            [Tx('/nick evan'), Rx('*** That nickname is already in use.')]
        )
        evan_messages = sessionMessages(
            'evan',
            [
                Rx('*** Incoming connection!'),
                Rx('*** wannabeevan has joined.'),
                Rx('*** wannabeevan has left.'),
            ]
        )
        evan_deferred = self.deferExpectedMessages(evan_messages, 1.0)
        reactor.callLater(
            0.2,
            lambda: evan_deferred.chainDeferred(
                self.deferExpectedMessages(wannabeevan_messages)
            )
        )
        return evan_deferred


# Message constructs
class Message(namedtuple('BaseMessage', ['message'])):
    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.message)


class Tx(Message):
    """Message to transmit"""


class Rx(Message):
    """Message to receive"""


def loginMessages(nick):
    """
    Return a list of Message instances for the initial login process
    for the nickname ``nick``.

    """
    return [
        Rx('*** Hello! What is your nickname?'),
        Tx(nick),
        Rx('*** Type "/help" for help.'),
        Rx('*** %s has joined.' % (nick,)),
    ]


def logoffMessages(nick):
    """
    Return a list of Message instances for the logoff process for
    the nickname ``nick``.

    """
    return [
        Tx('/quit'),
        Rx('*** %s has left.' % (nick,)),
    ]


def sessionMessages(nick, innerMessages, endNick=None):
    """
    Return a list of Message instances for the entire session, including
    login, between login/logoff, and logoff.

    If ``endNick`` is provided, it will be used instead of ``nick`` in
    the call to logoffMessages.

    """
    if endNick is None:
        endNick = nick
    messages = loginMessages(nick)
    messages.extend(innerMessages)
    messages.extend(logoffMessages(endNick))
    return messages


# State Machine and protocol
class SendReceiveStateAsserter(object):
    """
    State machine used by ``StateMachineClient`` to send messages and
    make assertions about received messages.

    The ``deferred`` attribute is used to record the assertions, and is
    chained to the protocol's deferred.

    """
    def __init__(self, messages):
        # stack of Tx/Rx messages
        self.messages = list(reversed(messages))
        self.deferred = defer.Deferred()

    def addAssertion(self, assertionMethod, *args):
        """
        Add a callback to self.deferred that invokes ``assertionMethod``
        with ``*args`` and ignores the input.

        """
        @self.deferred.addCallback
        def cbAssertion(ignored):
            assertionMethod(*args)

    def recordReceived(self, messageString, testInstance):
        """
        Verify that a message was expected to be received, and that it
        fits the expected message content.

        """
        if self.messages:
            if type(self.messages[-1]) is Rx:
                self.addAssertion(
                    testInstance.assertEqual,
                    self.messages.pop().message,
                    messageString
                )
            else:
                # This branch shouldn't be hit, since we flush all the Tx
                # messages off the stack inside transmitNext
                self.addAssertion(
                    testInstance.fail,
                    'Expected to transmit %r next but received %r' % (
                        self.messages[-1].message,
                        messageString
                    )
                )
        else:
            self.addAssertion(
                testInstance.fail,
                'Received %r but expected no more actions' % (messageString,)
            )

    def transmitNext(self, lineProtocol):
        """
        Flush all Tx messages off the end of the stack until an Rx
        message is seen.

        If the stack becomes empty, disconnect from the server.

        """
        while self.messages:
            if type(self.messages[-1]) is Rx:
                break
            lineProtocol.sendLine(self.messages.pop().message)
        else:
            lineProtocol.transport.loseConnection()

    def assertFinished(self, testInstance):
        """
        Finally make sure that the message stack is empty.

        """
        self.addAssertion(testInstance.assertEqual, self.messages, [])


class StateMachineClient(LineReceiver):
    """
    Simple ``LineReceiver`` implementation driven by a
    ``SendReceiveStateAsserter`` state machine.

    The ``deferred`` attribute chains the state machine's deferred,
    and will fire when the protocol loses connection to the server.

    The ``testInstance`` attribute is the TestCase instance used
    by the state machine to record failures.

    """
    def __init__(self, messages, testInstance):
        """``messages`` is passed directly to the state machine."""
        self.deferred = defer.Deferred()
        self.testInstance = testInstance
        self.stateMachine = SendReceiveStateAsserter(messages)
        self.deferred.chainDeferred(self.stateMachine.deferred)

    def connectionMade(self):
        """Flush any messages waiting to be sent."""
        self.stateMachine.transmitNext(self)

    def connectionLost(self, reason):
        """
        Call the final assertion method, and fire the deferred (which
        in turn fires the state machine's deferred)

        """
        self.stateMachine.assertFinished(self.testInstance)
        self.deferred.callback(None)

    def sendLine(self, line):
        #log.err('Sending line: %r' % (line,))
        LineReceiver.sendLine(self, line)

    def lineReceived(self, line):
        """
        Tell the state machine about the received message, and flush
        any messages waiting to be sent.

        """
        #log.err('Received line: %r' % (line,))
        self.stateMachine.recordReceived(line, self.testInstance)
        self.stateMachine.transmitNext(self)


class SimpleFactory(Factory):
    """
    Passthrough Factory. clientClass is the class of the protocol to
    build, other positional and keyword args are passed to the
    protocol's constructor.

    """
    def __init__(self, clientClass, *args, **kwargs):
        self.clientClass = clientClass
        self.args = args
        self.kwargs = kwargs

    def buildProtocol(self, addr):
        return self.clientClass(*self.args, **self.kwargs)
