#!/usr/bin/python3
def square_matrix_map(matrix=[]):
    return list(map(lambdai x: list(map(lambda n: n * n, x)), matrix))
