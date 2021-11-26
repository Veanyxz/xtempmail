from xtempmail import Email, extension
import logging
from xtempmail.mail import EmailMessage
app = Email(name='krn887', ext=extension[6], interval=2)
log = logging.getLogger('xtempmail')
log.setLevel(logging.INFO)
@app.on.message()
def baca(data: EmailMessage):
    print(f"\tfrom: {data.from_mail}\n\tsubject: {data.subject}\n\tpesan: {data.text}\n\tReply -> Hapus")
    option = {}
    ok = []
    for i in data.attachments: # -> Forward attachment
        ok.append(( i.name, i.download()))
    option['multiply_file'] = tuple(ok)
    if data.from_is_local:
        data.from_mail.send_message(data.subject,data.text, **option) # -> Forward message
    data.delete()  #delete message

@app.on.message(lambda msg:msg.attachments)
def get_message_media(data: EmailMessage):
    print(f'attachment: {[i.name for i in data.attachments]}')

@app.on.message(lambda x:x.from_mail.__str__().endswith('@gmail.com'))
def getGmailMessage(data: EmailMessage):
    print(f'Gmail: {data.from_mail}')

if __name__ == '__main__':
    try:
        app.listen_new_message() 
    except KeyboardInterrupt:
        app.destroy() #destroy inbox
        print('destroyed')
