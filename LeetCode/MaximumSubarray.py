def maxSubArray(nums):
    """
    :type nums: List[int]
    :rtype: int
    """
    loc = nums[0]
    glo = nums[0]
    for i in range(1, len(nums)):
        loc = max(loc + nums[i], nums[i])
        glo = max(glo, loc)
    return glo