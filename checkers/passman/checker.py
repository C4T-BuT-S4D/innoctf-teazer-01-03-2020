#!/usr/bin/env python3

from gevent import monkey

monkey.patch_all()

import os
import random
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from passman_lib import *


class Checker(BaseChecker):
    def __init__(self, *args, **kwargs):
        super(Checker, self).__init__(*args, **kwargs)
        self.mch = CheckMachine(self)

    def action(self, action, *args, **kwargs):
        try:
            super(Checker, self).action(action, *args, **kwargs)
        except requests.exceptions.ConnectionError:
            self.cquit(Status.DOWN, 'Connection error', 'Got requests connection error')

    def check(self):
        u, p = self.mch.register()
        sess = self.mch.login(u, p)
        users = self.mch.list_users(sess)
        self.assert_in(u, users, 'Invalid users page')

        passwords = []
        for _ in range(random.randint(10, 15)):
            passwords.append(self.mch.add_password(sess))

        def check1():
            returned = self.mch.list_passwords(requests, u, random.choice(passwords))
            if not set(passwords).issubset(set(returned)):
                cquit(Status.MUMBLE, 'Invalid password listing', 'check1')

        def check2():
            returned = self.mch.list_passwords(sess, u, random.choice(passwords))
            if not set(passwords).issubset(set(returned)):
                cquit(Status.MUMBLE, 'Invalid password listing', 'check2')

        def check3():
            u1, p1 = self.mch.register()
            tsess = self.mch.login(u1, p1)
            returned = self.mch.list_passwords(tsess, u, random.choice(passwords))
            if not set(passwords).issubset(set(returned)):
                cquit(Status.MUMBLE, 'Invalid password listing', 'check3')

        checks = [check1, check2, check3]
        random.shuffle(checks)
        for check in checks:
            check()

        self.cquit(Status.OK)

    def put(self, flag_id, flag, vuln):
        u, p = self.mch.register()
        sess = self.mch.login(u, p)

        passwords = [rnd_password() for _ in range(random.randint(9, 14))]
        passwords.append(flag)
        random.shuffle(passwords)

        for pp in passwords:
            self.mch.add_password(sess, pp)

        self.cquit(Status.OK, f'{u}:{p}:{random.choice(passwords)}')

    def get(self, flag_id, flag, vuln):
        u, p, rnd = flag_id.split(':')
        sess = self.mch.login(u, p)

        def check1():
            returned = self.mch.list_passwords(requests, u, random.choice((flag, rnd)))
            self.assert_in(flag, returned, 'Invalid flag listing', status=Status.CORRUPT)
            self.assert_in(rnd, returned, 'Invalid flag listing', status=Status.CORRUPT)

        def check2():
            returned = self.mch.list_passwords(sess, u, random.choice((flag, rnd)))
            self.assert_in(flag, returned, 'Invalid flag listing', status=Status.CORRUPT)
            self.assert_in(rnd, returned, 'Invalid flag listing', status=Status.CORRUPT)

        def check3():
            u1, p1 = self.mch.register()
            tsess = self.mch.login(u1, p1)
            returned = self.mch.list_passwords(tsess, u, random.choice((flag, rnd)))
            self.assert_in(flag, returned, 'Invalid flag listing', status=Status.CORRUPT)
            self.assert_in(rnd, returned, 'Invalid flag listing', status=Status.CORRUPT)

        checks = [check1, check2, check3]
        random.shuffle(checks)
        for check in checks:
            check()

        self.cquit(Status.OK)


if __name__ == '__main__':
    c = Checker(sys.argv[2])

    try:
        c.action(sys.argv[1], *sys.argv[3:])
    except c.get_check_finished_exception():
        cquit(Status(c.status), c.public, c.private)
