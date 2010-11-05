from sys import path

path.insert(0, '../')
path.insert(0, '../lib/')

import web
import template
import util

from google.appengine.api.mail import EmailMessage

urls = (
    '/send_mail/?', 'send_mail',
)

class send_mail:
    def POST(self):
        d = web.input()
        t = template.env.get_template('message.html')
        sender = util.get_user(user_id=d.sender_id)
        recipient = util.get_user(user_id=d.recipient_id)
        message = EmailMessage(
            sender=' '.join([
                sender.nickname,
                '<' + sender.user.email() + '>'
            ]),
            subject=' '.join([
                'The Connection Machine:',
                sender.nickname,
                'wants to get in touch!'
            ]),
            to=recipient.user.email(),
            reply_to=sender.user.email(),
            body=t.render(
                msg=d.message,
                sender=sender.id,
                site=web.ctx.homedomain,
                plain_text=True
            ),
            html=t.render(
                msg=d.message,
                sender=sender.id,
                site=web.ctx.homedomain
            ),
        )
        message.send()
