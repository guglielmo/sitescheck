from django.core.management.base import NoArgsCommand, CommandError
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from optparse import make_option
from sitescheck.models import Content, Recipient

class Command(NoArgsCommand):
  help = 'Notify variations, if necessary, to all recipients'
  
  option_list = NoArgsCommand.option_list + (
      make_option('--dryrun',
          action='store_true',
          dest='dryrun',
          default=False,
          help='Execute a dry run: no email is sent, no db is written.'),
      )
  
  
  def handle_noargs(self, **options):   
    msg_txt, msg_html = '', '<ul style="disc-style:none">'
    for content in Content.objects.filter(verification_status=Content.STATUS_CHANGED):
      msg_txt += "%s\n" % content.title
      msg_html += "<li>(<a href=\"%s\">%s</a>)</li>" % (content.url, content.title)
    msg_html += '</ul>'
  
    if msg_txt != '':
      recipients = []
      for recipient in Recipient.objects.all():
        recipients.append(recipient.email)
      print "recipients: " + "; ".join(recipients)

      if  options['dryrun'] != True:
        try:
          subject = '[Openpolis] Cambiamento nei siti sotto controllo!'
          msg = EmailMultiAlternatives(subject, msg_txt, settings.DEFAULT_FROM_EMAIL, recipients)
          msg.attach_alternative(msg_html, "text/html")
          msg.send()
          content.verification_status = Content.STATUS_NOT_CHANGED
          content.verification_error = ''
          content.save()
          print "ok"
        except:
          print "error sending email"
      else:
        print "will not send a bit; it's a dry run!"
    else:
      raise CommandError('No changes')        