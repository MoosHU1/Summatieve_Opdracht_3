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

