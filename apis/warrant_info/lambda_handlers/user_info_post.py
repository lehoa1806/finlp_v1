import json
import logging
import os
from typing import Dict

from apis.utils.exceptions import BadRequestException, UnauthorizedException
from postgresql.database import Database

logger = logging.getLogger()
logger.setLevel(logging.INFO)

WATCHLISTS_QUERY = """\
INSERT INTO "users_watchlists" ("user", "watchlist", "warrants")
VALUES {values_to_insert}
ON CONFLICT ("user", "watchlist")
DO UPDATE SET "warrants" = EXCLUDED."warrants";\
"""
WATCHLISTS_UPDATE = """\
UPDATE "users_watchlists"
SET ("watchlist", "warrants") = {values_to_update}
WHERE ("user", "watchlist") = {conditions};\
"""

PORTFOLIO_QUERY = """\
INSERT INTO "users_portfolio" ("user", "warrant", "quantity", "acquisitionPrice")
VALUES {values_to_insert}
ON CONFLICT ("user", "warrant")
DO UPDATE SET "quantity" = EXCLUDED."quantity", "acquisitionPrice" = EXCLUDED."acquisitionPrice";\
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
    if not isinstance(body_params, Dict) or not (
        body_params.get('watchlist') or body_params.get('portfolio')
    ):
        raise BadRequestException('No valid data in the request.')

    watchlist = body_params.get('watchlist')
    '''
    {
        'data': {
            name: WATCHLIST1,
            warrants: ['WARRANT1', 'WARRANT2'],
            newName: WATCHLIST2,
        },
        'action': 'insert'  // 'update', 'delete'
    }
    '''
    portfolio = body_params.get('portfolio')
    '''
    {
        'data': {
            warrant: 'WARRANT0',
            quantity: 100,
            acquisitionPrice: 9999,
        }
        'action': 'insert'  // 'update', 'delete'
    }
    '''

    credentials = {
        'host': os.getenv('POSTGRESQL_HOST'),
        'user': os.getenv('POSTGRESQL_USER'),
        'password': os.getenv('POSTGRESQL_PASSWD'),
        'dbname': os.getenv('POSTGRESQL_DB'),
        'port': int(os.getenv('POSTGRESQL_PORT')),
    }
    database = Database.load_database(config=credentials)
    if watchlist and isinstance(watchlist, dict):
        action = watchlist.get('action')
        data = watchlist.get('data', {})
        name = data.get('name')
        if name and action == 'insert':
            with database.connection.psycopg2_client.cursor() as cursor:
                values_to_insert = cursor.mogrify(
                    '(%s, %s, %s)',
                    [user, name, json.dumps(data.get('warrants'))]
                ).decode('utf-8')
            command = WATCHLISTS_QUERY.format(values_to_insert=values_to_insert)
            database.connection.execute(command)
            logging.info(f'Inserted {name} to users_watchlists.')

        elif name and action == 'update':
            new_name = data.get('newName')
            if new_name and name != new_name:
                with database.connection.psycopg2_client.cursor() as cursor:
                    values_to_update = cursor.mogrify(
                        '(%s, %s)', [new_name, json.dumps(data.get('warrants'))]).decode('utf-8')
                    conditions = cursor.mogrify('(%s, %s)', [user, name]).decode('utf-8')
                command = WATCHLISTS_UPDATE.format(values_to_update=values_to_update, conditions=conditions)
                database.connection.execute(command)
                logging.info(f'Updated {name} in users_watchlists.')
        elif name and action == 'delete':
            command = f'DELETE FROM users_watchlists WHERE ("user", "watchlist") = (\'{user}\', \'{name}\')'
            database.connection.execute(command)
            logging.info(f'Deleted {name} from users_watchlists.')
    if portfolio and isinstance(portfolio, dict):
        action = portfolio.get('action')
        data = portfolio.get('data', {})
        warrant = data.get('warrant')
        if warrant and action == 'insert':
            with database.connection.psycopg2_client.cursor() as cursor:
                values_to_insert = cursor.mogrify(
                        '(%s, %s, %s, %s)',
                        [user, warrant, data.get('quantity'),
                         data.get('acquisitionPrice')]).decode('utf-8')
            command = PORTFOLIO_QUERY.format(values_to_insert=values_to_insert)
            database.connection.execute(command)
            logging.info(f'Inserting {warrant} to to users_portfolio.')
        elif warrant and action == 'delete':
            command = f'DELETE FROM users_portfolio WHERE ("user", "warrant") = (\'{user}\', \'{warrant}\')'
            database.connection.execute(command)
            logging.info(f'Deleted {warrant} from users_portfolio.')

    return {
        'statusCode': 200,
        'body': 'Success.',
    }
