import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger.info('Requested event: {}'.format(event))
    return {
        'statusCode': 200,
        'body': 'Hi, good luck from RESTful POST example! '
                'We wish you all the success and good health !',
    }
