from utils.configs.setting import Setting

from postgresql_wrapper.database import Database as PostgreSQL


class Database(PostgreSQL):
    @classmethod
    def load_default_database(cls) -> PostgreSQL:
        setting = Setting()
        config = {
            'host': setting.postgresql_host,
            'user': setting.postgresql_credentials[0],
            'password': setting.postgresql_credentials[1],
            'dbname': setting.postgresql_database,
            'port': setting.postgresql_port,
        }
        return cls.load_database(config)
