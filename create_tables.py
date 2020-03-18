import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Connect to PostgreSQL DBMS
con = psycopg2.connect("dbname = voordeelshop user=postgres password=''")
con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

# Obtain a DB Cursor
cursor = con.cursor()


def create_tables():
    commands = (
        '''
        CREATE TABLE content_recommendations
        (
        product_cart_id varchar,
        product_recommendation_id varchar,
        FOREIGN KEY (product_cart_id) references products(id),
        FOREIGN KEY (product_recommendation_id) references products(id)
        )
        ''',
        '''
        CREATE TABLE colab_category
        (
        profid varchar,
        category varchar,
        FOREIGN KEY (profid) references profiles(id)
        )
        ''',
        '''
        CREATE TABLE colab_others_bought
        (
        prodid varchar,
        prodid_recommend varchar,
        FOREIGN KEY (prodid) references products(id),
        FOREIGN KEY (prodid_recommend) references products(id)
        )
       '''
    )

    try:
        for command in commands:
            cursor.execute(command)

        cursor.close()
        con.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if con is not None:
            con.close()


create_tables()