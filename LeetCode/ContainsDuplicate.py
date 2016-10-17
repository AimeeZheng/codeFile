def containsDuplicate(nums):
    """
    :type nums: List[int]
    :rtype: bool
    """
    filted = set(nums)
    if len(filted) < len(nums):
        return True
    return False

def containsDuplicate1(nums):
    """
    :type nums: List[int]
    :rtype: bool
    """
    container = set()
    for i in nums:
        if i in container:
            return True
        container.add(i)
    return False

def containsNearbyDuplicate(self, nums, k):
    """
    :type nums: List[int]
    :type k: int
    :rtype: bool
    """
    n = len(nums)
    tmp = dict()
    for i in range(n):
        num = nums[i]
        if i > k:
            tmp.pop(nums[i - k - 1], None)
        if num in tmp:
            return True
        else:
            tmp[num] = 1
    return False

    