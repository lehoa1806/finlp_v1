import logging
import os

from apis.utils.exceptions import UnauthorizedException
from postgresql.database import Database

logger = logging.getLogger()
logger.setLevel(logging.INFO)

QUERY = """\
SELECT
  t1."warrant" AS "warrant",
  t1."provider" AS "provider",
  TO_CHAR(t1."expiredDate", 'Mon-DD-YYYY') AS "expiredDate",
  t1."exercisePrice" AS "exercisePrice",
  t1."exerciseRatio" AS "exerciseRatio",
  t1."referencePrice" AS "referencePrice",
  t1."volume" AS "volume",
  t1."price" AS "price",
  t1."sharePrice" AS "sharePrice",
  t1."foreignBuy" AS "foreignBuy"
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
  )
ORDER BY "warrant";\
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
    keys = ('warrant', 'provider', 'expirationDate', 'exercisePrice', 'exerciseRatio', 'referencePrice',
            'volume', 'price', 'sharePrice', 'foreignBuy')
    data = list(database.query(QUERY, keys))
    return {'warrants': data}
