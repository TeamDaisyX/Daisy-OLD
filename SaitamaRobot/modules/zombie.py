# This bot checks list of the chats specified below and kicks deleted accounts

from pyrogram import Client
from pyrogram.errors import FloodWait
import time
import yaml

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

api_id = cfg['telegram']['api_id']
api_hash = cfg['telegram']['api_hash']
notify_before = cfg['notifications']['notify_before']
notify_after = cfg['notifications']['notify_after']
notify_before_ids = cfg['notifications']['notify_before_ids']
notify_after_ids = cfg['notifications']['notify_after_ids']
chat_ids = cfg['bot']['chat_ids']
SLEEP_PER_CHAT = cfg['bot']['sleep_per_chat']
SLEEP_AFTER_KICK = cfg['bot']['sleep_after_kick']
MAX_MESSAGE_LENGTH = 4000

def main():
    with Client("my_account", api_id, api_hash) as app:
        overall_kick_count = 0
        report = ""

        if notify_before:
            for user_id in notify_before_ids:
                do_notify_before(user_id, app)

        j = 0
        while j < len(chat_ids):
            chat_id = chat_ids[j]
            j += 1
            chat_id = int(chat_id)
            try:
                chat_info = app.get_chat(chat_id)
            except FloodWait as e:
                print("Getting chat info: Floodwait triggered. Trying again in {} seconds.".format(e.x))
                time.sleep(e.x)
                j -= 1
                continue
            except Exception as ex:
                msg = "Error of type {} occured when getting chat info: {}. Error message:".format(type(ex).__name__, ex.args)
                print(msg)
                report += msg+"\n"
                continue
            
            print("==========================================")
            print("")
            print("Working on chat {} now".format(chat_info.title))
            report += "=========================== \n {}\n===========================\n".format(chat_info.title)
            member_list = app.iter_chat_members(chat_id)
            kick_list = []
            skip_chat = False

            found_self = False
            for member in member_list:
                if member.user.is_self:
                    found_self = True
                    if (not member.status == "administrator" or not member.can_restrict_members) and not member.status == "creator":
                        msg = "⚠️⚠️⚠️ I have no permissions to kick members in {}. Skipping this chat... \n\n".format(chat_info.title)
                        print(msg)
                        report += msg+"\n"
                        skip_chat = True
                if member.user.is_deleted:
                    kick_list.append(member)
            
            if not found_self:
                msg = "⚠️⚠️⚠️ I'm no member of the group {}! Skipping this chat...\n\n".format(chat_info.title)
                print(msg)
                report += msg+"\n"
                skip_chat = True
            if skip_chat:
                continue

            print("Members to kick from {}".format(chat_info.title))
            kick_count = 0
            i = 0
            while i < len(kick_list):
                member = kick_list[i]
                i +=1
                display_userinfo(member)
                try:
                    app.kick_chat_member(chat_id, member.user.id)
                    time.sleep(SLEEP_AFTER_KICK)
                except FloodWait as e:
                    print("Kicking: Floodwait triggered. Trying again in {} seconds.".format(e.x))
                    time.sleep(e.x)
                    i -= 1
                    continue
                except Exception as ex:
                    msg = "Error of type {} occured when kicking user: {}. Error message:".format(type(ex).__name__, ex.args)
                    print(msg)
                    report += msg+"\n"
                    continue
                kick_count += 1
            overall_kick_count += kick_count

            msg = "Kicked {} deleted accounts from {}".format(kick_count, chat_info.title)
            print(msg)
            report += msg + "\n"

            print("Sleeping for {} seconds before continuing with next chat".format(SLEEP_PER_CHAT))
            time.sleep(SLEEP_PER_CHAT)
            report += "\n\n"
        msg = "Kicked {} users overall.".format(overall_kick_count)
        print(msg)
        report += "\n\n"+msg

        if notify_after:
            for user_id in notify_after_ids:
                do_notify_after(user_id, app, report)

def display_userinfo(chat_member):
    print("Name: {} {} (@{})".format(chat_member.user.first_name, chat_member.user.last_name, chat_member.user.username))
    print("is_deleted: {}".format(chat_member.user.is_deleted))

def do_notify_before(user_id, client):
    client.send_message(int(user_id), "Starting to clean up groups from deleted accounts")

def do_notify_after(user_id, client, report):
        send_message_split(user_id, client, "Sucessfully cleaned up. Full report: {}".format(report))

#sends a message longer than the telegram limit allows by splitting it into multiple. Always uses code formatting for the message
def send_message_split(user_id, client, message): 
    current_position = 0
    while current_position < len(message):
        end = min(current_position + MAX_MESSAGE_LENGTH, len(message) - 1)
        text = message[current_position:end]
        if len(text) == 0:
            return
        text = "```" + text + "```"
        current_position = end

        client.send_message(user_id, text, "markdown")



if __name__ == "__main__":
    main()
