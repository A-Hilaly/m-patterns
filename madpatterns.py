#
#

import re

ALPHANUMERIC_PATTERN = r'^[a-zA-Z_][a-zA-Z0-9_\$]*$'
NUMERIC_PATTERN = r'[0-9]*$'
ALPHA_PATTERN = r'[a-zA-Z_]*$'


class Validator(object):

    def __init__(self, pattern_regex):
        self._pr = pattern_regex

    def validate(self, element):
        return bool(re.match(self._pr, element))


class PatternValidator(object):

    def __init__(self, pattern_regex):
        self._validator = Validator(pattern_regex)

    def _validate_pattern(self, element):
        return self._validator.validate(element)

    def _validate_patterns(self, *args):
        return not(
            False in [
                self._validate_pattern(e) for e in list(args)
            ]
        )

    def validate(self, *args, **kwargs):
        return (
            self._validate_patterns(*args) and
                self._validate_patterns(*list(kwargs.values()))
        )

    @classmethod
    def Validate(cls, *args, pattern_regex=None, **kwargs):
        obj = object.__new__(cls)
        obj.__init__()
        return obj.validate(*args, **kwargs)

    @classmethod
    def _ValidateDecorator(cls, *args, **kwargs):
        raise NotImplemented()

class NumericValidator(PatternValidator):

    def __init__(self):
        PatternValidator.__init__(self, NUMERIC_PATTERN)

class AlphaValidator(PatternValidator):

    def __init__(self):
        PatternValidator.__init__(self, ALPHA_PATTERN)

class AlphaNumericValidator(PatternValidator):

    def __init__(self):
        PatternValidator.__init__(self, ALPHANUMERIC_PATTERN)
