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
        body_params.get('watchlists') or body_params.get('portfolio')
    ):
        raise BadRequestException('No valid data in the request.')

    watchlists = body_params.get('watchlists')
    '''
    [{
        name: WATCHLIST1,
        warrants: ['WARRANT1', 'WARRANT2'],
        newName: WATCHLIST2,
    }]
    '''
    portfolio = body_params.get('portfolio')
    '''
    [{
        warrant: 'WARRANT0',
        quantity: 100,
        acquisitionPrice: 9999,
    }]
    '''

    credentials = {
        'host': os.getenv('POSTGRESQL_HOST'),
        'user': os.getenv('POSTGRESQL_USER'),
        'password': os.getenv('POSTGRESQL_PASSWD'),
        'dbname': os.getenv('POSTGRESQL_DB'),
        'port': int(os.getenv('POSTGRESQL_PORT')),
    }
    database = Database.load_database(config=credentials)
    if watchlists:
        watchlists_to_insert = []
        for watchlist in watchlists:
            name = watchlist.get('name')
            new_name = watchlist.get('newName')
            if name != new_name:
                with database.connection.psycopg2_client.cursor() as cursor:
                    values_to_update = cursor.mogrify(
                        '(%s, %s)', [new_name, json.dumps(watchlist.get('warrants'))]).decode('utf-8')
                    condition = cursor.mogrify('(%s, %s)', [user, name]).decode('utf-8')
                    command = WATCHLISTS_UPDATE.format(values_to_update=values_to_update, condition=condition)
                    database.connection.execute(command)
                    logging.info('Update 1 records to users_watchlists.')
            else:
                watchlists_to_insert.append(watchlist)
        if watchlists_to_insert:
            with database.connection.psycopg2_client.cursor() as cursor:
                values_to_insert = ', '.join(
                    cursor.mogrify(
                        '(%s, %s, %s)', [user, item.get('name'), json.dumps(item.get('warrants'))]).decode('utf-8')
                    for item in watchlists_to_insert
                )
            logging.info(
                f'Inserting {len(watchlists)} records to users_watchlists.')
            command = WATCHLISTS_QUERY.format(values_to_insert=values_to_insert)
            database.connection.execute(command)

    if portfolio:
        with database.connection.psycopg2_client.cursor() as cursor:
            values_to_insert = ', '.join(
                cursor.mogrify(
                    '(%s, %s, %s, %s)',
                    [user,
                     item.get('warrant'),
                     item.get('quantity'),
                     str(item.get('acquisitionPrice'))]).decode('utf-8')
                for item in portfolio
            )
        logging.info(
            f'Inserting {len(portfolio)} records to users_portfolio.')
        command = PORTFOLIO_QUERY.format(values_to_insert=values_to_insert)
        database.connection.execute(command)

    return {
        'statusCode': 200,
        'body': 'Success.',
    }
