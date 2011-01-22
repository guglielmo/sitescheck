from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from sitescheck.models import Content

class Command(BaseCommand):
  args = '<id> <id>'
  help = 'Verify specified content'
  
  def handle(self, *args, **options):
    if len(args) == 0:
      for content in Content.objects.all():
        content.verify()
        print "%s: %s (%s)" % (content.id, content, content.verification_status)
    else:
      for content_id in args:
        try:
          content = Content.objects.get(pk=int(content_id))
        except Content.DoesNotExist:
          print '%s: content does not exist!\n' % content_id
        except:
          raise CommandError('Unexpected error')
        else:
          content.verify()
          print "%s: %s (%s)" % (content.id, content, content.verification_status)
        