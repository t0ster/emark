# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Semester'
        db.create_table('core_semester', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('core', ['Semester'])

        # Adding model 'Group'
        db.create_table('core_group', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('core', ['Group'])

        # Adding model 'Subject'
        db.create_table('core_subject', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Group'])),
            ('semester', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Semester'])),
            ('start_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('per2weeks', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('core', ['Subject'])

        # Adding model 'Lesson'
        db.create_table('core_lesson', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Subject'])),
            ('start_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('canceled', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('core', ['Lesson'])


    def backwards(self, orm):
        
        # Deleting model 'Semester'
        db.delete_table('core_semester')

        # Deleting model 'Group'
        db.delete_table('core_group')

        # Deleting model 'Subject'
        db.delete_table('core_subject')

        # Deleting model 'Lesson'
        db.delete_table('core_lesson')


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
            'start_date': ('django.db.models.fields.DateField', [], {})
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
