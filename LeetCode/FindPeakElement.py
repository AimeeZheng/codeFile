def findPeakElement(nums):
    """
    :type nums: List[int]
    :rtype: int
    """
    n = len(nums)
    if n == 1:
        return 0
    slope = []
    positive = False
    negative = False
    for i in range(n - 1):
        k = nums[i + 1] - nums[i]
        if k > 0:
            positive = True
        else:
            negative = True
        slope.append(k)
    if positive and not negative:
        return n - 1
    if negative and not positive:
        return 0
    for i in range(1, n - 1):
        if slope[i] < 0 and slope[i - 1] > 0:
            return i
    if nums[0] > nums[n - 1]:
        return 0
    else:
        return n - 1

def findPeakElement1(nums):
    """
    :type nums: List[int]
    :rtype: int
    """
    n = len(nums)
    for i in range(1, n):
        if nums[i] < nums[i - 1]:
            return i - 1
    return n - 1

def findPeakElement2(nums):
    """
    Binary search
    :type nums: List[int]
    :rtype: int
    """
    left = 0
    right = len(nums) - 1
    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] < nums[mid + 1]:
            left = mid + 1
        else:
            right = mid
    return left
        