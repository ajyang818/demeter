# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Business.display_stars'
        db.delete_column(u'business_business', 'display_stars')

        # Adding field 'Business.stars'
        db.add_column(u'business_business', 'stars',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=2, decimal_places=1, blank=True),
                      keep_default=False)


        # Changing field 'Business.business_yelp_slug'
        db.alter_column(u'business_business', 'business_yelp_slug', self.gf('django.db.models.fields.SlugField')(max_length=100, primary_key=True))
        # Adding index on 'Business', fields ['business_yelp_slug']
        db.create_index(u'business_business', ['business_yelp_slug'])

        # Deleting field 'Category.id'
        db.delete_column(u'business_category', u'id')

        # Adding field 'Category.slug'
        db.add_column(u'business_category', 'slug',
                      self.gf('django.db.models.fields.SlugField')(default='temp-slug', max_length=200, primary_key=True),
                      keep_default=False)

        # Adding field 'Category.parent'
        db.add_column(u'business_category', 'parent',
                      self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['business.Category']),
                      keep_default=False)

        # Adding field 'Category.lft'
        db.add_column(u'business_category', u'lft',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=1, db_index=True),
                      keep_default=False)

        # Adding field 'Category.rght'
        db.add_column(u'business_category', u'rght',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=1, db_index=True),
                      keep_default=False)

        # Adding field 'Category.tree_id'
        db.add_column(u'business_category', u'tree_id',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=1, db_index=True),
                      keep_default=False)

        # Adding field 'Category.level'
        db.add_column(u'business_category', u'level',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=1, db_index=True),
                      keep_default=False)


        # Changing field 'Category.name'
        db.alter_column(u'business_category', 'name', self.gf('django.db.models.fields.CharField')(max_length=200))

    def backwards(self, orm):
        # Removing index on 'Business', fields ['business_yelp_slug']
        db.delete_index(u'business_business', ['business_yelp_slug'])

        # Adding field 'Business.display_stars'
        db.add_column(u'business_business', 'display_stars',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=2, decimal_places=1, blank=True),
                      keep_default=False)

        # Deleting field 'Business.stars'
        db.delete_column(u'business_business', 'stars')


        # Changing field 'Business.business_yelp_slug'
        db.alter_column(u'business_business', 'business_yelp_slug', self.gf('django.db.models.fields.CharField')(max_length=100, primary_key=True))
        # Adding field 'Category.id'
        db.add_column(u'business_category', u'id',
                      self.gf('django.db.models.fields.AutoField')(default=1, primary_key=True),
                      keep_default=False)

        # Deleting field 'Category.slug'
        db.delete_column(u'business_category', 'slug')

        # Deleting field 'Category.parent'
        db.delete_column(u'business_category', 'parent_id')

        # Deleting field 'Category.lft'
        db.delete_column(u'business_category', u'lft')

        # Deleting field 'Category.rght'
        db.delete_column(u'business_category', u'rght')

        # Deleting field 'Category.tree_id'
        db.delete_column(u'business_category', u'tree_id')

        # Deleting field 'Category.level'
        db.delete_column(u'business_category', u'level')


        # Changing field 'Category.name'
        db.alter_column(u'business_category', 'name', self.gf('django.db.models.fields.CharField')(max_length=100))

    models = {
        u'business.business': {
            'Meta': {'object_name': 'Business'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'business_yelp_slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'primary_key': 'True'}),
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['business.Category']", 'symmetrical': 'False'}),
            'elite_count': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'elite_stars': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '4', 'blank': 'True'}),
            'is_closed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_harvested': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'neighborhood': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['business.Neighborhood']", 'symmetrical': 'False'}),
            'phone': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'review_count': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'stars': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '2', 'decimal_places': '1', 'blank': 'True'})
        },
        u'business.category': {
            'Meta': {'object_name': 'Category'},
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['business.Category']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '200', 'primary_key': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
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