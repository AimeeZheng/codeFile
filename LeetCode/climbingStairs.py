def climbStairs(self, n):
    """
    :type n: int
    :rtype: int
    """
    a = 0
    b = 1
    for i in range(n):
        cnt = a + b
        a = b
        b = cnt
    return cnt