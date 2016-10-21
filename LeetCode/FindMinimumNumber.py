def findMin(nums):
    """
    :type nums: List[int]
    :rtype: int
    """
    n = len(nums)
    if n == 1:
        return nums[0]
    for i in range(1, n):
        if nums[i] < nums[i - 1]:
            return nums[i]
    return nums[0]

def findMin(nums):
    """
    Binary search
    :type nums: List[int]
    :rtype: int
    """
    left = 0
    right = len(nums) - 1
    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] > nums[right]:
            left = mid + 1
        else:
            right = mid
    return nums[left]