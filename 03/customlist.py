

class CustomList(list):

    def __init__(self, numeric: list=None) -> None:
        numeric = numeric if numeric is not None else []
        if not isinstance(numeric, list):
            raise TypeError(f'numeric is {type(numeric)}')
        super().__init__(numeric)

    def __str__(self) -> str:
        return super().__str__() + f' sum = {sum(self)}'
    
    def __add__(self, other):
        lenght = min(len(self), len(other))
        result = [self[i] + other[i] for i in range(lenght)]
        result.extend(self[lenght:])
        result.extend(other[lenght:])
        return CustomList(result)
    
    def __sub__(self, other):
        lenght = min(len(self), len(other))
        result = [self[i] - other[i] for i in range(lenght)]
        result.extend(self[lenght:])
        result.extend([-1*val for val in other[lenght:]])
        return CustomList(result)
    
    def __radd__(self, other):
        return self.__add__(other)
    
    def __rsub__(self, other):
        lenght = min(len(self), len(other))
        result = [other[i] - self[i] for i in range(lenght)]
        result.extend(other[lenght:])
        result.extend([-1*val for val in self[lenght:]])
        return CustomList(result)
        
    def __lt__(self, other) -> bool:
        return sum(self) < sum(other)
    
    def __le__(self, other) -> bool:
        return sum(self) <= sum(other)
    
    def __eq__(self, other) -> bool:
        return sum(self) == sum(other)
    
    def __ne__(self, other) -> bool:
        return sum(self) != sum(other)
    
    def __ge__(self, other) -> bool:
        return sum(self) >= sum(other)
    
    def __gt__(self, other) -> bool:
        return sum(self) > sum(other)