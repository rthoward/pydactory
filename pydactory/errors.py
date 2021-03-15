class PydactoryError(Exception):
    pass


class NoDefaultGeneratorError(Exception):
    def __init__(self, key=None, type_=None):
        self.key = key
        self.type = type_
        self.message = f"Default of type {type_} could not be generated for key {key}."
        super().__init__(self.message)
