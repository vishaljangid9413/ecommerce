from django import template
from django.utils.safestring import SafeString
from decimal import Decimal


register = template.Library()

@register.filter
def sort_by(obj, value):
    try:
        return obj.order_by(value)
    except Exception as e:
        print("SORT BY - ERROR:", str(e))
        return obj

@register.filter
def join_by(arr, key):
    try:
        return (key).join(arr)
    except Exception as e:
        print("JOIN BY - ERROR:", str(e))
        return arr

@register.filter
def get_item(dictionary, key):
    return dictionary.get(str(key), 0)

@register.filter
def multiply(value, multiplier):
    safe_string = SafeString("123.45")  # Example SafeString object
    decimal_value = Decimal("2.5")  # Example Decimal value

    # Convert SafeString to a numeric value
    numeric_value = Decimal(str(safe_string))  # Convert SafeString to string, then to Decimal

    # Perform the multiplication
    result = numeric_value * decimal_value
    return result