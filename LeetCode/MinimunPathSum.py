def minPathSum(grid):
    """
    :type grid: List[List[int]]
    :rtype: int
    """
    m = len(grid)
    n = len(grid[0])
    min_sum = [[0 for i in range(n)] for j in range(m)]
    for i in range(m):
        for j in range(n):
            if i == 0 and j == 0:
                min_sum[i][j] = grid[i][j]
                continue
            if i == 0:
                min_sum[i][j] = min_sum[i][j - 1] + grid[i][j]
            elif j == 0:
                min_sum[i][j] = min_sum[i - 1][j] + grid[i][j]
            else:  
                min_sum[i][j] = min(min_sum[i - 1][j] + grid[i][j], min_sum[i][j - 1] + grid[i][j])
    print(min_sum)
    return min_sum[m - 1][n - 1]