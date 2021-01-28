class ServiceException(Exception):
    error_code = 'Service Unavailable'

    def __str__(self) -> str:
        return f'{self.error_code}: {" ".join(self.args)}'


class AccessDeniedException(Exception):
    error_code = 'Access Denied'


class BadRequestException(Exception):
    error_code = 'Bad Request'


class InternalErrorException(Exception):
    error_code = 'Internal Error'


class UnauthorizedException(Exception):
    error_code = 'Unauthorized'
