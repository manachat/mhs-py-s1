import numpy as np
from hw_3_1 import Matrix, gen_matrix

class HashMixin():

    def __get_val__(self):
        pass

    def __hash__(self):
        # я человек простой, вижу матрицу - считаю определитель
        return int(round(np.linalg.det(self.__get_val__())))
    
    def __eq__(self, __value) -> bool:
        if not isinstance(__value, HashMixin):
            return False
        return np.equal(self.__get_val__(), __value.__get_val__()).all()
        

class HashedMatrix(Matrix, HashMixin):

    hash_cache = {}

    def __init__(self, matrix) -> None:
        super().__init__(matrix)

    def __get_val__(self):
        return self.matrix
    
    def __matmul__(self, other):
        mul_hash = self.__hash__() * other.__hash__()
        if mul_hash in HashedMatrix.hash_cache:
            return HashedMatrix.hash_cache[mul_hash]
        else:
            res = super().__matmul__(other)
            HashedMatrix.hash_cache[mul_hash] = res
            return res
        
def print_matrix(matrix, file):
    with open('artifacts/3.3/' + file, 'w') as f:
        f.write(str(matrix))

# 3*9 - 5*6 = 27 - 30 = -3
# 3*7 - 4 * 6 = 21 - 24 = -3
def main():
    A = HashedMatrix(np.asarray([[5, 3], [9, 6]]))
    C = HashedMatrix(np.asarray([[4, 3], [7, 6]]))
    B = HashedMatrix(np.asarray([[1, 0], [0, 1]]))
    D = HashedMatrix(np.asarray([[1, 0], [0, 1]]))
    assert(A != C)
    assert(A.__hash__() == C.__hash__())
    assert(B == D)

    print_matrix(A, 'A.txt')
    print_matrix(B, 'B.txt')
    print_matrix(C, 'C.txt')
    print_matrix(D, 'D.txt')
    
    AB = A @ B
    CD = C @ D
    HashedMatrix.hash_cache = {}
    real_CD = C @ D
    assert(CD != real_CD)

    print_matrix(AB, 'AB.txt')
    print_matrix(real_CD, 'CD.txt')
    with open('artifacts/3.3/hash.txt', 'w') as f:
        # mul не hashed
        f.write(str(AB.__hash__()))
        f.write(str(real_CD.__hash__()))
    
    


if __name__ == '__main__':
    main()