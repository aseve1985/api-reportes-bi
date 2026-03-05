import psycopg2
import pandas as pd

from .config import (
    REDSHIFT_HOST,
    REDSHIFT_DB,
    REDSHIFT_USER,
    REDSHIFT_PASSWORD,
    REDSHIFT_PORT,
    query
)


def ejecutar_query_redshift(params):
    conn = None
    try:
        conn = psycopg2.connect(
            host=REDSHIFT_HOST,
            dbname=REDSHIFT_DB,
            user=REDSHIFT_USER,
            password=REDSHIFT_PASSWORD,
            port=REDSHIFT_PORT
        )

        conn.autocommit = False
        cur = conn.cursor()

        cur.execute(query, params)

        # 👉 Si la query devuelve resultados (SELECT / FUNCTION)
        if cur.description:
            columns = [desc[0] for desc in cur.description]
            rows = cur.fetchall()
            df = pd.DataFrame(rows, columns=columns)
        else:
            df = None

        conn.commit()
        print("Query ejecutada correctamente en Redshift")

        return df

    except Exception as e:
        if conn:
            conn.rollback()
        raise Exception(f"Error ejecutando query en Redshift: {e}")

    finally:
        if conn:
            conn.close()
