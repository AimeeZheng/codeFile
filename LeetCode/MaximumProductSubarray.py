def maxProduct(nums):
    """
    :type nums: List[int]
    :rtype: int
    """
    max_local = nums[0]
    min_local = nums[0]
    Max = nums[0]
    for i in range(1, len(nums)):
        max_tmp = max_local
        max_local = max(max(max_local * nums[i], nums[i]), min_local * nums[i])
        min_local = min(min(max_tmp * nums[i], nums[i]), min_local * nums[i])
        Max = max(Max, max_local)
    return Max