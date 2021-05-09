from aws_wrappers.dynamodb.database import Database as DynamoDB
from aws_wrappers.dynamodb.table import Table


class Database(DynamoDB):
    # Load table:
    def load_configuration_table(self) -> Table:
        return self.load_table(table_name='global_configuration')

    def get_tracking_table(self) -> Table:
        return self.load_table(table_name='global_tracking')
