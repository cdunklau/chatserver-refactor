class UnknownMap(dict):
    def __getattr__(self, k):
        return self[k]

    def u(self, *a):  # ** REMOVEME!!!
        return self.__setitem__(*a)  # ** REMOVEME!!!

    def __setattr__(self, k, v):
        return self.__setitem__(k, v)

    @property
    def s(self):
        class InnerUnknown(object):
            def __getitem__(innerself, k):
                return reduce(getattr, k.split('.'), self)
        return InnerUnknown()


# Was called "n"
namespace = UnknownMap()

MODULES = [
    'sys',
    'signal',
    'socket',
    'select',
    'collections',
    'errno',
    'types',
    'itertools',
    're'
]

SERVER_EXIT_MESSAGE = '*** Server going down!'
WHO_MESSAGE_PREFIX = '*** Currently connected: '
HELP_RESPONSE = (
    '*** Available commands:\r\n'
    '***  /help -- get help\r\n'
    '***  /quit -- disconnect\r\n'
    '***  /me -- perform an action\r\n'
    '***  /who -- list connected users\r\n'
    '***  /nick -- change your nickname to something better'
)
NICK_RESPONSE_FORMAT = '*** %s is now known as %s.'
NICK_RESPONSE_ERROR = '*** That nickname is invalid.'
HELP_MESSAGE = '*** Type "/help" for help.'
GREETING_PROMPT = '*** Hello! What is your nickname?'
NICK_NONUNIQUE_ERROR = '*** That nickname is already in use.'
INCOMING_MESSAGE = '*** Incoming connection!'
COMMAND_ERROR_FORMAT = '*** No such command: /%s'
JOIN_MESSAGE_FORMAT = '*** %s has joined.'
COMMAND_PATTERN = '^/([A-z]*)\\s*(.*)$'
WORD_PATTERN = '^[A-z0-9_]+$'
PART_MESSAGE_FORMAT = '*** %s has left.'
ACTION_MESSAGE_FORMAT = '* %s %s'
CHAT_MESSAGE_FORMAT = '<%s> %s'

def import_to_namespace():
    for module_name in MODULES:
        setattr(namespace, module_name, __import__(module_name))

def add_signal_handlers():
    signal_signal = namespace.s['signal.signal']

    def signal_handler(s, f):
        if namespace.f:
            namespace.s['sys.exit']()
        else:
            namespace.sa(SERVER_EXIT_MESSAGE, namespace.o)
            if not namespace.u('f', True):
                namespace.fc(namespace.l)

    signal_signal(namespace.s['signal.SIGINT'], signal_handler)
    signal_signal(namespace.s['signal.SIGTERM'], signal_handler)

def do_select_routine():
    try:
        v = namespace.select.select(namespace.so, namespace.w(), [])
    except namespace.select.error, e:
        if e[0] != namespace.errno.EINTR:
            raise
    else:
        namespace.u('sr', v)

def listen_socket():
    namespace.s['l.listen'](5)

def filter_namespace_ro_attrib():
    return [s for s in namespace.so if s in namespace.so]

def close_socket():
    namespace.s['l.close']()

