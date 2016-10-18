def generate(numRows):
    """
    :type numRows: int
    :rtype: List[List[int]]
    """
    result = []
    L = [1]
    while len(L) <= numRows:
        L.append(0)
        result.append(L[:-1])
        L = [L[i - 1] + L[i] for i in range(len(L))]
    return result

def getRow(rowIndex):
    """
    :type rowIndex: int
    :rtype: List[int]
    """
    L = [1]
    if rowIndex = 1:
        return 
    while len(L) <= rowIndex:
        L.append(0)
        L = [L[i - 1] + L[i]  for i in range(len(L))]
    return L
