#                                MPATTERNS
#                    Fast and minimal syntax validation

#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.


import re

ALPHANUMERIC_PATTERN = r'^[a-zA-Z_][a-zA-Z0-9_\$]*$'
NUMERIC_PATTERN = r'[0-9]*$'
ALPHA_PATTERN = r'[a-zA-Z_]*$'

######################
# Default Validation #
######################

class DefaultException(Exception):
    pass


class Validator(object):
    """
    Validate an element using a regex sample
    ----------------------------------------
    >>> from mpatterns import Validator
    >>> v = Validator(r'[0-5]*$')
    >>> v.validate("01")
    True
    >>> v.validate("016")
    False
    """
    def __init__(self, pattern_regex):
        self._pr = pattern_regex

    def validate(self, element):
        return bool(re.match(self._pr, element))


class PatternValidator(object):
    """
    Validate a list of elements and values of a dictionary
    ------------------------------------------------------
    >>> from mpatterns import PatternValidator as PV
    >>> pv = PV(r'[a-zA-Z_]*$')
    >>> pv.validate("le", "reg", "__okei", option="zeke")
    True
    >>> pv.validate("le", "reg", "__okei", option="982092878")
    False
    """
    def __init__(self, pattern_regex):
        self._validator = Validator(pattern_regex)

    def _validate_pattern(self, element):
        return self._validator.validate(str(element))

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
    def Validate(cls, *args, **kwargs):
        obj = object.__new__(cls)
        obj.__init__()
        return obj.validate(*args, **kwargs)


def ValidateDecorator(type_class, _return, _raise):
    """
    Decorate a function to all validate it arguments using a PatternValidator
    -------------------------------------------------------------------------
    >>> from mpatterns import ValidateDecorator, DefaultException, NumericValidator
    >>> @ValidateDecorator(NumericValidator, True, DefaultException)
        def sm(a, b):
            return a + b

    >>> sm(1, 2):
    3
    >>> sm("ab", "cd"):
        File "<stdin>", line 1, in <module>
        File "/Users/ial-ah/GitHub/mad-patterns/madpatterns.py", line 56, in wrap_args
            raise _raise()
        mpatterns.AlphaNumericValidatorException
    """
        def wrap_func(func):
            def wrap_args(*args, **kwargs):
                passed = type_class.Validate(*args, **kwargs)
                if passed:
                    _res = func(*args, **kwargs)
                    if _return:
                        return _res
                else:
                    raise _raise()
            return wrap_args
        return wrap_func

######################
# Numeric Validation #
######################

class NumericValidatorException(Exception):
    pass


class NumericValidator(PatternValidator):

    def __init__(self):
        PatternValidator.__init__(self, NUMERIC_PATTERN)


def NumericValidateDecorator(_return):
    return ValidateDecorator(NumericValidator, _return, NumericValidatorException)

####################
# Alpha Validation #
####################

class AlphaValidatorException(Exception):
    pass

class AlphaValidator(PatternValidator):

    def __init__(self):
        PatternValidator.__init__(self, ALPHA_PATTERN)


def AlphaValidateDecorator(_return):
    return ValidateDecorator(AlphaValidator, _return, AlphaValidatorException)


############################
# Alpha Numeric Validation #
############################

class AlphaNumericValidatorException(Exception):
    pass

class AlphaNumericValidator(PatternValidator):

    def __init__(self):
        PatternValidator.__init__(self, ALPHANUMERIC_PATTERN)

def AlphaNumericValidateDecorator(_return):
    return ValidateDecorator(AlphaNumericValidator, _return, AlphaNumericValidatorException)
