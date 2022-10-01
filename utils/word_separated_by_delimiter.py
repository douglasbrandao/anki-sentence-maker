def word_separated_by_delimiter(w: str, d: str):
    word: list[str] = w.split()
    if len(word) > 1:
        return d.join(word)
    return word[0]
