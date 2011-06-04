# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Semester.starts_from_1st_week'
        db.add_column('core_semester', 'starts_from_1st_week', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Semester.starts_from_1st_week'
        db.delete_column('core_semester', 'starts_from_1st_week')


    models = {
        'core.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'core.lesson': {
            'Meta': {'ordering': "['start_datetime']", 'object_name': 'Lesson'},
            'canceled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Subject']"})
        },
        'core.semester': {
            'Meta': {'object_name': 'Semester'},
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'starts_from_1st_week': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'core.subject': {
            'Meta': {'ordering': "['start_datetime']", 'object_name': 'Subject'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'per2weeks': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'semester': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Semester']"}),
            'start_datetime': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['core']
