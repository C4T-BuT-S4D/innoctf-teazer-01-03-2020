#!/usr/bin/env python3

from gevent import monkey

monkey.patch_all()

import os
import copy
import sys
argv = copy.deepcopy(sys.argv)

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pogemonko_lib import *


class Checker(BaseChecker):
    def __init__(self, *args, **kwargs):
        super(Checker, self).__init__(*args, **kwargs)
        self.mch = CheckMachine(self)

    def action(self, action, *args, **kwargs):
        try:
            super(Checker, self).action(action, *args, **kwargs)
        except pwnlib.exception.PwnlibException:
            self.cquit(Status.DOWN, 'Connection error', 'Got connection error')
        finally:
            self.mch.close_r()

    def check(self):
        self.mch.init_r()
        u1, p1 = self.mch.register()
        u2, p2 = self.mch.register()
        l = self.mch.list_users()
        self.assert_in(u1, l, "Can't find user in user list")
        self.assert_in(u2, l, "Can't find user in user list")

        self.mch.login(u1, p1)

        desc1, name1 = rnd_string(50), rnd_string(10)

        self.mch.catch_pokemon(desc1, name1)
        s = self.mch.list_pokemons()

        self.assert_in(desc1, s, "Can't find pokemon description")
        self.assert_in(name1, s, "Can't find pokemon name")

        self.mch.logout()

        self.mch.login(u2, p2)

        desc2, name2 = rnd_string(50), rnd_string(10)

        self.mch.catch_pokemon(desc2, name2)
        s = self.mch.list_pokemons()

        self.assert_in(desc2, s, "Can't find pokemon description")
        self.assert_in(name2, s, "Can't find pokemon name")

        f = self.mch.fight_user(u1)

        if "win" not in f and "lose" not in f and "Tie" not in f:
            self.cquit(Status.MUMBLE, "Can't get fight result")

        self.cquit(Status.OK)

    def put(self, flag_id, flag, vuln):
        self.mch.init_r()
        u, p = self.mch.register()
        self.mch.login(u, p)
        name = rnd_string(10)
        self.mch.catch_pokemon(flag, name)
        self.cquit(Status.OK, f"{u}:{p}")

    def get(self, flag_id, flag, vuln):
        self.mch.init_r()
        u, p = flag_id.split(":")
        self.mch.login(u, p)
        s = self.mch.list_pokemons()
        self.assert_in(flag, s, "Can't get flag", status=Status.CORRUPT)
        self.cquit(Status.OK)


if __name__ == '__main__':
    c = Checker(argv[2])

    try:
        c.action(argv[1], *argv[3:])
    except c.get_check_finished_exception():
        cquit(Status(c.status), c.public, c.private)
