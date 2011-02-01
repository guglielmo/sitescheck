from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from sitescheck.models import Content
import datetime

class Command(BaseCommand):
  args = '<id> <id>'
  help = 'Verify specified content'

  option_list = BaseCommand.option_list + (
    make_option('--dryrun',
        action='store_true',
        dest='dryrun',
        default=False,
        help='Execute a dry run: no db is written.'),
    make_option('--hash',
        action='store_true',
        dest='showhash',
        default=False,
        help='Show hash code.'),
    make_option('--html',
        action='store_true',
        dest='showhtml',
        default=False,
        help='Show html code.'),
  )
      
  
  def handle(self, *args, **options):
    if len(args) == 0:
      contents = Content.objects.all()
    else:
      contents = Content.objects.filter(id__in=args)
    
    for content in contents:
      hashed = ''
      err_msg = ''
      try:
        verification_status = content.verify(options['dryrun'])
      except IOError as detail:
        err_msg = "Url non leggibile: %s" % (content.url)
      except Exception as detail:
        err_msg = "Errore sconosciuto (%s): %s" % (type(detail), detail)
      finally:
        if err_msg != '':
          if options['dryrun'] == False:
            content.verification_status = Content.STATUS_ERROR
            content.verification_error = err_msg
            content.verified_at = datetime.datetime.now()
            content.save()
          print "%s: %s - %s" % (content.id, content, err_msg)
        else:
          print "%s: %s (%s)" % (content.id, content, verification_status)
          if options['showhash'] == True:
            print "hash: %s" % content.check_hash()
          if options['showhtml'] == True:
            print "%s" % content.get_html()
          print "---\n"
          
        