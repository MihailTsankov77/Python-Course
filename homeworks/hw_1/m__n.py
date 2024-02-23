def get_split_index(word):
    w_len = len(word)

    if w_len%3 == 2:
        return (w_len + 1) // 3

    return w_len // 3

def beginning(word):
    return word[:get_split_index(word)]

def middle(word):
    split_index = get_split_index(word)
    return word if len(word) == 1 else word[split_index:-split_index]

def end(word):
    return '' if len(word) == 1 else word[-get_split_index(word):]

def split_word(word):
    return beginning(word), middle(word), end(word)

def split_sentence(sentence):
    return [split_word(word) for word in sentence.split()]