from singer import utils
import psycopg2

from target_postgres.postgres import PostgresTarget
from target_postgres import target_tools

REQUIRED_CONFIG_KEYS = [
    'postgres_database'
]

def main(config, input_stream=None):
    with psycopg2.connect(
            host=config.get('postgres_host', 'localhost'),
            port=config.get('postgres_port', 5432),
            dbname=config.get('postgres_database'),
            user=config.get('postgres_username'),
            password=config.get('postgres_password')
    ) as connection:
        postgres_target = PostgresTarget(
            connection,
            postgres_schema=config.get('postgres_schema', 'public'))

        if input_stream:
            target_tools.stream_to_target(input_stream, postgres_target, config=config)
        else:
            target_tools.main(postgres_target)

def cli():
    args = utils.parse_args(REQUIRED_CONFIG_KEYS)

    main(args.config)
