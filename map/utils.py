def change_price_to_string(price):
    if price:
        origin_price = price * 10000
        result_price = ''
        if origin_price >= 100000000:
            result_price += format(int(origin_price) // 100000000, ",") + '억 '
            origin_price = int(origin_price) % 100000000
        if origin_price >= 10000:
            result_price += format(int(origin_price) // 10000, ",")
            origin_price = int(origin_price) % 10000
        if origin_price >= 1:
            result_price += format(int(origin_price), ",")
        result_price = result_price.rstrip()
        return result_price

def change_maintenance_fee_to_string(price):
    if price:
        result_price = float(price)
        return result_price
