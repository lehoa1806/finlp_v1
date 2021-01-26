import json
from datetime import datetime, timedelta
from decimal import Decimal
from enum import Enum


class CustomJSONEncoder(json.JSONEncoder):
    """
    Util class to encode complex objects that are not supported by
    json.JSONEncoder.
    """
    def default(self, obj):
        if hasattr(obj, 'hex'):
            return obj.hex
        if isinstance(obj, datetime):
            return str(obj)
        elif isinstance(obj, Decimal):
            return int(obj)
        elif isinstance(obj, Enum):
            if not obj.value:
                return None
            else:
                return str(obj.value)
        elif isinstance(obj, timedelta):
            return obj.__str__()

        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)
