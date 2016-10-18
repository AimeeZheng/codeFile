def removeDuplicates(nums):
    """
    :type nums: List[int]
    :rtype: int
    """
    n = len(nums)
    if n < 2:
        return n
    last = nums[0]
    tmp = []
    for i in range(1, n):
        if nums[i] == last:
            tmp.append(i)
            n -= 1
        else:
            last = nums[i]
            if len(tmp) > 0:
                nums[tmp[0]] = nums[i]
                tmp = tmp[1:]
                tmp.append(i)
    #print(nums[:n])
    return n