# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Content'
        db.create_table('sitescheck_content', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('xpath', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('regexp', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('hashed', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('verified_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('verification_status', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('verification_error', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
        ))
        db.send_create_signal('sitescheck', ['Content'])

        # Adding model 'Recipient'
        db.create_table('sitescheck_recipient', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=75)),
        ))
        db.send_create_signal('sitescheck', ['Recipient'])


    def backwards(self, orm):
        
        # Deleting model 'Content'
        db.delete_table('sitescheck_content')

        # Deleting model 'Recipient'
        db.delete_table('sitescheck_recipient')


    models = {
        'sitescheck.content': {
            'Meta': {'object_name': 'Content'},
            'hashed': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'regexp': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
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
