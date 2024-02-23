def convert_to_dict(plugboard_position):
    dictionary = {}
    for i in plugboard_position:
        for j in i:
            dictionary[j] = (i - {j}).pop()
    return dictionary


def convert_to_dict_decorator(func):
    def wrapper(text, plugboard_position):
        return func(text, convert_to_dict(plugboard_position))
    return wrapper


def encrypt_text_with_dict(text, dictionary):
    return "".join(map(lambda key: dictionary.get(key, key), text))


def reverse_dict(dictionary):
    return {value: key for key, value in dictionary.items()}


def reverse_dict_decorator(func):
    def wrapper(text, dictionary):
        return func(text, reverse_dict(dictionary))
    return wrapper


@convert_to_dict_decorator
def plugboard(text, plugboard_position):
    return encrypt_text_with_dict(text, plugboard_position)


def rotor(text, rotor_position):
    return encrypt_text_with_dict(text, rotor_position)


@reverse_dict_decorator
def rotor_decrypt(text, rotor_position):
    return encrypt_text_with_dict(text, rotor_position)


def enigma_encrypt(plugboard_position, rotor_position):
    def decorator(func):
        def wrapper(text):
            encrypted_text = rotor(
                plugboard(text, plugboard_position), rotor_position)
            return func(encrypted_text)
        return wrapper
    return decorator


def enigma_decrypt(plugboard_position, rotor_position):
    def decorator(func):
        def wrapper(text):
            decrypted_text = plugboard(rotor_decrypt(
                text, rotor_position), plugboard_position)
            return func(decrypted_text)
        return wrapper
    return decorator
