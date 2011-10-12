import difflib
from django.shortcuts import render_to_response
from sitescheck.models import *

def diff(request, content_id):
    content = Content.objects.get(pk=content_id)
    live = content.get_live_meat().splitlines(1)
    stored = content.meat.splitlines(1)
    diff = difflib.HtmlDiff().make_table(stored, live, context=True, numlines=2)    
    return render_to_response("diff.html", { 'content': content, 'diff': diff } )
