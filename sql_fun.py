import psycopg2
import config

# Connecting to database
conn = psycopg2.connect(
    dbname=config.database,
    user=config.user,
    password=config.password,
    host=config.host,
    port=config.port   # Disable for test
    )

curs = conn.cursor()
print('Connect to database:', conn.dsn)


def simple_find_member(member_id: str) -> bool:
    """Checking for user existence in the database"""
    curs.execute("SELECT id FROM users WHERE id=%s", (member_id,))
    return False if curs.fetchone() == None else True  # "is None" don't working


def add_user(member_id: str) -> None:
    """Add user in database with standard user data"""
    curs.execute("""
                INSERT INTO users
                VALUES (%(id)s, %(t_coins)s, %(t_coins_full)s);
                """, {'id': member_id, 't_coins': 0, 't_coins_full': 0}
                 )
    conn.commit()


def check_balance(member_id: str) -> list:
    """Checking user account in database"""
    curs.execute("SELECT id,t_coin,t_coin_full FROM users where id=%s", (member_id,))
    return curs.fetchall()


def update_balance_full(member_id: str, tca: int, tcf: int) -> None:
    """Update user data (balance and history) in database"""
    curs.execute("""
                UPDATE users 
                SET t_coin = %(t_coin)s, t_coin_full = %(t_coin_full)s 
                WHERE id=%(id)s
                """, {'id': member_id, 't_coin': tca, 't_coin_full': tcf}
                 )
    conn.commit()


def update_balance_tca(member_id: str, tca: int) -> None:
    """Update user balance in database"""
    curs.execute("""
                UPDATE users 
                SET t_coin = %(t_coin)s
                WHERE id=%(id)s
                """, {'id': member_id, 't_coin': tca}
                 )
    conn.commit()


def update_balance_tcf(member_id: str, tcf: int) -> None:
    """Update user history in database"""
    curs.execute("""
                UPDATE users 
                SET t_coin_full = %(t_coin_full)s
                WHERE id=%(id)s
                """, {'id': member_id, 't_coin_full': tcf}
                 )
    conn.commit()
