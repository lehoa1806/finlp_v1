import logging
import os

from lambdas.utils.exceptions import UnauthorizedException
from postgresql.database import Database

logger = logging.getLogger()
logger.setLevel(logging.INFO)

QUERY = """\
SELECT
  "warrant",
  "provider",
  "expired_date",
  "volume",
  "price",
  "share_price",
  "exercise_price",
  "exercise_ratio",
  "foreign_buy"
FROM
  (
    SELECT
      *
    FROM
      "vietnam_warrants"
    WHERE
      "datetime" > current_date + INTERVAL '-1 day'
  ) AS t1
  INNER JOIN (
    SELECT
      "warrant",
      MAX("datetime") AS "datetime"
    FROM
      "vietnam_warrants"
    WHERE
      "datetime" > current_date + INTERVAL '-1 day'
    GROUP BY
      "warrant"
  ) AS t2
    USING (
    "warrant",
    "datetime"
  ) ;\
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
        'username': os.getenv('POSTGRESQL_USER'),
        'password': os.getenv('POSTGRESQL_PASSWD'),
        'dbname': os.getenv('POSTGRESQL_DB'),
        'port': int(os.getenv('POSTGRESQL_PORT')),
    }
    database = Database.load_database(config=credentials)
    keys = ('warrant', 'provider', 'expired_date', 'volume', 'price', 'share_price', 'exercise_price', 'exercise_ratio',
            'foreign_buy')
    data = next(database.query(QUERY, keys), {})
    return data
