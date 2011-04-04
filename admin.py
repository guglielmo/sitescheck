from django.contrib import admin
from sitescheck.models import Content, Recipient



class ContentAdmin(admin.ModelAdmin):    
  list_display = ('_linked_title', 'verified_at', '_status_and_message')
  search_fields = ('title', 'notes' )
  list_filter = ('verification_status', )
  fieldsets = (
    (None, { 
      'fields': ('title', 'notes', 'url', 'xpath', 'regexp', 'hashed'),
      'classes': ['wide', 'extrapretty']
    }),
    ('Verification', {
      'fields': ('verified_at', 'verification_status', 'verification_error')
    })
  )
  readonly_fields = ('hashed', 'verified_at', 'verification_status', 'verification_error')
  
  def _linked_title(self, obj):
    return '%s <a href="%s" target="_blank"><img src="/images/extlink.gif" alt="vai" title="vai alla url: %s"</a>' % (obj.title, obj.url, obj.url)
  _linked_title.allow_tags = True
  _linked_title.short_description = 'Identificativo della URL (con link)'
  
  def _status_and_message(self, obj):
    status = obj.verification_status
    if obj.verification_status == 0:
      msg = "IMMUTATO"
    elif obj.verification_status == 1:
      msg = "CAMBIATO"
    else:
      msg = obj.verification_error
      
    return ("%s - %s" % (status, msg))
  _status_and_message.short_description = 'Status'
  
admin.site.register(Content, ContentAdmin)
admin.site.register(Recipient)
