# -*- coding: utf-8 -*-
#
# github_plugin.py for kakoune-blackboard
# by lenormf
#

import shlex
import codecs
import subprocess

from irc3.plugins.command import command
import irc3


def str_unescape(s):
    return codecs.decode(codecs.encode(s, "latin-1", "backslashreplace"), "unicode-escape")


def str_escape(s):
    return codecs.decode(codecs.encode(s, "unicode-escape"), "latin-1", "backslashreplace")


@irc3.plugin
class KakouneBlackboard:
    requires = ["irc3.plugins.log"]

    def __init__(self, bot):
        self.bot = bot
        self.log = bot.log

    def _prefix_messages(self, messages, prefix):
        return ["%s%s" % (prefix, v) for v in messages]

    @command(permission="view", aliases=["v"])
    async def version(self, mask, target, args):
        """Show the version of Kakoune invoked

           %%version
        """

        version = subprocess.check_output(["kak", "-version"])
        version = version.decode("utf-8").strip()

        if target.startswith("#"):
            return "%s: %s" % (mask.nick, version)
        else:
            return version

    @command(permission="view", aliases=["exec"])
    async def execute_keys(self, mask, target, args):
        """Execute primitives on the given data

           %%execute_keys <data> <key>...
        """

        self.log.debug("User %s is executing keys: %s", mask.nick, (mask, target, args))

        keys = shlex.split(shlex.quote("".join(args["<key>"])))[0]

        self.log.debug("keys: [%s]", keys)

        cmd = [
            "kak",
            "-n",
            "-f",
            keys,
        ]
        p = subprocess.Popen(cmd,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)

        data = str_unescape(args["<data>"])

        self.log.debug("data: [%s]", data)

        stdout_data, stderr_data = p.communicate(data.encode("utf-8"))
        exit_code = p.wait()

        self.log.debug("the process exited with code %d", exit_code)

        data_output = ""
        messages = []
        if not exit_code:
            data_output = stdout_data
        else:
            messages.append("error code %d" % exit_code)
            data_output = stderr_data

        data_output = str_escape(data_output.decode("utf-8"))

        self.log.debug("encoded output: %s", data_output)

        messages.append(data_output)

        if target.startswith("#"):
            return self._prefix_messages(messages, "%s: " % mask.nick)
        else:
            return messages
