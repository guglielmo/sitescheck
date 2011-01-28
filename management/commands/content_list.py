from django.core.management.base import NoArgsCommand, CommandError
from sitescheck.models import Content

class Command(NoArgsCommand):
  help = 'List all contents in the DB, printing out ID and titles'
  
  def handle_noargs(self, **options):
    for content in Content.objects.all():
      print "%s - \"%s\" (%s)" % (content.id, content, content.verification_status)
