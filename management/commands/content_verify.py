from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from sitescheck.models import Content
import datetime
import sys

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
    make_option('--offset',
        action='store',
        type='int',
        dest='offset',
        default=0,
        help='Force offset <> 0'),
    make_option('--limit',
        action='store',
        type='int',
        dest='limit',
        default=0,
        help='Force offset <> 0'),
  )
      
  
  def handle(self, *args, **options):
    offset = options['offset']
    limit = options['limit']

    if len(args) == 0:
      if (limit > 0):
        contents = Content.objects.all()[offset:(offset+limit)]
      else:
        contents = Content.objects.all()[offset:]
    else:
      contents = Content.objects.filter(id__in=args)
    
    for content in contents:
      hashed = ''
      err_msg = ''
      try:
        verification_status = content.verify(options['dryrun'])
      except IOError:
        err_msg = "Errore: Url non leggibile: %s" % (content.url)
      except Exception:
        (e_type, e_value, e_traceback) = sys.exc_info()
        err_msg = "Errore sconosciuto (%s): %s" % (e_type, e_value)
      finally:
        if err_msg != '':
          if options['dryrun'] == False:
            content.verification_status = Content.STATUS_ERROR
            content.verification_error = err_msg
            content.verified_at = datetime.datetime.now()
            content.save()
          print "id: %s - %s" % (content.id,  err_msg)
        else:
          print "%s: %s (%s)" % (content.id, content, verification_status)
          if options['showhash'] == True:
            print "hash: %s" % content.check_hash()
          if options['showhtml'] == True:
            print "%s" % content.get_html()

        print "---\n"
          
        