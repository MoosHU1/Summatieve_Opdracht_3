import psycopg2


def get(colom, table):
    try:
        connection = psycopg2.connect("dbname = voordeelshop user=postgres password=''")

        cursor = connection.cursor()
        postgreSQL_select_Query = "select "+colom+" from "+table

        cursor.execute(postgreSQL_select_Query)
        print("Selecting rows from products table using cursor.fetchall")
        records = cursor.fetchall()

        return records

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)

    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")



def content_filtering():
    records = get("*", "products")
    category_in_cart = 'Huishouden'
    target_in_cart = 'Vrouwen'
    sellingprice_in_cart = 190
    for row in records:
        if row[4] == category_in_cart and \
                sellingprice_in_cart-20 < row[10] < sellingprice_in_cart+20 and \
                row[7] == target_in_cart:

            print(row[1])

def collaborative_filtering():
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


    print(prodids)

