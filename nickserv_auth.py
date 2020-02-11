# -*- coding: utf-8 -*-
#
# nickserv_auth.py for kakoune-blackboard
# by lenormf
#

import irc3


@irc3.event(r"(@(?P<tags>\S+) )?:(?P<ns>.+)!NickServ@services."
            r" NOTICE (?P<nick>.+) :This nickname is registered.*")
def register(bot, ns=None, nick=None, **kw):
    if bot.config["password"]:
        bot.privmsg(ns, "identify %s %s" % (nick, bot.config["password"]))
