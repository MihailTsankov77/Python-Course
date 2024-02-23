import sys


# Methods for each char of a FN
# It might be nice to simply copy them to avoid duplicate definitions
# but even the copy module couldn't produce different identity so I gave up.
def method_F():
    pass  # Static method defined in the class


def method_N():
    raise BaseException('Опаааааа, и тука има нещо нередно.')


def method_M(num):
    return 0 if num % 2 else num ** 2


def method_I(*, left='', right=''):
    return left + right


def method_0():
    raise TypeError('Опаааааа, тука има нещо нередно.')


def method_1(num):
    return 0 if num % 2 else num ** 2


def method_2(*, left, right):
    return left + right


def method_3(num):
    return 0 if num % 2 else num ** 2


def method_4(num):
    return 0 if num % 2 else num ** 2


def method_5(*, left, right):
    return left + right


def method_6():
    raise TypeError('Опаааааа, тука има нещо нередно.')


def method_7(*, left, right):
    return left + right


def method_8(num):
    return 0 if num % 2 else num ** 2


def method_9(*, left='', right=''):
    return left + right

# Decoy functions that look like real ones, but are not


def decoy_1():
    raise TypeError('Това не е грешката с правилния текст.')


def decoy_2():
    raise AttributeError('Това е друг вид грешка.')


def decoy_3(num):
    if num == 0:
        return 666  # Just making sure that squaring zeroes is still not correct
    return num ** 2 if num % 2 else 0  # The opposite of what is really expected


def decoy_4(*, left='', right=''):
    # Let's see if somebody uses the same value for left and right and falls into the trap
    return right + left


# Class that will be used for every instance inside the master object
BUILDING_BLOCK = type('BuildingBlock', (object, ), {
                      'F': staticmethod(method_F)})

# Reference to the current module to allow adding an object to it
THIS = sys.modules[__name__]

# Definition of an object to create.
# Dictionaries will be parsed as objects.
# The rest is parsed as is.
OBJECT_DEFINITION = {
    'clue_1': {
        'F': decoy_2
    },
    'clue_2': {
        'clue_2_1': {
            'N': method_N,
            'F': decoy_1,
            '0': decoy_1,
            '1': method_1,
            'fake_1': (1, 2, 3)
        },
        '2': method_2,
        'clue_2_3': {
            'clue_2_3_1': {},
            '8': decoy_2,
            '9': decoy_4,
            '3': method_3,
            'clue_2_3_3': {
                '4': method_4,
                '5': method_5,
                '6': decoy_3,
                '7': decoy_1,
                'fake_1': 'random string',
                'clue_2_3_3_4': 42
            },
            '6': method_6,
            'N': decoy_3,
            '4': decoy_2,
            '5': decoy_1,
            'fake_1': 3.14
        }
    },
    'clue_3': {
        'clue_3_1': {
            'clue_3_1_1': {
                '7': method_7,
                '8': method_8,
                'F': decoy_1,
                '2': decoy_3,
                '3': decoy_4,
                'clue_3_1_1_3': {
                    '9': method_9
                }
            },
            '0': method_0,
            'fake_1': set()
        },
        'clue_3_2': {
            'clue_3_2_1': {
                'clue_3_2_1_1': {
                    'N': decoy_1,
                    'clue_3_2_1_1_1': {
                        'clue_3_2_1_1_1_1': {
                            'M': method_M,
                            'I': method_I,
                            'F': decoy_1,
                            '5': decoy_2,
                            '0': decoy_3,
                            '1': decoy_4,
                        }
                    }
                }
            }
        }
    }
}


_RAW_RESULTS = {
    '0123456789MI': {'correct': 30, 'points': 30},
    'Още факултетни номера и резултати тук...': '...'
}

# Build results with tuples of functions as keys
_RESULTS = {}
for key, val in _RAW_RESULTS.items():
    fun_key = tuple([globals()[f'method_{x}'] for x in 'FN' + key])
    _RESULTS[fun_key] = val

# Construct a master object based on the dict definition
# and attach it to the current module


def construct_object(root, obj_def):
    for key, val in obj_def.items():
        if type(val) is dict:
            obj = BUILDING_BLOCK()
            setattr(root, key, obj)
            construct_object(obj, val)
        else:
            setattr(root, key, val)


construct_object(THIS, OBJECT_DEFINITION)
