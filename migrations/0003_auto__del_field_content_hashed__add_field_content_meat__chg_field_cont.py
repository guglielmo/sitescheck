# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Content.hashed'
        db.delete_column('sitescheck_content', 'hashed')

        # Adding field 'Content.meat'
        db.add_column('sitescheck_content', 'meat', self.gf('django.db.models.fields.TextField')(default='', blank=True), keep_default=False)

        # Changing field 'Content.todo'
        db.alter_column('sitescheck_content', 'todo', self.gf('django.db.models.fields.CharField')(max_length=3))


    def backwards(self, orm):
        
        # Adding field 'Content.hashed'
        db.add_column('sitescheck_content', 'hashed', self.gf('django.db.models.fields.CharField')(default='', max_length=128, blank=True), keep_default=False)

        # Deleting field 'Content.meat'
        db.delete_column('sitescheck_content', 'meat')

        # Changing field 'Content.todo'
        db.alter_column('sitescheck_content', 'todo', self.gf('django.db.models.fields.CharField')(max_length=2))


    models = {
        'sitescheck.content': {
            'Meta': {'object_name': 'Content'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meat': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'regexp': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'todo': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
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
