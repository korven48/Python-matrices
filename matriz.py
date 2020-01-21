from copy import deepcopy

def create_matrix(x, y=False, content=0):
    if not y: y = x
    matrix = [[content for _ in range(x)] for _ in range(y)]
    return Matriz(matrix)

class Matriz():
    def __init__(self, lista):
        if not isinstance(lista, list):
            raise TypeError('Only lists')
            
        self.matrix = lista
        
        y = len(self.matrix)
        x = len(self.matrix[0])
        self.size = x, y
        
    def __repr__(self):
        return f'Matriz({self.matrix})'
    
    def __len__(self):
        return len(self.matrix)
    
    def __getitem__(self, item):
        return self.matrix[item]

        
    def __round__(self, n):
        final = create_matrix(*self.size)
        n, m = self.size
        for i in range(m):
            for j in range(n):
                final[i][j]  = round(self[i][j], n)
        return final
        
    
    def __add__(self, other):
        if self.size != other.size:
            raise ValueError('Sizes must be equal in matrix sumation')

        final = create_matrix(*self.size)
        n, m = self.size
        for i in range(m):
            for j in range(n):
                final[i][j] = self[i][j] + other[i][j]
        return final
    
    def __sub__(self, other):
        if self.size != other.size:
            raise ValueError('Sizes must be equal in matrix subtraction')

        final = create_matrix(*self.size)
        n, m = self.size
        for i in range(m):
            for j in range(n):
                final[i][j] = self[i][j] - other[i][j]
        return final
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return self.scalar_mul(other)
        elif isinstance(other, Matriz):        #This may not work when module imported
            return self.dot_prod(other)
        else:
            raise TypeError(f'Cannot multiply {other} by matrix')
    
    def __rmul__(self, other):
        if isinstance(other, (int, float)):
            return self.scalar_mul(other)
        elif isinstance(other, Matriz):        #This may not work when module imported
            return self.dot_prod(other)
        else:
            raise TypeError(f'Cannot multiply {other} by matrix')
    
    
    def to_list(self):
        return deepcopy(self.matrix)
    
    def item(self):
        if self.size != (1, 1):
            raise ValueError('Only for 1x1 matrices')
        return self[0][0]


    def scalar_mul(self, x):
        final = create_matrix(*self.size)
        n, m = self.size
        for i in range(m):
            for j in range(n):
                final[i][j] = x * self[i][j]
        return final
            
    
    def dot_prod(self, other):
        (n1, m1), (n2, m2) = self.size, other.size
        if n1 != m2:
            raise ValueError(
                f'Matrix multiplication cannot be performed with matrices of size: {self.size}, {other.size}')

        final = create_matrix(n2, m1)
        for i in range(m1):
            for j in range(n2):
                final[i][j] = sum(self[i][index] * other[index][j] for index in range(n1))
        return final
    
    def transpose(self):
        x, y = self.size
        final = create_matrix(y, x)
        for i in range(x):
            for j in range(y):
                final[i][j] = self[j][i]
        return final
    
    def cofactor(self, y, x):
        final = self.to_list()
        del final[y]
        for i in range(len(final)):
            del final[i][x]
        final = Matriz(final)
        return final.determinant()

    
    def adjunto(self, y, x):
        if (x+y)%2 == 0:
            return self.cofactor(y, x) 
        else:
            return -self.cofactor(y, x)
    
    
    def determinant(self):
        if self.size != self.size[::-1]:
            raise ValueError('Determinant is not defined for non square matrices')

        if not isinstance(self, Matriz):
            raise TypeError(f'Determinant is not defined for {type(self)}, it must be a Matriz')

        if len(self) == 1:
            return self.item()

        row = self[0]
        total = 0
        for i, element in enumerate(row):
            total += element * self.adjunto(0, i)
        return total
    
    def cof(self):
        ''' Cofactor matrix: wrongly called matriz adjunta, it really is the '''
        final = create_matrix(*self.size)
        n, m = self.size
        for i in range(m):
            for j in range(n):
                final[i][j] = self.adjunto(i, j)
        return final
    
    def adjugate(self):
        return self.cof().transpose()
    
    def has_inverse(self):
        if self.determinant() == 0:
            return False
        else:
            return True
    
    def inverse(self):
        if not self.has_inverse():
            raise ValueError('This matrix does not have an inverse')
        # inverse = 1/det * traspuesta(adjunta(self))
        final = 1/self.determinant() * self.adjugate()
        return final