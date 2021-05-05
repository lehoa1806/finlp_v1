import logging
import os
from datetime import datetime

from apis.utils.exceptions import UnauthorizedException
from postgresql.database import Database

logger = logging.getLogger()
logger.setLevel(logging.INFO)

CREATE_TEMP_QUERY = """\
CREATE TEMP TABLE "vietnam_warrants_snapshot_staging_{timestamp}" AS
SELECT
  t1."warrant" AS "warrant",
  t1."provider" AS "provider",
  t1."expiredDate" AS "expiredDate",
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
      "datetime" > current_date + INTERVAL '-4 hours'
  ) AS t1
  INNER JOIN (
    SELECT
      "warrant",
      MAX("datetime") AS "datetime"
    FROM
      "vietnam_warrants"
    WHERE
      "datetime" > current_date + INTERVAL '-4 hours'
    GROUP BY
      "warrant"
  ) AS t2
    USING (
    "warrant",
    "datetime"
  );\
"""
INSERT_TEMP_QUERY = """\
INSERT INTO "vietnam_warrants_snapshot_staging_{timestamp}"
SELECT
  *
FROM
  "vietnam_warrants_snapshot" AS t1
WHERE
  NOT EXISTS (
    SELECT
      1
    FROM
      "vietnam_warrants_snapshot_staging_{timestamp}"
    WHERE
      warrant = t1.warrant
  );\
"""
TRUNCATE_SNAPSHOT_QUERY = """\
TRUNCATE TABLE "vietnam_warrants_snapshot";\
"""
INSERT_SNAPSHOT_QUERY = """\
INSERT INTO "vietnam_warrants_snapshot"
SELECT * FROM "vietnam_warrants_snapshot_staging_{timestamp}";\
"""
DROP_TEMP_QUERY = """\
DROP TABLE "vietnam_warrants_snapshot_staging_{timestamp}";\
"""
SELECT_DATA_QUERY = """\
SELECT * FROM "vietnam_warrants_snapshot";\
"""
QUERY = """\
SELECT
  t1."warrant" AS "warrant",
  t1."provider" AS "provider",
  TO_CHAR(t1."expiredDate", 'YYYY-MM-DD') AS "expiredDate",
  t1."exercisePrice" AS "exercisePrice",
  t1."exerciseRatio" AS "exerciseRatio",
  t1."referencePrice" AS "referencePrice",
  t1."volume" AS "volume",
  t1."price" AS "price",
  t1."sharePrice" AS "sharePrice",
  t1."foreignBuy" AS "foreignBuy",
  t2."price" AS "estimatedSharePrice"
FROM
  ( SELECT * FROM "vietnam_warrants_snapshot" ) AS t1
  LEFT JOIN "vietnam_estimated_prices" AS t2 ON t1."warrant" = t2."name"
ORDER BY t1."warrant";\
"""


def lambda_handler(event, context):
    logger.info('Requested event: {}'.format(event))

    aws_identity = event.get('apigw_context', {}).get('identity', {})
    user_arn = aws_identity.get('userArn', '')
    arn_parts = user_arn.split('user/') if 'arn:aws:iam' in user_arn else []
    user = arn_parts[1] if len(arn_parts) == 2 else ''
    if not user:
        raise UnauthorizedException('Invalid AWS credentials !.')

    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
    credentials = {
        'host': os.getenv('POSTGRESQL_HOST'),
        'user': os.getenv('POSTGRESQL_USER'),
        'password': os.getenv('POSTGRESQL_PASSWD'),
        'dbname': os.getenv('POSTGRESQL_DB'),
        'port': int(os.getenv('POSTGRESQL_PORT')),
    }
    database = Database.load_database(config=credentials)
    database.execute(CREATE_TEMP_QUERY.format(timestamp=timestamp))
    database.execute(INSERT_TEMP_QUERY.format(timestamp=timestamp))
    database.execute(TRUNCATE_SNAPSHOT_QUERY)
    database.execute(INSERT_SNAPSHOT_QUERY.format(timestamp=timestamp))

    keys = ('warrant', 'provider', 'expirationDate', 'exercisePrice', 'exerciseRatio', 'referencePrice',
            'volume', 'price', 'sharePrice', 'foreignBuy', 'estimatedSharePrice')
    data = {}
    for item in database.query(QUERY, keys):
        data.update({item.get('warrant', 'Unknown'): item})
    return {'warrants': data}
