
class Error(Exception):
    def __init__(self, fn, ln):
        self.message = f'Something went wrong'
        self.file_name = fn
        self.line_number = ln

    def __str__(self) -> str:
        return f'{self.message}: {self.file_name}:{self.line_number}'

    def __repr__(self) -> str:
        return self.__str__()


class NotEnoughOperantsError(Error):
    def __init__(self, fn, ln, count):
        super().__init__(fn, ln)
        self.message = f'Not Enough Operants (Required {count})'

    def __str__(self) -> str:
        return super().__str__()

    def __repr__(self) -> str:
        return super().__repr__()


class InvalidSyntaxError(Error):
    def __init__(self, fn, ln, token):
        super().__init__(fn, ln)
        self.message = f'Invalid Syntax'
        self.token = token

    def __str__(self) -> str:
        return super().__str__() + f' {self.token}'

    def __repr__(self) -> str:
        return super().__repr__() + f' {self.token}'


class NotDefinedError(Error):
    def __init__(self, fn, ln, name):
        super().__init__(fn, ln)
        self.name = name
        self.message = f'Word is not defined - {self.name}'

    def __str__(self) -> str:
        return super().__str__()

    def __repr__(self) -> str:
        return super().__repr__()
