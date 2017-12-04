from orator.migrations import Migration


class CreateVideosTable(Migration):

    def up(self):
        with self.schema.create('videos') as table:
            table.increments('id')
            table.string('url')
            table.string('title')
            table.string('video_url').nullable()
            table.string('preview_url').nullable()
            table.string('categories').nullable()
            table.string('views')
            table.string('added_by')
            table.timestamp('added_at')

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('videos')
