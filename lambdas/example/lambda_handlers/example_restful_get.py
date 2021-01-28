import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger.info('Requested event: {}'.format(event))
    return {
        'statusCode': 200,
        'body': 'Hi, Best wishes from RESTful GET example! '
                'Have a Wonderful day!',
    }
