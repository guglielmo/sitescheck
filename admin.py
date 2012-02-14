from django.contrib import admin
from sitescheck.models import Content, Recipient

class ContentAdmin(admin.ModelAdmin):    
  list_display = ('_linked_title', 'todo', 'verified_at', '_status_and_message')
  search_fields = ('title', 'notes' )
  radio_fields = {'todo': admin.HORIZONTAL}
  list_filter = ('verification_status', 'todo' )
  fieldsets = (
    (None, { 
      'fields': ('title', 'notes', 'url', 'xpath', 'regexp', 'meat'),
      'classes': ['wide', 'extrapretty']
    }),
    ('Verification', {
      'fields': ('todo', 'verified_at', 'verification_status', 'verification_error')
    })
  )
  readonly_fields = ('meat', 'verified_at', 'verification_status', 'verification_error')
  
  def _linked_title(self, obj):
    return '%s <a href="%s" target="_blank"><img src="/images/extlink.gif" alt="vai" title="vai alla url: %s"</a>' % (obj.title, obj.url, obj.url)
  _linked_title.allow_tags = True
  _linked_title.short_description = 'Identificativo della URL'
  
  def _status_and_message(self, obj):
    status = obj.verification_status
    if obj.verification_status == 0:
      msg = "IMMUTATO"
    elif obj.verification_status == 1:
      msg = 'CAMBIATO - <a href="/diff/%s"><img src="/images/extlink.gif" alt="vai"/> visualizza le differenze</a>' % obj.id
    else:
      msg = obj.verification_error
      
    return ("%s - %s" % (status, msg))
  _status_and_message.allow_tags = True
  _status_and_message.short_description = 'Status'
  
  def update(self, request, queryset):
      for obj in queryset:
          obj.update()
  update.short_description = "Aggiorna contenuto dai siti live"
  
  def verify(self, request, queryset):
      for obj in queryset:
          obj.verify()
  verify.short_description = "Verifica differenze sui siti live"
  
  def set_todo(self, request, queryset):
      for obj in queryset:
          obj.todo = 'yes'
          obj.save()
  set_todo.short_description = "Marca il sito come da fare"
  
  def unset_todo(self, request, queryset):
      for obj in queryset:
          obj.todo = 'no'
          obj.save()
  unset_todo.short_description = "Marca il sito come non da fare"
  
  actions = [update, verify, set_todo, unset_todo]
  
admin.site.register(Content, ContentAdmin)
admin.site.register(Recipient)
