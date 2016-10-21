def missingNumber(nums):
    """
    :type nums: List[int]
    :rtype: int
    """
    nums = sorted(nums)
    n = len(nums)
    for i in range(n):
        if nums[i] > i:
            return i
    return n

def missingNumber1(nums):
    return sum(range(len(nums) + 1)) - sum(nums)