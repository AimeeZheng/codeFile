def maxRotateFunction(self, A):
    """
    :type A: List[int]
    :rtype: int
    """
    n = len(A)
    if n == 0:
        return 0
    f = sum(i * e for i, e in enumerate(A))
    A_sum = sum(A)
    result = f
    for k in range(1, n):
        f += A_sum - n * A[n - k]
        result = max(result, f)
    return result