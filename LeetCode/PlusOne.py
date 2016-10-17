def plusOne(self, digits):
    """
    :type digits: List[int]
    :rtype: List[int]
    """
    n = len(digits)
    result = []
    c = 0
    for i in range(n - 1, -1, -1):
        tmp = 0
        d = digits[i]
        if i == n - 1:
            tmp = d + 1
        else:
            tmp = d + c
            
        if tmp > 9:
            tmp = tmp % 10
            c = 1
        else:
            c = 0
        result.append(tmp)
    if c == 1:
        result.append(1)
    result.reverse()
    return result