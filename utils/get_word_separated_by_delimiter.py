def get_word_separated_by_delimiter(w: str, d: str):
    """Convert list of strings to a single string separated by a delimiter"""
    word: list[str] = w.split()
    if len(word) > 1:
        return d.join(word)
    return word[0]
