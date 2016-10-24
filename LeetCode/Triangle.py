def minimumTotal(triangle):
    """
    Note: DP  O(n*n/2) space, top-down
    :type triangle: List[List[int]]
    :rtype: int
    """
    n = len(triangle)
    min_sum = [[0 for i in range(r + 1)] for r in range(n)]
    min_sum[0][0] = triangle[0][0]
    for i in range(1, n):
        for j in range(i + 1):
            if j == 0:
                min_sum[i][j] = min_sum[i - 1][j] + triangle[i][j]
            elif j == i:
                min_sum[i][j] = min_sum[i - 1][j - 1] + triangle[i][j]
            else:
                min_sum[i][j] = min(min_sum[i - 1][j - 1] + triangle[i][j], min_sum[i - 1][j] + triangle[i][j])
    return min(min_sum[n - 1])

def minimumTotal2(triangle):
    """
    Note: DP  bottom-up, O(n) space
    :type triangle: List[List[int]]
    :rtype: int
    """
    n = len(triangle)
    min_sum = triangle[-1]
    for i in range(n - 2, -1, -1):
        for j in range(i + 1):
            min_sum[j] = min(min_sum[j], min_sum[j + 1]) + triangle[i][j]
    return min_sum[0]

