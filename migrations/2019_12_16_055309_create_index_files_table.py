from orator.migrations import Migration

class CreateIndexFilesTable(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('index_files') as table:
            table.big_increments('id')
            table.string('filename')
            table.string('scnl')
            table.date('date')
            table.float('sample_rate').default(0.0)
            table.float('min_amplitude').default(0.0)
            table.float('max_amplitude').default(0.0)
            table.float('availability').default(0.0)
            table.unique(['scnl','date'])
            table.index('date')
            table.index('scnl')
            table.nullable_timestamps()

    def down(self):
        self.schema.drop_if_exists('index_files')
        pass
