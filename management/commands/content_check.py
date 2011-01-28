from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from sitescheck.models import Content

class Command(BaseCommand):
  args = '<id> <id>'
  help = 'Check specified content and print the corresponding hash'
  
  def handle(self, *args, **options):
    # loop over ids passed as args
    for content_id in args:
      # grab content from db or print error message
      try:
        content = Content.objects.get(pk=int(content_id))
      except Content.DoesNotExist:
        print '%s: content does not exist!\n' % content_id
      except:
        raise CommandError('Unexpected error')
      else:
        hash_string = content.check_hash()
        print "%s: %s (%s)\n%s\n" % (content.id, content, content.verification_status, hash_string)