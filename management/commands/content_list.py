from django.core.management.base import NoArgsCommand, CommandError
from sitescheck.models import Content

class Command(NoArgsCommand):
  help = 'List all contents in the DB that are marked as todo, printing out ID and titles'
  
  def handle_noargs(self, **options):
    for content in Content.objects.filter(todo='yes'):
      print "%s - \"%s\" (%s)" % (content.id, content, content.verification_status)
