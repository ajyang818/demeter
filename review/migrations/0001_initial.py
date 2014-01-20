# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Review'
        db.create_table(u'review_review', (
            ('review_yelp_id', self.gf('django.db.models.fields.CharField')(max_length=40, primary_key=True)),
            ('yelper', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['yelper.Yelper'])),
            ('business', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['business.Business'])),
            ('publish_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('harvest_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('stars', self.gf('django.db.models.fields.DecimalField')(max_digits=2, decimal_places=1)),
            ('review_text', self.gf('django.db.models.fields.CharField')(max_length=5250)),
            ('rotd', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('updated_review', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'review', ['Review'])


    def backwards(self, orm):
        # Deleting model 'Review'
        db.delete_table(u'review_review')


    models = {
        u'business.business': {
            'Meta': {'object_name': 'Business'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'business_yelp_slug': ('django.db.models.fields.CharField', [], {'max_length': '100', 'primary_key': 'True'}),
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['business.Category']", 'symmetrical': 'False'}),
            'display_stars': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '2', 'decimal_places': '1', 'blank': 'True'}),
            'elite_count': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'elite_stars': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '4', 'blank': 'True'}),
            'is_closed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_harvested': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'neighborhood': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['business.Neighborhood']", 'symmetrical': 'False'}),
            'phone': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'review_count': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'business.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'business.neighborhood': {
            'Meta': {'object_name': 'Neighborhood'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        u'review.review': {
            'Meta': {'object_name': 'Review'},
            'business': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['business.Business']"}),
            'harvest_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {}),
            'review_text': ('django.db.models.fields.CharField', [], {'max_length': '5250'}),
            'review_yelp_id': ('django.db.models.fields.CharField', [], {'max_length': '40', 'primary_key': 'True'}),
            'rotd': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'stars': ('django.db.models.fields.DecimalField', [], {'max_digits': '2', 'decimal_places': '1'}),
            'updated_review': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'yelper': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['yelper.Yelper']"})
        },
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

    complete_apps = ['review']