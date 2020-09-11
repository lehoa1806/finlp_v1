import os


def get_environment_variable(env, default=None, require=False):
    val = os.getenv(env) or default
    if val is None and require:
        raise Exception('Environment variable [{}] not available.'.format(env))
    return val


# Slack
def get_slack_token():
    return get_environment_variable('FINULP_SLACK_TOKEN')
