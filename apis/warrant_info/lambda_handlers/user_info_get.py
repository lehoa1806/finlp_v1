import json
import logging
import os
from typing import Any

from apis.utils.exceptions import UnauthorizedException
from postgresql.database import Database

logger = logging.getLogger()
logger.setLevel(logging.INFO)

WATCHLISTS_QUERY = """\
SELECT
  t1."watchlist" AS "watchlist",
  t1."warrants" AS "warrants"
FROM
  "users_watchlists" AS t1
WHERE
  t1."user" = '{user}';\
"""

PORTFOLIO_QUERY = """\
SELECT
  t1."warrant" AS "warrant",
  t1."quantity" AS "quantity",
  t1."acquisitionPrice" AS "acquisitionPrice"
FROM
  "users_portfolio" AS t1
WHERE
  t1."user" = '{user}';\
"""


def parse_json(
    data: str = '',
    default: Any = None,
) -> Any:
    if not data or not isinstance(data, str):
        return default
    try:
        value = json.loads(data)
        return type(default)(value) if default is not None else value
    except (json.decoder.JSONDecodeError, TypeError):
        return default


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

    # Watchlists
    keys = ('warrant', 'quantity', 'acquisitionPrice')
    query = PORTFOLIO_QUERY.format(user=user)
    watchlists = {}
    for item in database.query(query, keys):
        watchlist = item.get('watchlist', 'Unknown')
        warrants = parse_json(item.get('warrants', ''), [])
        watchlists.update({watchlist: warrants})

    # Portfolio
    keys = ('watchlist', 'warrants')
    query = WATCHLISTS_QUERY.format(user=user)
    portfolio = {}
    for item in database.query(query, keys):
        warrant = item.get('warrant', 'Unknown')
        quantity = item.get('quantity', 0)
        acquisition_price = item.get('acquisitionPrice', 0)
        portfolio.update({
            warrant: {
                'warrant': warrant,
                'quantity': quantity,
                'acquisitionPrice': acquisition_price,
            },
        })
    return {
        'user': {
            'name': user,
            'watchlists': watchlists,
            "portfolio": portfolio,
        },
    }