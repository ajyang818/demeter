# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Yelper'
        db.create_table(u'yelper_yelper', (
            ('yelp_id', self.gf('django.db.models.fields.CharField')(max_length=40, primary_key=True)),
            ('display_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('yelping_since', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('last_harvest', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('reviews', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('elite', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'yelper', ['Yelper'])


    def backwards(self, orm):
        # Deleting model 'Yelper'
        db.delete_table(u'yelper_yelper')


    models = {
        u'yelper.yelper': {
            'Meta': {'object_name': 'Yelper'},
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'elite': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'last_harvest': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'reviews': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'yelp_id': ('django.db.models.fields.CharField', [], {'max_length': '40', 'primary_key': 'True'}),
            'yelping_since': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        }
    }

    complete_apps = ['yelper']