def main(port):
    import_to_namespace()

    namespace.sw = do_select_routine
    namespace.l = namespace.s['socket.socket'](
        namespace.s['socket.AF_INET'],
        namespace.s['socket.SOCK_STREAM']
    )
    namespace.ro = filter_namespace_ro_attrib

    def bind_socket():
        namespace.s['l.bind'](('', port))

    functions_to_run = [
        add_signal_handlers,
        bind_socket,
        listen_socket,
        lambda: namespace.update(
            si=(lambda o: o.__setitem__),
            di=(lambda o: o.__delitem__),
            cr=namespace.s['re.compile'](COMMAND_PATTERN),
            nn={},
            dp=lambda s, d, c, l: namespace.dd.get(c, d)(s, l, c),
            dd=dict(
                me=lambda s, l, c: (
                    namespace.sa(ACTION_MESSAGE_FORMAT % (namespace.nn[s], l))
                ),
                quit=lambda s, l, c: namespace.c(s),
                who=lambda s, l, c: namespace.ws(
                    s, WHO_MESSAGE_PREFIX + ', '.join(namespace.s['nn.values']())
                ),
                help=lambda s, l, c: namespace.ws(s, HELP_RESPONSE),
                nick=lambda s, l, c: (
                    (
                        (
                            [namespace.sa(NICK_RESPONSE_FORMAT % (namespace.nn[s], l))] and
                            namespace.si(namespace.nn)(s, l)
                        )
                        if namespace.nr.match(l)
                        else namespace.ws(s, NICK_RESPONSE_ERROR)
                    )
                    if l not in namespace.nn.values()
                    else namespace.ws(s, NICK_NONUNIQUE_ERROR)
                )
            ),
            so=(namespace.u('f', False) or [namespace.l]),
            ib=namespace.s['collections' '.defaultdict'](list),
            ob=namespace.s['collections.defaultdict'](list),
            o=(lambda: filter(lambda s:  s is not namespace.l, namespace.so)),
            w=(lambda: filter(namespace.ob.__getitem__, namespace.o())),
            ws=(lambda s, l: namespace.ob[s].append(l + '\r\n')),
            nr=namespace.s['re.compile'](WORD_PATTERN),
            sa=(
                lambda d, f=namespace.ro: map(
                    lambda s: namespace.ws(s, d),
                    f()
                )
            ),
            fs=set(),
            c=(
                lambda s: [
                    namespace.sa(PART_MESSAGE_FORMAT % namespace.nn[s])
                    if s in namespace.nn and s not in namespace.fs
                    else None
                ] and namespace.s['fs.add'](s)
            ),
            fc=(
                lambda s: (
                    [s.close()] and
                    (namespace.so.remove(s) if s in namespace.so else None) or
                    (namespace.fs.remove(s) if s in namespace.fs else None) or
                    (namespace.di(namespace.ib)(s) if s in namespace.ib else None) or
                    (namespace.di(namespace.ob)(s) if s in namespace.ob else None) or
                    (namespace.di(namespace.nn)(s) if s in namespace.nn else None)
                )
            )
        ),
        lambda:  map(
            lambda f:  map(
                apply,
                [
                    lambda: namespace.u('sr', ([], [], [])),
                    lambda: namespace.sw(),
                    lambda: map(
                        apply,
                        [
                            lambda *ss: map(
                                lambda s: map(
                                    apply,
                                    [
                                        lambda: (
                                            namespace.sa(INCOMING_MESSAGE)
                                        ),
                                        lambda: (
                                            namespace.so.append(
                                                s.accept()[0]
                                            )
                                        ),
                                        lambda: namespace.ws(
                                            namespace.so[-1],
                                            GREETING_PROMPT
                                        )
                                    ]
                                ) if s is namespace.l else map(
                                    apply,
                                    [
                                        lambda: (
                                            namespace.ib[s].append(
                                                s.recv(4096)
                                            ) or
                                            (
                                                namespace.c(s)
                                                if (
                                                    namespace.ib[s][-1]
                                                    == ''
                                                )
                                                else None
                                            )
                                        )
                                    ]
                                ),
                                ss
                            ),
                            lambda *ss: map(
                                lambda s: (
                                    lambda d: (
                                        namespace.si(namespace.ob)(
                                            s,
                                            [d[s.send(d):]]
                                        ) or
                                        (
                                            namespace.si(namespace.ob)(s, [])
                                            if namespace.ob[s] == ['']
                                            else None
                                        )
                                    )
                                )(''.  join(namespace.ob[s])), ss),
                            lambda *ss: None
                        ],
                        namespace.sr
                    ),
                    lambda: [
                        namespace.di(v)(slice(None, None))
                        for k, v
                        in namespace.ob.items()
                        if v and not filter(None, v)
                    ],
                    lambda: namespace.u('sl', {}),
                    lambda: map(
                        (
                            lambda (k, v): (
                                namespace.si(namespace.sl)(
                                    k,
                                    ''.join(v).split('\r\n')
                                ) or namespace.si(namespace.ib)(
                                    k,
                                    [namespace.sl[k].pop()]
                                )
                            )
                        ),
                        namespace.ib.items()
                    ),
                    lambda: namespace.sl and map(
                        lambda (s, l): (
                            (
                                namespace.sa(
                                    CHAT_MESSAGE_FORMAT % (
                                        namespace.nn[s],
                                        l[1:]
                                        if l.startswith('//')
                                        else l
                                    )
                                )
                                if (
                                    not l.startswith('/') or
                                    l.startswith('//')
                                )
                                else (
                                    namespace.dp(
                                        s,
                                        lambda s, l, c: (
                                            namespace.ws(
                                                s,
                                                COMMAND_ERROR_FORMAT % c
                                            )
                                        ),
                                        *namespace.s['cr.match'](
                                            l
                                        ).groups()
                                    )
                                )
                            )
                            if s in namespace.nn
                            else (
                                (
                                    (
                                        namespace.si(namespace.nn)(s, l) or
                                        [namespace.ws(s, HELP_MESSAGE)] and
                                        namespace.sa(JOIN_MESSAGE_FORMAT % l)
                                    )
                                    if namespace.nr.match(l)
                                    else namespace.ws(s, NICK_RESPONSE_ERROR)
                                )
                                if l not in namespace.nn.values()
                                else namespace.ws(s, NICK_NONUNIQUE_ERROR)
                            )
                        ),
                        [
                            (s, l.rstrip())
                            for s, ll
                            in namespace.sl.items()
                            for l
                            in ll
                        ]
                    ),
                    lambda: (
                        namespace.f and
                        map(
                            lambda (s, b): (
                                namespace.fc(s)
                                if not filter(None, b)
                                else None
                            ),
                            namespace.ob.items()
                        )
                    ),
                    lambda: map(
                        lambda s: (
                            namespace.fc(s)
                            if not filter(None,  namespace.ob[s])
                            else None
                        ),
                        list(namespace.fs)
                    )
                ]
            ),
            iter(lambda: bool(namespace.so), False)
        ),
        close_socket
    ]
    for func in functions_to_run:
        result = func()
        if type(result) is tuple and len(result) == 2:
            name, value = result  # names for setattr args
            setattr(namespace, name, value)
