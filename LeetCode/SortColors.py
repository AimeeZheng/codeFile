def sortColors(nums):
    """
    Note: 2 traversals
    :type nums: List[int]
    :rtype: void Do not return anything, modify nums in-place instead.
    """
    r = 0
    w = 0
    b = 0
    for i in nums:
        if i == 0:
            r += 1
        elif i == 1:
            w += 1
        else:
            b += 1
    
    for i in range(len(nums)):
        if i < r:
            nums[i] = 0
        elif i < r + w:
            nums[i] = 1
        else:
            nums[i] = 2

def sortColors2(nums):
    """
    Note: 1 traversals
    """
    n = len(nums)
    i = 0
    r = 0
    b = 0
    while i < n - b:
        if nums[i] == 0:
            swap(nums, i, r)
            r += 1
        if nums[i] == 2:
            b += 1
            swap(nums, i, -b)
            i -= 1
        i += 1

def swap(nums, i, j):
    tmp = nums[i]
    nums[i] = nums[j]
    nums[j] = tmp