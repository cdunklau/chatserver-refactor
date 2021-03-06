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

MESSAGES_ETC = [
    '*** Server going down!',
    '*** Currently connected: ',
    (
        '*** Available commands:\r\n'
        '***  /help -- get help\r\n'
        '***  /quit -- disconnect\r\n'
        '***  /me -- perform an action\r\n'
        '***  /who -- list connected users\r\n'
        '***  /nick -- change your nickname to something better'
    ),
    '*** %s is now known as %s.',
    '*** That nickname is invalid.',
    '*** Type "/help" for help.',
    '*** Hello! What is your nickname?',
    '*** That nickname is already in use.',
    '*** Incoming connection!',
    '*** No such command: /%s',
    '*** %s has joined.',
    '^/([A-z]*)\\s*(.*)$',
    '^[A-z0-9_]+$',
    '*** %s has left.',
    '* %s %s',
    '<%s> %s'
]

main = lambda port: (
                map(
                    lambda r:  (
                        lambda rr: (
                            setattr(namespace, *rr)
                            if (type(rr) is tuple and len(rr) == 2)
                            else None
                        )
                    )(r()),
                    [
                        lambda: map(
                            setattr,
                            *zip(
                                *[
                                    (namespace, m, __import__(m))
                                    for m
                                    in MODULES
                                ]
                            )
                        ),
                        lambda: map(
                            namespace.s['signal.signal'],
                            (namespace.s['signal.SIGINT'], namespace.s['signal.SIGTERM']),
                            [
                                lambda s, f: (
                                    namespace.s['sys.exit']()
                                    if namespace.f
                                    else (
                                        [namespace.sa(MESSAGES_ETC[0], namespace.o)] and
                                        namespace.u('f', True) or
                                        namespace.fc(namespace.l)
                                    )
                                )
                            ] * 2
                        ),
                        lambda: (
                            'sw',
                            namespace.s['types.Functio' 'nType'](
                                compile(
                                    "try:\n"
                                    "\tv = namespace.select.select(namespace.so, namespace.w(), [])\n"
                                    "except namespace.select.error, e:\n"
                                    "\tif e[0] != namespace.errno.EINTR: raise\n"
                                    "else:\n"
                                    "\tnamespace.u('sr', v)",
                                    '',
                                    'exec'
                                ),
                                dict(namespace=namespace, OSError=OSError)
                            )
                        ),
                        lambda: (
                            'l',
                            namespace.s['socket.socket'](
                                namespace.s['socket.AF_INET'],
                                namespace.s['socket.SOCK_STREAM']
                            )
                        ),
                        lambda: namespace.s['l.bind'](('', port)),
                        lambda: namespace.s['l.listen'](5),
                        lambda: (
                            'ro', lambda: filter(lambda s: s in namespace.nn,  namespace.so)
                        ),
                        lambda: namespace.update(
                            si=(lambda o: o.__setitem__),
                            di=(lambda o: o.__delitem__),
                            cr=namespace.s['re.compile'](MESSAGES_ETC[11]),
                            nn={},
                            dp=lambda s, d, c, l: namespace.dd.get(c, d)(s, l, c),
                            dd=dict(
                                me=lambda s, l, c: (
                                    namespace.sa(MESSAGES_ETC[14] % (namespace.nn[s], l))
                                ),
                                quit=lambda s, l, c: namespace.c(s),
                                who=lambda s, l, c: namespace.ws(
                                    s, MESSAGES_ETC[1] + ', '.join(namespace.s['nn.values']())
                                ),
                                help=lambda s, l, c: namespace.ws(s, MESSAGES_ETC[2]),
                                nick=lambda s, l, c: (
                                    (
                                        (
                                            [namespace.sa(MESSAGES_ETC[3] % (namespace.nn[s], l))] and
                                            namespace.si(namespace.nn)(s, l)
                                        )
                                        if namespace.nr.match(l)
                                        else namespace.ws(s, MESSAGES_ETC[4])
                                    )
                                    if l not in namespace.nn.values()
                                    else namespace.ws(s, MESSAGES_ETC[7])
                                )
                            ),
                            so=(namespace.u('f', False) or [namespace.l]),
                            ib=namespace.s['collections' '.defaultdict'](list),
                            ob=namespace.s['collections.defaultdict'](list),
                            o=(lambda: filter(lambda s:  s is not namespace.l, namespace.so)),
                            w=(lambda: filter(namespace.ob.__getitem__, namespace.o())),
                            ws=(lambda s, l: namespace.ob[s].append(l + '\r\n')),
                            nr=namespace.s['re.compile'](MESSAGES_ETC[12]),
                            sa=(
                                lambda d, f=namespace.ro: map(
                                    lambda s: namespace.ws(s, d),
                                    f()
                                )
                            ),
                            fs=set(),
                            c=(
                                lambda s: [
                                    namespace.sa(MESSAGES_ETC[13] % namespace.nn[s])
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
                                                            namespace.sa(MESSAGES_ETC[8])
                                                        ),
                                                        lambda: (
                                                            namespace.so.append(
                                                                s.accept()[0]
                                                            )
                                                        ),
                                                        lambda: namespace.ws(
                                                            namespace.so[-1],
                                                            MESSAGES_ETC[6]
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
                                                    MESSAGES_ETC[15] % (
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
                                                                MESSAGES_ETC[9] % c
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
                                                        [namespace.ws(s, MESSAGES_ETC[5])] and
                                                        namespace.sa(MESSAGES_ETC[10] % l)
                                                    )
                                                    if namespace.nr.match(l)
                                                    else namespace.ws(s, MESSAGES_ETC[4])
                                                )
                                                if l not in namespace.nn.values()
                                                else namespace.ws(s, MESSAGES_ETC[7])
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
                        lambda: namespace.s['l.' 'close']()
                    ]
                )
            )
