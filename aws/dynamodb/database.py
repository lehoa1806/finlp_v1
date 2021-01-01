from typing import Any, Dict, Optional

import boto3
from botocore.config import Config

from common.common import AWS_REGION

from .table import Table


class Database:
    """
    The Class to manage all DynamoDB tables.
    """
    def __init__(
        self,
        boto_client: Any,
    ) -> None:
        self.dynamodb = boto_client

    @property
    def tables(self):
        self.dynamodb.get_tables()

    def load_table(
        self,
        table_name: str,
    ) -> Table:
        return Table(self.dynamodb.Table(table_name))

    @classmethod
    def load_database(
        cls,
        max_pool_connections: Optional[int] = None,
    ) -> 'Database':
        kwargs: Dict[str, Any] = {'region_name': AWS_REGION}
        if max_pool_connections:
            # Fix "Connection pool is full, discarding connection:
            # dynamodb.us-west-2.amazonaws.com" issue
            config = Config(user_agent_extra='Resource',
                            max_pool_connections=max_pool_connections)
            kwargs['config'] = config
        dynamo_client = boto3.resource('dynamodb', **kwargs)
        return Database(boto_client=dynamo_client)

    # Load table:
    def load_configuration_table(self) -> Table:
        return self.load_table(table_name='global_configuration')
