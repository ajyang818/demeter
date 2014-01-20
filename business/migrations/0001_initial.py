# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Neighborhood'
        db.create_table(u'business_neighborhood', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=2)),
        ))
        db.send_create_signal(u'business', ['Neighborhood'])

        # Adding model 'Category'
        db.create_table(u'business_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'business', ['Category'])

        # Adding model 'Business'
        db.create_table(u'business_business', (
            ('business_yelp_slug', self.gf('django.db.models.fields.CharField')(max_length=100, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('is_closed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('review_count', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('display_stars', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=2, decimal_places=1, blank=True)),
            ('elite_count', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('elite_stars', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=4, blank=True)),
            ('last_harvested', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'business', ['Business'])

        # Adding M2M table for field category on 'Business'
        m2m_table_name = db.shorten_name(u'business_business_category')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('business', models.ForeignKey(orm[u'business.business'], null=False)),
            ('category', models.ForeignKey(orm[u'business.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['business_id', 'category_id'])

        # Adding M2M table for field neighborhood on 'Business'
        m2m_table_name = db.shorten_name(u'business_business_neighborhood')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('business', models.ForeignKey(orm[u'business.business'], null=False)),
            ('neighborhood', models.ForeignKey(orm[u'business.neighborhood'], null=False))
        ))
        db.create_unique(m2m_table_name, ['business_id', 'neighborhood_id'])


    def backwards(self, orm):
        # Deleting model 'Neighborhood'
        db.delete_table(u'business_neighborhood')

        # Deleting model 'Category'
        db.delete_table(u'business_category')

        # Deleting model 'Business'
        db.delete_table(u'business_business')

        # Removing M2M table for field category on 'Business'
        db.delete_table(db.shorten_name(u'business_business_category'))

        # Removing M2M table for field neighborhood on 'Business'
        db.delete_table(db.shorten_name(u'business_business_neighborhood'))


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
        }
    }

    complete_apps = ['business']