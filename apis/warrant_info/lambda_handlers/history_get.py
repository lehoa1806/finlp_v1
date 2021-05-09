import logging
import os

from apis.utils.exceptions import UnauthorizedException
from utils.postgresql import Database

logger = logging.getLogger()
logger.setLevel(logging.INFO)

QUERY = """\
SELECT
  TO_CHAR(t1."date", 'YYYY-MM-DD') AS "date",
  t1."user" AS "user",
  t1."recordId" AS "recordId",
  t1."warrant" AS "warrant",
  t1."action" AS "action",
  t1."quantity" AS "quantity",
  t1."price" AS "price",
  t1."acquisitionPrice" AS "acquisitionPrice",
  t1."realizedLossProfit" AS "realizedLossProfit",
  t1."editable" AS "editable"
FROM
  "users_history" AS t1
WHERE
  t1."user" = '{user}'\
"""


def lambda_handler(event, context):
    logger.info('Requested event: {}'.format(event))

    aws_identity = event.get('apigw_context', {}).get('identity', {})
    user_arn = aws_identity.get('userArn', '')
    arn_parts = user_arn.split('user/') if 'arn:aws:iam' in user_arn else []
    user = arn_parts[1] if len(arn_parts) == 2 else ''
    if not user:
        raise UnauthorizedException('Invalid AWS credentials !.')
    body_params = event.get('body_params')
    start_time = body_params.get('start_time')
    end_time = body_params.get('end_time')
    credentials = {
        'host': os.getenv('POSTGRESQL_HOST'),
        'user': os.getenv('POSTGRESQL_USER'),
        'password': os.getenv('POSTGRESQL_PASSWD'),
        'dbname': os.getenv('POSTGRESQL_DB'),
        'port': int(os.getenv('POSTGRESQL_PORT')),
    }
    database = Database.load_database(config=credentials)

    # History
    keys = ('date', 'user', 'recordId', 'warrant', 'action', 'quantity', 'price',
            'acquisitionPrice', 'realizedLossProfit', 'editable')
    query = QUERY.format(user=user)
    if start_time:
        query += f' AND t1."date" > \'{start_time}\''
        if end_time:
            query += f' AND t1."date" < \'{end_time}\''
    else:
        query += f' AND t1."date" > CURRENT_DATE - INTERVAL \'3 months\''
    query += ';'
    records = list(database.query(query, keys))
    return {'records': records}
