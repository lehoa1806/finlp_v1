import logging
import os
from typing import Dict

from apis.utils.exceptions import BadRequestException, UnauthorizedException
from postgresql.database import Database

logger = logging.getLogger()
logger.setLevel(logging.INFO)

INSERT_QUERY = """\
INSERT INTO "users_history" (
  "date", "user", "recordId", "warrant", "action", "quantity", "price",
  "acquisitionPrice", "realizedLossProfit", "editable"
)
VALUES {values_to_insert}
ON CONFLICT ("user", "recordId")
DO UPDATE SET "warrant" = EXCLUDED."warrant",
 "action" = EXCLUDED."action",
 "quantity" = EXCLUDED."quantity",
 "price" = EXCLUDED."price",
 "acquisitionPrice" = EXCLUDED."acquisitionPrice",
 "realizedLossProfit" = EXCLUDED."realizedLossProfit",
 "editable" = EXCLUDED."editable"
;\
"""
DELETE_QUERY = """\
DELETE FROM "users_history"
WHERE "user" = '{user}' AND "recordId" = '{record_id}';\
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
    if not body_params:
        raise BadRequestException('No data in the request.')
    if not isinstance(body_params, Dict) or not body_params.get('records'):
        raise BadRequestException('No valid data in the request.')

    records = body_params.get('records')
    '''
    {'action': 'insert', 'record': {...}}
    {'action': 'delete', 'record': {...}}
    '''
    action = records.get('action')
    record = records.get('record')
    credentials = {
        'host': os.getenv('POSTGRESQL_HOST'),
        'user': os.getenv('POSTGRESQL_USER'),
        'password': os.getenv('POSTGRESQL_PASSWD'),
        'dbname': os.getenv('POSTGRESQL_DB'),
        'port': int(os.getenv('POSTGRESQL_PORT')),
    }
    database = Database.load_database(config=credentials)
    if action == 'insert':
        with database.connection.psycopg2_client.cursor() as cursor:
            values_to_insert = cursor.mogrify(
                    '(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    [record.get('date'),
                     user,
                     record.get('recordId'),
                     record.get('warrant'),
                     record.get('action'),
                     record.get('quantity'),
                     record.get('price'),
                     record.get('acquisitionPrice'),
                     record.get('realizedLossProfit'),
                     record.get('editable', True)]).decode('utf-8')
        logging.info(
            f'Inserting data to to users_history.')
        command = INSERT_QUERY.format(values_to_insert=values_to_insert)
        database.connection.execute(command)
    elif action == 'delete':
        record_id = record.get('recordId', 'Unknown')
        command = DELETE_QUERY.format(user=user, record_id=record_id)
        database.connection.execute(command)

    return {
        'statusCode': 200,
        'body': 'Success.',
    }
