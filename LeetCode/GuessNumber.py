def guessNumber(n):
    """
    Binary Search
    :type n: int
    :rtype: int
    """
    low = 1
    high = n + 1
    while low < high:
        mid = low + (high - low) // 2
        res = guess(mid)
        if res == 1:
            low = mid + 1
        elif res == -1:
            high = mid
        else:
            return mid
    return low