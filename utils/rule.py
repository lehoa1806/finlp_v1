from copy import deepcopy
from typing import Dict, List

from .conditions import AttributeCondition, Condition


class Rule:
    def __init__(
        self,
        conditions: Dict,
    ) -> None:
        if not isinstance(conditions, Dict):
            msg = 'Not supported conditions: {}'.format(conditions)
            raise ValueError(msg)
        if len(conditions) != 1:
            self.operator = 'and'
            self.conditions = conditions
        else:
            self.operator = list(conditions.keys())[0].lower()
            self.conditions = list(conditions.values())[0]

    def __call__(
        self,
        data: Dict,
    ) -> bool:
        def conditions_are_matched(
            _operator: str,
            _conditions: Dict[str, str],
            _data: Dict[str, str],
        ) -> bool:
            _sub_conditions = [Condition(_operator)(_data.get(key), value)
                               for key, value in _conditions.items()]
            return all(_sub_conditions)

        if not isinstance(data, Dict):
            raise ValueError('Invalid conditions data: {}'.format(data))
        if not self.conditions:
            return True
        elif self.operator in Condition.LOGICAL_OPERATORS:
            conditions = [Rule(dict([item]))(data)
                          for item in self.conditions.items()]
            return Condition(self.operator)(*conditions)
        elif self.operator in AttributeCondition.ATTRIBUTE_OPERATORS:
            conditions = [
                AttributeCondition(self.operator)(key, data)
                if value else not AttributeCondition(self.operator)(key, data)
                for key, value in self.conditions.items()
            ]
            return all(conditions)
        else:
            if isinstance(self.conditions, List):
                return any(
                    [conditions_are_matched(_operator=self.operator,
                                            _conditions=sub_conditions,
                                            _data=data)
                     for sub_conditions in self.conditions]
                )
            elif isinstance(self.conditions, Dict):
                return conditions_are_matched(
                    _operator=self.operator,
                    _conditions=self.conditions,
                    _data=data,
                )

    def update_rules(
        self,
        rules: 'Rule',
    ) -> None:
        if not rules.conditions:
            return
        if self.operator == rules.operator:
            self.conditions.update(rules.conditions)
        elif self.operator == 'and':
            self.conditions.update({rules.operator: rules.conditions})
        else:
            self.conditions = {
                self.operator: self.conditions,
                rules.operator: rules.conditions,
            }
            self.operator = 'and'

    def get_rule(
        self,
        rule_key: str,
    ) -> Dict:
        """
        Return all available rules for the given rule_key
        """
        def remove_invalid_paths(key: str, nested_dict: Dict) -> None:
            """
            Keep desired paths, which contain the given key in the nested
            dictionary and remove the rest
            """
            for k, v in list(nested_dict.items()):
                if k == key:
                    continue
                if isinstance(v, Dict):
                    remove_invalid_paths(key, v)
                if not v or not isinstance(v, Dict):
                    nested_dict.pop(k)

        conditions = deepcopy(self.conditions)
        remove_invalid_paths(rule_key, conditions)
        return conditions
