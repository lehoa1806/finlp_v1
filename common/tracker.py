from typing import Any, Dict, Optional

from aws_apis.dynamodb.database import Database


class Tracker:
    def __init__(self, database: Database) -> None:
        self.table = database.get_tracking_table()
        self.pkey = 'track_id'
        self.skey = 'track_type'

    @property
    def tracker(self):
        raise NotImplementedError

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        return self.table.get_item(
            partition_key=key,
            sort_key=self.tracker,
        )

    def save(self, data: Dict) -> None:
        if self.pkey not in data:
            raise ValueError('Track ID needs to be specified')
        data.update({self.skey: self.tracker})
        self.table.put_item(data)
