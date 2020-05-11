def word_separated_by_hiphen(w, d):
    word = w.split()
    if len(word) > 1:
        return d.join(word)
    return word[0]
