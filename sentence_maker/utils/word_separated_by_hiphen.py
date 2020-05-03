def word_separated_by_hiphen(w):
    word = w.split()
    if len(word) > 1:
        return '-'.join(word)
    return word[0]
