import inspect
import time
import logging
import re
from pathlib import Path

from telethon import events

from DaisyX import CMD_LIST, LOAD_PLUG
import glob
import sys
from DaisyX import ubot
from DaisyX import telethn as tbot
from pymongo import MongoClient
from DaisyX import MONGO_DB_URI

client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["missjuliarobot"]
gbanned = db.gban


def register(**args):
    pattern = args.get("pattern")
    r_pattern = r"^[/]"

    if pattern is not None and not pattern.startswith("(?i)"):
        args["pattern"] = "(?i)" + pattern

    args["pattern"] = pattern.replace("^/", r_pattern, 1)
    stack = inspect.stack()
    previous_stack_frame = stack[1]
    file_test = Path(previous_stack_frame.filename)
    file_test = file_test.stem.replace(".py", "")
    reg = re.compile("(.*)")

    if pattern is not None:
        try:
            cmd = re.search(reg, pattern)
            try:
                cmd = cmd.group(1).replace("$", "").replace("\\", "").replace("^", "")
            except BaseException:
                pass

            try:
                CMD_LIST[file_test].append(cmd)
            except BaseException:
                CMD_LIST.update({file_test: [cmd]})
        except BaseException:
            pass

    def decorator(func):
        async def wrapper(check):
            if check.edit_date:
                return
            if check.fwd_from:
                return
            if check.is_group or check.is_private:
                pass
            else:
                print("i don't work in channels")
                return
            users = gbanned.find({})
            for c in users:
                if check.sender_id == c["user"]:
                    return
            try:
                await func(check)
                try:
                    LOAD_PLUG[file_test].append(func)
                except Exception:
                    LOAD_PLUG.update({file_test: [func]})
            except BaseException:
                return
            else:
                pass

        tbot.add_event_handler(wrapper, events.NewMessage(**args))
        return wrapper

    return decorator


def juliabot(**args):
    pattern = args.get("pattern", None)
    disable_edited = args.get("disable_edited", False)
    ignore_unsafe = args.get("ignore_unsafe", False)
    unsafe_pattern = r"^[^/!#@\$A-Za-z]"
    group_only = args.get("group_only", False)
    disable_errors = args.get("disable_errors", False)
    insecure = args.get("insecure", False)
    if pattern is not None and not pattern.startswith("(?i)"):
        args["pattern"] = "(?i)" + pattern

    if "disable_edited" in args:
        del args["disable_edited"]

    if "ignore_unsafe" in args:
        del args["ignore_unsafe"]

    if "group_only" in args:
        del args["group_only"]

    if "disable_errors" in args:
        del args["disable_errors"]

    if "insecure" in args:
        del args["insecure"]

    if pattern:
        if not ignore_unsafe:
            args["pattern"] = args["pattern"].replace("^.", unsafe_pattern, 1)

    def decorator(func):
        async def wrapper(check):
            if check.edit_date and check.is_channel and not check.is_group:
                return
            if group_only and not check.is_group:
                return
            if check.via_bot_id and not insecure and check.out:
                # Ignore outgoing messages via inline bots for security reasons
                return

            try:
                await func(check)
            except events.StopPropagation:
                raise events.StopPropagation
            except KeyboardInterrupt:
                pass
            except BaseException as e:
                print(e)
            else:
                pass

        if not disable_edited:
            ubot.add_event_handler(wrapper, events.MessageEdited(**args))
        ubot.add_event_handler(wrapper, events.NewMessage(**args))
        return wrapper

    return decorator

