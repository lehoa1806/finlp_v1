from functools import reduce
from typing import Any, Dict, Iterator, List, Set, Tuple

from botocore import exceptions

from .conditions import AttrCondition, Condition, KeyCondition
from .utils import KeyType


class Table:
    """
    The Class to manage DynamoDB table behavior.
    """
    def __init__(
        self,
        table: Any,
    ) -> None:
        self.boto_table = table

    @property
    def name(self):
        return self.boto_table.name

    @property
    def schema(self) -> Dict[str, str]:
        _schema: Dict[str, str] = {}
        for key_element in self.boto_table.key_schema:
            if key_element['KeyType'] == 'HASH':
                _schema['partition_key'] = key_element['AttributeName']
            elif key_element['KeyType'] == 'RANGE':
                _schema['sort_key'] = key_element['AttributeName']
        return _schema

    def get_index(
        self,
        partition_key: Any = None,
        sort_key: Any = None,
        item: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        _item = item or {}
        _pk_value = partition_key or _item.get(self.schema['partition_key'])
        _sk_value = sort_key or _item.get(str(self.schema.get('sort_key')))

        _index: Dict[str, Any] = {}
        for _key, _value in self.schema.items():
            if _key == 'partition_key':
                _index[_value] = _pk_value
            elif _key == 'sort_key' and _sk_value:
                _index[_value] = _sk_value
        return _index

    @classmethod
    def get_projection_expression(
        cls,
        attributes_to_get: List[str],
    ) -> Tuple[str, Dict[str, str]]:
        # Support nested attribute but don't support attribute name that
        # contains dots
        _attrs: Set = set()
        for _attr in attributes_to_get:
            if '.' in _attr:
                _attrs.update(_attr.split('.'))
            else:
                _attrs.add(_attr)

        _attr_list = list(_attrs)
        _exp_list = ['#' + _attr for _attr in _attr_list]
        projection_expression = ', '.join(_exp_list)
        expression_attr_names = dict(zip(_exp_list, _attr_list))
        return projection_expression, expression_attr_names

    @classmethod
    def get_expression(
        cls,
        expressions: List[Dict[str, Any]],
        key_type: KeyType = KeyType.Attr,
    ):
        def get_condition(expression: Dict[str, Any]) -> Condition:
            """
            Convert data from Dict to Condition
            :param expression: {'and': [{'eq': {'key': 'value'}}]}
            :return: Condition
            """
            _condition_class = (
                AttrCondition if key_type == KeyType.Attr else KeyCondition
            )
            # The expression has only one operator-object pair
            _operator = list(expression.keys())[0]
            _object = list(expression.values())[0]
            if isinstance(_object, List):
                _sub_conditions = [get_condition(expr) for expr in _object]
                return _condition_class(_operator, None, None, _sub_conditions)
            else:
                # The expression object has only one key-value pair
                _key = list(_object.keys())[0]
                _value = list(_object.values())[0]
                return _condition_class(_operator, _key, _value, None)
        if len(expressions) == 1:
            return get_condition(expressions[0])()
        elif len(expressions) > 1:
            return reduce(
                lambda x, y: get_condition(x)() & get_condition(y)(),
                expressions,
            )
        raise ValueError('expressions cannot be empty')

    # Table functions:
    def delete_item(
        self,
        partition_key: Any = None,
        sort_key: Any = None,
        item: Dict[str, Any] = None,
    ) -> None:
        _index = self.get_index(partition_key, sort_key, item)
        self.boto_table.delete_item(Key=_index)

    def get_item(
        self,
        partition_key: Any,
        sort_key: Any = None,
        attributes_to_get: List[str] = None,
    ) -> Dict[str, Any]:
        _index = self.get_index(partition_key, sort_key)
        _kwargs: Dict[str, Any] = {'Key': _index}
        if attributes_to_get:
            _expression, _attr_names = self.get_projection_expression(
                attributes_to_get=attributes_to_get)
            _kwargs.update({
                'ProjectionExpression': _expression,
                'ExpressionAttributeNames': _attr_names,
            })
        response = self.boto_table.get_item(**_kwargs)
        return response.get('Item', {})

    def put_item(
        self,
        item: Dict[str, Any],
        filter_conditions: List[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        _kwargs: Dict[str, Any] = {'Item': item}
        if filter_conditions:
            _kwargs.update({
                'ConditionExpression': self.get_expression(
                    filter_conditions),
                'ReturnValues': 'ALL_OLD',
            })
        try:
            response = self.boto_table.put_item(**_kwargs)
            return response.get('Attributes', {})
        except exceptions.ClientError as err:
            error_code = err.response['Error']['Code']
            if error_code == 'ConditionalCheckFailedException':
                return {}
            raise err

    def query(
        self,
        key_conditions: List[Dict[str, Any]],
        filter_conditions: List[Dict[str, Any]] = None,
        attributes_to_get: List[str] = None,
        index_name: str = None,
        **kwargs,
    ) -> Iterator[Dict[str, Any]]:
        _kwargs = kwargs if kwargs else {}
        _kwargs.update({
            'KeyConditionExpression': self.get_expression(
                key_conditions, KeyType.Key),
            'IndexName': index_name,
        })
        if attributes_to_get:
            _expression, _attr_names = self.get_projection_expression(
                attributes_to_get=attributes_to_get)
            _kwargs.update({
                'ProjectionExpression': _expression,
                'ExpressionAttributeNames': _attr_names,
            })
        if filter_conditions:
            _kwargs.update({
                'FilterExpression': self.get_expression(filter_conditions),
            })
        while True:
            _kwargs = {k: v for k, v in _kwargs.items() if v is not None}
            response = self.boto_table.query(**_kwargs)
            for item in response['Items']:
                yield item
            if 'LastEvaluatedKey' not in response:
                break
            _kwargs['ExclusiveStartKey'] = response['LastEvaluatedKey']

    def scan(
        self,
        filter_conditions: List[Dict[str, Any]] = None,
        attributes_to_get: List[str] = None,
        index_name: str = None,
        **kwargs,
    ) -> Iterator[Dict[str, Any]]:
        _kwargs = kwargs if kwargs else {}
        _kwargs.update({'IndexName': index_name})
        if attributes_to_get:
            _expression, _attr_names = self.get_projection_expression(
                attributes_to_get=attributes_to_get)
            _kwargs.update({
                'ProjectionExpression': _expression,
                'ExpressionAttributeNames': _attr_names,
            })
        if filter_conditions:
            _kwargs.update({
                'FilterExpression': self.get_expression(filter_conditions),
            })
        while True:
            _kwargs = {k: v for k, v in _kwargs.items() if v is not None}
            response = self.boto_table.scan(**_kwargs)
            for item in response['Items']:
                yield item
            if 'LastEvaluatedKey' not in response:
                break
            _kwargs['ExclusiveStartKey'] = response['LastEvaluatedKey']

    def update_item(
        self,
        partition_key: Any = None,
        sort_key: Any = None,
        add_data: Dict[str, Any] = None,
        remove_data: List[str] = None,
        set_data: Dict[str, Any] = None,
    ) -> bool:
        """
        Update an existing item
        :param partition_key:
        :param sort_key:
        :param add_data:
        :param remove_data:
        :param set_data:
        :return:
        """
        _index = self.get_index(
            partition_key=partition_key,
            sort_key=sort_key,
            item=add_data or set_data or {}
        )
        _add_data = {
            k: v for k, v in add_data.items() if k not in _index
        } if add_data else {}
        _set_data = {
            k: v for k, v in set_data.items() if k not in _index
        } if set_data else {}
        _remove_data = remove_data or []
        _attr_names = {}
        _attr_values = {}
        _update_expression = ''
        for _i, (_k, _v) in enumerate(_add_data.items()):
            if _i == 0:
                _update_expression += ' add #{} :{}'.format(_k, _k)
            else:
                _update_expression += ', #{} = :{}'.format(_k, _k)
            _attr_values[':{}'.format(_k)] = _v
            _attr_names['#{}'.format(_k)] = _k
        for _i, (_k, _v) in enumerate(_set_data.items()):
            if _i == 0:
                _update_expression += ' set #{} = :{}'.format(_k, _k)
            else:
                _update_expression += ', #{} = :{}'.format(_k, _k)
            _attr_values[':{}'.format(_k)] = _v
            _attr_names['#{}'.format(_k)] = _k
        for _i, _k in enumerate(_remove_data):
            if _i == 0:
                _update_expression += ' remove {}'.format(_k)
            else:
                _update_expression += ', {}'.format(_k)

        _kwargs = {
            'Key': _index,
            'UpdateExpression': _update_expression,
            'ExpressionAttributeNames': _attr_names,
            'ExpressionAttributeValues': _attr_values,
            'ReturnValues': 'UPDATED_NEW',
        }
        response = self.boto_table.update_item(**_kwargs)
        return response.get('Attributes', {})
