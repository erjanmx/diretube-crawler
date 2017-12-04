from orator.migrations import Migration


class CreateVideoTagsTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('tags_videos') as table:
            table.increments('id')
            table.integer('video_id')
            table.integer('tag_id')


    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('tags_videos')
