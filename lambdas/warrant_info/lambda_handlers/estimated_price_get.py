import logging
import os

from lambdas.utils.exceptions import UnauthorizedException
from postgresql.database import Database

logger = logging.getLogger()
logger.setLevel(logging.INFO)

QUERY = """\
SELECT
  "name",
  MAX("price")
FROM
  "vietnam_estimated_prices"
GROUP BY "name";\
"""


def lambda_handler(event, context):
    logger.info('Requested event: {}'.format(event))

    aws_identity = event.get('apigw_context', {}).get('identity', {})
    user_arn = aws_identity.get('userArn', '')
    arn_parts = user_arn.split('user/') if 'arn:aws:iam' in user_arn else []
    user = arn_parts[1] if len(arn_parts) == 2 else ''
    if not user:
        raise UnauthorizedException('Invalid AWS credentials !.')

    credentials = {
        'host': os.getenv('POSTGRESQL_HOST'),
        'user': os.getenv('POSTGRESQL_USER'),
        'password': os.getenv('POSTGRESQL_PASSWD'),
        'dbname': os.getenv('POSTGRESQL_DB'),
        'port': int(os.getenv('POSTGRESQL_PORT')),
    }
    database = Database.load_database(config=credentials)
    keys = ('name', 'price')
    data = {}
    for item in database.query(QUERY, keys):
        data.update({item['name']: item['price']})
    return {'prices': data}
