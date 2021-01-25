import argparse
import logging
import sys
from datetime import datetime

import pytz


class ArgumentParser(argparse.ArgumentParser):
    timezone: str = 'Asia/Ho_Chi_Minh'

    @property
    def arguments(self):
        group = self.add_mutually_exclusive_group()
        group.add_argument(
            '--debug',
            action='store_true',
            help='Print debugging messages.',
        )
        args = self.parse_args(namespace=argparse.Namespace())
        # Set log
        fmt = '%(asctime)s.%(msecs)03d %(name)s [%(levelname)s]: %(message)s'
        logging.basicConfig(
            format=fmt,
            datefmt='%Y-%m-%d %I:%M:%S',
            level=logging.DEBUG if args.debug else logging.INFO,
            handlers=[logging.StreamHandler(sys.stdout)],
        )
        return args

    def add_argument(self, *args, **kwargs):
        if args and isinstance(args[0], str) and not args[0].startswith('--'):
            args_list = list(args)
            args_list[0] = f'--{ args_list[0]}'
            args = tuple(args_list)
        super().add_argument(*args, **kwargs)

    def get_local_date(
        self,
        date_string: str,
    ) -> datetime:
        local = pytz.timezone(self.timezone)
        try:
            return local.localize(datetime.strptime(date_string, '%Y-%m-%d'))
        except ValueError:
            try:
                return local.localize(
                    datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
                )
            except ValueError as error:
                raise argparse.ArgumentTypeError(
                    'Invalid date format({}), should be YYYY-MM-DD or '
                    'YYYY-MM-DD HH:MM:SS'.format(str(error)))

    def add_date_input(
        self,
        name: str,
        timezone: str = 'Asia/Ho_Chi_Minh',
        required: bool = True,
    ):
        group = self.add_mutually_exclusive_group(required=required)
        self.timezone = timezone
        group.add_argument(
            '--{}'.format(name),
            type=self.get_local_date,
            help='{} in format: YYYY-MM-DD or YYYY-MM-DD HH:MM:SS'.format(name)
        )

    def add_file_input(
        self,
        name: str,
        description: str = '',
        required: bool = True,
    ) -> None:
        group = self.add_mutually_exclusive_group(required=required)
        group.add_argument(
            '--{}'.format(name),
            type=argparse.FileType('rt'),
            help=description,
        )

    def add_file_output(
        self,
        name: str,
        description: str = '',
        required: bool = True,
    ) -> None:
        group = self.add_mutually_exclusive_group(required=required)
        group.add_argument(
            '--{}'.format(name),
            type=argparse.FileType('x'),
            help=description,
        )
