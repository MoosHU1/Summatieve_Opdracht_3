import psycopg2


def get(colom, table, limit):
    try:
        connection = psycopg2.connect("dbname = voordeelshop user=postgres password=''")

        cursor = connection.cursor()
        if colom == 'a':
            postgreSQL_select_Query = "SELECT profid, category FROM profiles_previously_viewed, products WHERE prodid = id LIMIT 100;"

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
        elif table == "colab_recommendations":
            cursor.execute("""INSERT INTO colab_recommendations VALUES(%s,%s)""",(values[0], values[1]))

        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into table")

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into table", error)


def content_filtering():
    records = get("*", "products",'')

    #   Hardcoded voor deze opdracht
    productid_in_cart = '45416'
    category_in_cart = 'Huishouden'
    target_in_cart = 'Vrouwen'
    sellingprice_in_cart = 190


    recommended_ids = []

    for row in records:
        if row[4] == category_in_cart and \
                sellingprice_in_cart-20 < row[10] < sellingprice_in_cart+20 and \
                row[7] == target_in_cart:

            recommended_ids.append(row[0])

    for recommendation in recommended_ids:
        insert_into_postgres("content_recommendations", (productid, recommendation))




def collaborative_filtering():  # Profielen koppelen aan categorie
    profiles_category_get = get("a", "", "")

    profiles_category = []
    for item in profiles_category_get:
        if profiles_category_get.count(item) > 2:
            profiles_category.append(item)

    profiles_category = set(profiles_category)

    for item in profiles_category:
        print(item)
        insert_into_postgres("colab_recommendations", (item))






















def collaborative_filtering_test():
    records = get("*", "profiles_previously_viewed")
    productids_cart = ['8510', '20371']
    profids = []
    prodids =[]
    for productid in productids_cart: # 1 recommendation per product in winkelmandje
        for row in records:
            if row[0] in profids:
                prodids.append(row[1])
                profids.remove(row[0])
                break
            if row[1] == productid:
                profids.append(row[0])


def collaborative_filtering_test_(): #    Profielen koppelen aan categorie
    profiles_viewed_category_get = get("a", "", "")

    #   Deze 3 for loops halen alle profielen weg die minder dan 3 producten hebben bekeken
    profids = []
    for item in profiles_viewed_category_get:
        profids.append(item[0])

    for item in profids:
        if profids.count(item) <=3:
            profids.remove(item)

    profiles_viewed_category = []
    for item in profiles_viewed_category_get:
        if item[0] in profids:
            profiles_viewed_category.append(item)

