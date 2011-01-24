from django.core.management.base import NoArgsCommand, CommandError
from django.core.mail import send_mail
from django.conf import settings
from optparse import make_option
from sitescheck.models import Content, Recipient

class Command(NoArgsCommand):
  help = 'Notify variations, if necessary, to all recipients'
  
  def handle_noargs(self, **options):   
    msg = ''
    for content in Content.objects.filter(verification_status=Content.STATUS_CHANGED):
      msg += "%s (%s)\n" % (content.title, content.url)

    if msg != '':
      print msg
      recipients = ()
      for recipient in Recipient.objects.all():
        recipients += (recipient.name, recipient.email)
        print "  %s (%s)" % (recipient.name, recipient.email)
      try:
        send_mail('[Openpolis] Cambiamento nei siti sotto controllo!', 
                  msg, settings.DEFAULT_FROM_EMAIL, 
                  recipients, fail_silently=False)
        content.verification_status = Content.STATUS_NOT_CHANGED
        content.verification_error = ''
      except:
        print "Errore"
    else:
      raise CommandError('No changes')        