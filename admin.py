from django.contrib import admin
from sitescheck.models import Content, Recipient

class ContentAdmin(admin.ModelAdmin):    
  list_display = ('title', 'verified_at', 'verification_status')
  search_fields = ('title', 'notes' )
  list_filter = ('verification_status', )
  fieldsets = (
    (None, { 
      'fields': ('title', 'notes', 'url', 'xpath', 'regexp', 'hashed') 
    }),
    ('Verification', {
      'fields': ('verified_at', 'verification_status', 'verification_error')
    })
  )
  readonly_fields = ('hashed', 'verified_at', 'verification_status', 'verification_error')
admin.site.register(Content, ContentAdmin)
admin.site.register(Recipient)
