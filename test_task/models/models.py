from ..config.db import DATABASES
from orator import DatabaseManager, Model
from orator.orm import belongs_to_many

db = DatabaseManager(DATABASES)
Model.set_connection_resolver(db)


class Tag(Model):
    __timestamps__ = False
    __fillable__ = ['name']


class Video(Model):
    __timestamps__ = False
    __fillable__ = ['url', 'title', 'video_url', 'preview_url', 'categories', 'views', 'added_by', 'added_at']

    @belongs_to_many
    def tags(self):
        return Tag


class VideoTag(Model):
    __timestamps__ = False
    __fillable__ = ['video_id', 'tag_id']
