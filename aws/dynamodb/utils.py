from enum import Enum

from boto3.dynamodb import conditions


class KeyType(Enum):
    Attr: str = 'Attr'
    Key: str = 'Key'


CONDITION_TYPE = {
    'Attr': conditions.Attr,
    'Key': conditions.Key,
}
