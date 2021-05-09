import logging
import os
from typing import Dict

from apis.utils.exceptions import BadRequestException, UnauthorizedException
from utils.postgresql.database import Database

logger = logging.getLogger()
logger.setLevel(logging.INFO)


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
    if not isinstance(body_params, Dict) or not body_params.get('prices'):
        raise BadRequestException('No valid data in the request.')

    prices = body_params.get('prices')

    credentials = {
        'host': os.getenv('POSTGRESQL_HOST'),
        'user': os.getenv('POSTGRESQL_USER'),
        'password': os.getenv('POSTGRESQL_PASSWD'),
        'dbname': os.getenv('POSTGRESQL_DB'),
        'port': int(os.getenv('POSTGRESQL_PORT')),
    }
    database = Database.load_database(config=credentials)
    with database.connection.psycopg2_client.cursor() as cursor:
        values_to_insert = ', '.join(
            cursor.mogrify('(%s, %s)', [name, price]).decode('utf-8')
            for name, price in prices.items()
        )
    logging.info(
        f'Inserting {len(prices)} records to vietnam_estimated_prices.')
    command = (
        f'INSERT INTO "vietnam_estimated_prices" ("name", "price") '
        f'VALUES {values_to_insert} ON CONFLICT ("name")'
        f'DO UPDATE SET price = EXCLUDED.price'
    )
    database.connection.execute(command)
    return {
        'statusCode': 200,
        'body': 'Success.',
    }
