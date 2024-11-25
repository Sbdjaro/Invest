

if __name__ == '__main__':

    # Инициализируем таблицу с инструментами
    from .instruments import get_sql_instruments
    get_sql_instruments(force=True)
