def thirdMax(nums):
    """
    without using sort or set
    :type nums: List[int]
    :rtype: int
    """
    n = len(nums)
    max_1 = nums[0]
    for i in range(1, n):
        max_1 = max(max_1, nums[i])
    if n < 3:
        return max_1
    flag = False
    for i in range(n):
        if nums[i] < max_1 and not flag:
            max_2 = nums[i]
            flag = True
        if nums[i] < max_1 and nums[i] > max_2:
            max_2 = nums[i]
    if not flag:
       return max_1
    flag = False
    for i in range(n):
        if nums[i] < max_2 and not flag:
            max_3 = nums[i]
            flag = True
        if nums[i] < max_2 and nums[i] > max_3:
            max_3 = nums[i]
    if not flag:
       return max_1
    return max_3