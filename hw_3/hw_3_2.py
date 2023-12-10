from re import S
from typing import Any, Literal as L
import numpy as np
from numpy import ufunc

class FileOutMixin():
    def __get_val__(self):
        pass

    def writeFile(self, filename):
        with open(filename, 'w') as f:
            f.write(str(self.__get_val__()))

class StrMixin():
    def __get_val__(self) -> Any:
        pass

    def __str__(self):
        formated = ['\t'.join([str(int(w)) for w in x]) for x in self.__get_val__()]
        st = '\n'.join(formated)
        return st



class MyVal(np.lib.mixins.NDArrayOperatorsMixin, StrMixin, FileOutMixin):

    def __init__(self, matrix):
        if type(matrix) != np.ndarray:
            raise ValueError('need numpy')
        if len(matrix.shape) != 2:
            raise ValueError('not a matrix')
        self.matrix = matrix
        self.h = matrix.shape[0]
        self.w = matrix.shape[1]

    _HANDLED_TYPES = (np.ndarray, )

    def __array_ufunc__(self, ufunc: ufunc, method: L['__call__', 'reduce', 'reduceat', 'accumulate', 'outer', 'inner'], *inputs: Any, **kwargs: Any) -> Any:
        out = kwargs.get('out', ())
        for x in inputs + out:
            
            if not isinstance(x, (np.ndarray, MyVal)):
                return NotImplemented

        inputs = tuple(x.value if isinstance(x, MyVal) else x
                       for x in inputs)
        if out:
            kwargs['out'] = tuple(
                x.value if isinstance(x, MyVal) else x
                for x in out)
        result = getattr(ufunc, method)(*inputs, **kwargs)

        if type(result) is tuple:
            # multiple return values
            return tuple(type(self)(x) for x in result)
        elif method == 'at':
            # no return value
            return None
        else:
            # one return value
            return type(self)(result)
    
    def __get_val__(self):
        return self.matrix
    
    @property
    def value(self):
        return self.matrix
    
    @value.setter
    def value(self, new_value):
        self._matrix = new_value

def main():
    np.random.seed(0)
    v = MyVal(np.random.randint(0, 10, (10, 10)))
    v1 = MyVal(np.random.randint(0, 10, (10, 10)))
    (v + v1).writeFile('artifacts/3.2/sum.txt')
    (v * v1).writeFile('artifacts/3.2/mul.txt')
    (v @ v1).writeFile('artifacts/3.2/matmul.txt')

if __name__ == '__main__':
    main()
