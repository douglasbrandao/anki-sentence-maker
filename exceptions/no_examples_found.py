class NoExamplesFound(Exception):
    def __init__(self, message="No examples were found on WordHippo"):
        super().__init__(message)
