# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Setting.description'
        db.add_column('django_settings_setting', 'description', self.gf('django.db.models.fields.TextField')(default='', max_length=1024, blank=True), keep_default=False)

    def backwards(self, orm):
        
        # Deleting field 'Setting.description'
        db.delete_column('django_settings_setting', 'description')

    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'django_settings.integer': {
            'Meta': {'object_name': 'Integer'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'django_settings.positiveinteger': {
            'Meta': {'object_name': 'PositiveInteger'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'django_settings.setting': {
            'Meta': {'object_name': 'Setting'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'setting_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'setting_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"})
        },
        'django_settings.string': {
            'Meta': {'object_name': 'String'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['django_settings']
