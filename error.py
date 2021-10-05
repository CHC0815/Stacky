
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
