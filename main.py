'''
Bron 1: https://stackoverflow.com/questions/40942814/remove-commas-from-tuples-in-list

'''

import psycopg2


def get(colom, table, limit):
    try:
        connection = psycopg2.connect("dbname = voordeelshop user=postgres password=''")

        cursor = connection.cursor()
        if colom == 'a':
            postgreSQL_select_Query = "SELECT profid, category FROM profiles_previously_viewed, products WHERE prodid = id LIMIT 500;"

        elif limit == '':
            postgreSQL_select_Query = "select " +colom+" from " + table
        else:
            postgreSQL_select_Query = "select "+colom+" from "+table+" limit "+limit


        cursor.execute(postgreSQL_select_Query)
        print("Selecting rows from products table using cursor.fetchall")
        records = cursor.fetchall()

        return records

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)


def insert_into_postgres(table, values):
    try:
        connection = psycopg2.connect("dbname = voordeelshop user=postgres password=''")
        cursor = connection.cursor()

        if table == "content_recommendations":
            cursor.execute("""INSERT INTO content_recommendations VALUES({},{})""".format(values[0], values[1]))
        elif table == "colab_category":
            cursor.execute("""INSERT INTO colab_category VALUES(%s,%s)""",(values[0], values[1]))
        elif table == "colab_others_bought":
            cursor.execute("""INSERT INTO colab_others_bought VALUES(%s,%s)""", (values[0], values[1]))

        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into table")

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into table", error)


def content_filtering():
    records = get("*", "products",'50')

    recommended_ids = []
    loop =0
    for product_cart in records:
        for product_recommend in records:
            # [4] = Category, [10] = Sellingprice, [7] = targetaudience
            if product_cart != product_recommend and product_recommend[4] == product_cart[4] and \
                    product_cart[10]-5 < product_recommend[10] < product_cart[10]+5 and \
                    product_recommend[7] == product_cart[7]:

                insert_into_postgres("content_recommendations", (product_cart[0],product_recommend[0]))



def collaborative_filtering_category():  # Profielen koppelen aan categorie
    profiles_category_get = get("a", "", "")
    products = get("*", "products", "")

    #   Koppelt een categorie aan elk profiel
    profiles_category = []
    for item in profiles_category_get:
        if profiles_category_get.count(item) > 2:
            profiles_category.append(item)

    profiles_category = set(profiles_category)

    for item in profiles_category:
        insert_into_postgres("colab_category", (item))


def collaborative_filtering_others_bought():
    records = get("*", "profiles_previously_viewed",'100')
    productids_get = get("id", "products", '')

    productids = [item[0] for item in productids_get] #    Zorgt dat de tuples gewoon strings worden

    # 1 recommendation per product in winkelmandje op basis van andere mensen die
    # naar hetzelfde product hebben gekeken
    profid_temp = ''
    for productid in productids:
        for record in records:
            if record[0] == profid_temp:
                insert_into_postgres("colab_others_bought", (productid, record[1]))
                profid_temp = ''
            if productid == record[1]:
                profid_temp = record[0]



collaborative_filtering_category()