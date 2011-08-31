# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Content.todo'
        db.add_column('sitescheck_content', 'todo', self.gf('django.db.models.fields.CharField')(default='si', max_length=2), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Content.todo'
        db.delete_column('sitescheck_content', 'todo')


    models = {
        'sitescheck.content': {
            'Meta': {'object_name': 'Content'},
            'hashed': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'regexp': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'todo': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'verification_error': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'verification_status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'verified_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'xpath': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'})
        },
        'sitescheck.recipient': {
            'Meta': {'object_name': 'Recipient'},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        }
    }

    complete_apps = ['sitescheck']
