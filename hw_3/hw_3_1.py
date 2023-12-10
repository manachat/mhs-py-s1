import numpy as np


class Matrix():

    def __init__(self, matrix) -> None:
        if type(matrix) != np.ndarray:
            raise ValueError('need numpy')
        if len(matrix.shape) != 2:
            raise ValueError('not a matrix')
        self.matrix = matrix
        self.h = matrix.shape[0]
        self.w = matrix.shape[1]

    # +
    def __add__(self, other):
        if self.h != other.h:
            raise ValueError(f'height mismatch {self.h} {other.h}')
        if self.w != other.w:
            raise ValueError(f'width mismatch {self.w} {other.w}')
        res = np.ndarray(shape=self.matrix.shape)
        for i in range(self.h):
            for j in range(self.w):
                res[i][j] = self.matrix[i][j] + other.matrix[i][j]

        return Matrix(res)
        

    # *
    def __mul__(self, other):
        if self.h != other.h:
            raise ValueError(f'height mismatch {self.h} {other.h}')
        if self.w != other.w:
            raise ValueError(f'width mismatch {self.w} {other.w}')
        res = np.ndarray(shape=self.matrix.shape)
        for i in range(self.h):
            for j in range(self.w):
                res[i][j] = self.matrix[i][j] * other.matrix[i][j]
        
        return Matrix(res)

    # @
    def __matmul__(self, other):
        if self.w != other.h:
            raise ValueError(f'dimensions mismatch {self.w} {other.h}')
        res = np.ndarray(shape=(self.h, other.w))
        h_lim = self.h
        w_lim = other.w
        mul_lim = self.w
        for i in range(h_lim):
            for j in range(w_lim):
                s = 0
                for k in range(mul_lim):
                    s += self.matrix[i][k] * other.matrix[k][j]
                res[i][j] = s
        return Matrix(res)
    
    def __str__(self):
       formated = ['\t'.join([str(int(w)) for w in x]) for x in self.matrix]
       st = '\n'.join(formated)
       return st


def gen_matrix():
    return np.random.randint(0, 10, (10, 10))

def main():
    np.random.seed(0)
    m1 = Matrix(gen_matrix())
    m2 = Matrix(gen_matrix())

    with open('artifacts/3.1/matrix+.txt', 'w') as out:
        out.write(str(m1 + m2))
    with open('artifacts/3.1/matrix*.txt', 'w') as out:
        out.write(str(m1 * m2))
    with open('artifacts/3.1/matrix@.txt', 'w') as out:
        out.write(str(m1 @ m2))



if __name__ == '__main__':
    main()