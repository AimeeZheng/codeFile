def removeElement(nums, val):
    """
    :type nums: List[int]
    :type val: int
    :rtype: int
    """
    n = len(nums)
    tmp = []
    for i in range(n):
        if nums[i] == val:
            n -= 1
            tmp.append(i)
        else:
            if len(tmp) > 0:
                nums[tmp[0]] = nums[i]
                tmp = tmp[1:]
                tmp.append(i)
    print(nums[:n])
    return n