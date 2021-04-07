import logging
import os
from typing import Dict

from lambdas.utils.exceptions import BadRequestException, UnauthorizedException
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

    header_params = event.get('header_params', {})
    api_key = header_params.get('x-api-key', '')
    if not api_key:
        raise UnauthorizedException('No content sent in the request.')
    body_params = event.get('body_params')
    if not body_params:
        raise BadRequestException('No content sent in the request.')
    if not isinstance(body_params, Dict) or not body_params.get('ivy_id'):
        raise BadRequestException('Please provide the User ID.')

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
