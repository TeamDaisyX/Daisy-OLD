from DaisyX.services.redis import redis as r
from tempmail import TempMail
from DaisyX import bot
from DaisyX.decorator import register
from .utils.disable import disableable_dec
from .utils.message import get_arg
from .utils.message import get_args_str


@register(cmds=['newmail', 'addmail'])
@disableable_dec('newmail')
def newmail(m):
        #initialize Temp-Male and making a new Email.
        tm = TempMail()
        email = tm.get_email_address()
        r.set('email:{}:mail'.format(str(m.from_user.id)), email)
        bot.send_message(m.chat.id, 'Your new Email: '+email)
        
@register(cmds=['mails', 'mailinbox'])
@disableable_dec('mails')
def mails(m):
    try :
        #initialize Temp-Mail and read recieved Mails.
        mail = r.get('email:{}:mail'.format(str(m.from_user.id)))
        if not mail:
                bot.send_message(m.from_user.id, 'Make an email first.\nUse /newmail')
                return
        parts = mail.split('@')
        tm = TempMail(login=parts[0], domain='@'+parts[1])
        mails = tm.get_mailbox()
        if not mails :
                bot.send_message(m.from_user.id, 'There is no email...')
        else:
            if 'error' in mails :
                bot.send_message(m.from_user.id, 'There is no email...')
            else:
                print (mails)
                for i in mails:
                        bot.send_message(m.from_user.id, 'Mail from: '+i['mail_from']+'\n\nSubject: '+i['mail_subject']+'\n\nText: ' +i['mail_text'])
    except:
       bot.send_message(m.from_user.id, 'There is no email...')
