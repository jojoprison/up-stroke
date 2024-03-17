import asyncpg
from sshtunnel import SSHTunnelForwarder
import asyncio


async def get_pg_remote_connect():
    try:
        ssh_tunnel = SSHTunnelForwarder(
            ('135.181.251.7', 22),
            ssh_username='squalordf',
            ssh_password='149367139Diez',
            remote_bind_address=('localhost', 5432)
        )

        ssh_tunnel.start()
        print('ssh tunnel open')

        db_params = {
            'database': 'postgres',
            'user': 'postgres',
            'password': 'postgres',
            'host': 'localhost',
            'port': ssh_tunnel.local_bind_port
        }

        print('run')

        # con = psycopg2.connect(**db_params)
        con = await asyncpg.connect(**db_params)

        print(con)
    except:
        print('con fail')


if __name__ == '__main__':
    conn = asyncio.get_event_loop().run_until_complete(get_pg_remote_connect())