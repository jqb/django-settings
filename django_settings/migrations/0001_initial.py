# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'String'
        db.create_table('django_settings_string', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=254)),
        ))
        db.send_create_signal('django_settings', ['String'])

        # Adding model 'Integer'
        db.create_table('django_settings_integer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('django_settings', ['Integer'])

        # Adding model 'PositiveInteger'
        db.create_table('django_settings_positiveinteger', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('django_settings', ['PositiveInteger'])

        # Adding model 'Setting'
        db.create_table('django_settings_setting', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('setting_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('setting_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('django_settings', ['Setting'])


    def backwards(self, orm):
        
        # Deleting model 'String'
        db.delete_table('django_settings_string')

        # Deleting model 'Integer'
        db.delete_table('django_settings_integer')

        # Deleting model 'PositiveInteger'
        db.delete_table('django_settings_positiveinteger')

        # Deleting model 'Setting'
        db.delete_table('django_settings_setting')


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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'setting_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'setting_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"})
        },
        'django_settings.string': {
            'Meta': {'object_name': 'String'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '254'})
        }
    }

    complete_apps = ['django_settings']
