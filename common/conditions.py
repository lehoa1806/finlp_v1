from typing import Any, Dict, Iterable, Optional


class Condition:
    LOGICAL_OPERATORS = ['and', 'or', 'not']
    CONDITION_OPERATORS = ['eq', 'lt', 'lte', 'gt', 'gte', 'ne', 'contains',
                           'not_contains', 'contains_any', 'begins_with']

    def __init__(
        self,
        operator: str,
    ):
        self.operator = operator.lower()
        self.support_operators = \
            self.CONDITION_OPERATORS + self.LOGICAL_OPERATORS

    def __call__(self, *values: Any) -> bool:
        if self.operator not in self.support_operators:
            return True
        elif self.operator == 'and':
            return all(values)
        elif self.operator == 'or':
            return any(values)
        elif self.operator == 'not':
            return not all(values)
        else:
            if not values or len(values) == 1:
                return False
            caller = getattr(self, self.operator)
            return caller(*values)

    @classmethod
    def eq(
        cls,
        left_operand: Any,
        right_operand: Any,
    ) -> bool:
        """
        Return true if the left operand is equal to the right operand.

        :param left_operand: input value
        :param right_operand: based value
        :return: boolean
        """
        return type(right_operand)(left_operand) == right_operand

    @classmethod
    def lt(
        cls,
        left_operand: Any,
        right_operand: Any,
    ) -> bool:
        """
        Return true if the left operand is less than the right operand.

        :param left_operand: input value
        :param right_operand: based value
        :return: boolean
        """
        return type(right_operand)(left_operand) < right_operand

    @classmethod
    def lte(
        cls,
        left_operand: Any,
        right_operand: Any,
    ) -> bool:
        """
        Return true if the left operand is less than or equal to the right
        operand.

        :param left_operand: input value
        :param right_operand: based value
        :return: boolean
        """
        return type(right_operand)(left_operand) <= right_operand

    @classmethod
    def gt(
        cls,
        left_operand: Any,
        right_operand: Any,
    ) -> bool:
        """
        Return true if the left operand is greater than the right operand.

        :param left_operand: input value
        :param right_operand: based value
        :return: boolean
        """
        return type(right_operand)(left_operand) > right_operand

    @classmethod
    def gte(
        cls,
        left_operand: Any,
        right_operand: Any,
    ) -> bool:
        """
        Return true if the left operand is greater than or equal to the right
        operand.

        :param left_operand: input value
        :param right_operand: based value
        :return: boolean
        """
        return type(right_operand)(left_operand) >= right_operand

    @classmethod
    def ne(
        cls,
        left_operand: Any,
        right_operand: Any,
    ) -> bool:
        """Return true if the left operand is not equal to the right operand.

        :param left_operand: input value
        :param right_operand: based value
        :return: boolean
        """
        return type(right_operand)(left_operand) != right_operand

    @classmethod
    def contains(
        cls,
        left_operand: str,
        right_operand: str,
    ) -> bool:
        """Return true if the left operand contains the right operand.

        :param left_operand: input value
        :param right_operand: based value
        :return: boolean
        """
        left_operand = str(left_operand or '')
        return right_operand in left_operand

    @classmethod
    def not_contains(
        cls,
        left_operand: str,
        right_operand: str,
    ) -> bool:
        """Return true if the left operand does not contain the right operand.

        :param left_operand: input value
        :param right_operand: based value
        :return: boolean
        """
        left_operand = str(left_operand or '')
        return right_operand not in left_operand

    @classmethod
    def contains_any(
        cls,
        left_operand: str,
        right_operand: Iterable[str],
    ) -> bool:
        """Return true if the left operand contains any elements from the given
        list.

        :param left_operand: input value
        :param right_operand: A list of base values
        :return: boolean
        """
        return any(
            element in str(left_operand or '') for element in right_operand
        )

    @classmethod
    def begins_with(
        cls,
        left_operand: str,
        right_operand: str,
    ) -> bool:
        """Return true if the left operand begins with the right operand.

        :param left_operand: input value
        :param right_operand: based value
        :return: boolean
        """
        left_operand = str(left_operand or '')
        return left_operand.startswith(right_operand)


class AttributeCondition(Condition):
    ATTRIBUTE_OPERATORS = ['exists', 'not_exists']

    def __init__(
        self,
        operator: str,
    ):
        super().__init__(operator)
        self.support_operators = \
            self.support_operators + self.ATTRIBUTE_OPERATORS

    def __call__(
        self,
        key: Optional[str] = None,
        data: Optional[Dict] = None,
        *values: Any,
    ) -> bool:
        if not isinstance(data, Dict):
            data = {}
        if self.operator in self.ATTRIBUTE_OPERATORS:
            caller = getattr(self, self.operator)
            return caller(key, data)
        else:
            if key:
                left_operand = data.get(key)
                values = (left_operand,) + values
            return super().__call__(*values)

    @classmethod
    def exists(
        cls,
        key: str,
        data: Dict,
    ) -> bool:
        """
        Return true if the given key is in the given data or the corresponding
        value is True.

        :param key: the given key
        :param data: the given data
        :return: boolean
        """
        return data.get(key, False)

    @classmethod
    def not_exists(
        cls,
        key: str,
        data: Dict,
    ) -> bool:
        """
        Return true if the given key is not in the given data or the
        corresponding value is True.

        :param key: the given key
        :param data: the given data
        :return: boolean
        """
        return not data.get(key, False)
