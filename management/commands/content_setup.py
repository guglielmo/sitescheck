from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from sitescheck.models import Content
import datetime
import sys

class Command(BaseCommand):
  args = '<id> <id>'
  help = 'Setup content, getting live from specified websites'

  option_list = BaseCommand.option_list + (
    make_option('--dryrun',
        action='store_true',
        dest='dryrun',
        default=False,
        help='Execute a dry run: no db is written.'),
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
        contents = Content.objects.filter(todo='yes')[offset:(offset+limit)]
      else:
        contents = Content.objects.filter(todo='yes')[offset:]
    else:
      contents = Content.objects.filter(id__in=args)
    
    if (len(contents) == 0):
      print "no content to get this time"
      
    for cnt, content in enumerate(contents):
      err_msg = ''
      try:
        content.meat = content.get_live_meat()
        content.verification_status = Content.STATUS_NOT_CHANGED
        content.verification_error = None
        content.verified_at = None
      except IOError:
        err_msg = "Errore: Url non leggibile: %s" % (content.url)
      except Exception, e:
        err_msg = "Errore sconosciuto: %s" % (e)
      finally:
        if err_msg != '':
          if options['dryrun'] == False:
            content.verification_status = Content.STATUS_ERROR
            content.verification_error = err_msg
            content.verified_at = datetime.datetime.now()
            content.save()
          print "%s/%s - %s while processing %s (id: %s)" % \
                (cnt+1, len(contents), err_msg, content, content.id,)
        else:
          print "%s/%s - %s is %s (id: %s)" % \
                (cnt+1, len(contents), content, 
                 Content.STATUS_NOT_CHANGED, content.id,)
          if options['showhtml'] == True:
             print "Meaningful content: %s" % content.get_live_meat()
          if options['dryrun'] == False:
              content.save()
        
  

