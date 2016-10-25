def intersection(nums1, nums2):
    """
    Using hash map
    :type nums1: List[int]
    :type nums2: List[int]
    :rtype: List[int]
    """
    result = []
    if len(nums1) == 0 or len(nums2) == 0:
        return result
    m = dict()
    for i in set(nums1):
        m[i] = 1
    for i in set(nums2):
        if i in m:
            result.append(i)
    return result

def intersection2(nums1, nums2):
    """
    Binary search
    :type nums1: List[int]
    :type nums2: List[int]
    :rtype: List[int]
    """
    result = []
    nums1 = sorted(nums1)
    for num in set(nums2):
        if binarySearch(nums1, num):
            result.append(num)
    return result
            
def binarySearch(nums, target):
    low = 0
    high = len(nums)
    while low < high:
        mid = low + (high - low) // 2
        if nums[mid] < target:
            low = mid + 1
        elif nums[mid] > target:
            high = mid
        else:
            return True
    return False

#contains duplicates
def intersect(nums1, nums2):
    """
    Hash Map
    :type nums1: List[int]
    :type nums2: List[int]
    :rtype: List[int]
    """
    result = []
    m = dict()
    for i in nums1:
        if i in m:
            m[i] += 1
        else:
            m[i] = 1
    for num in nums2:
        if num in m and m[num] > 0:
            result.append(num)
            m[num] -= 1
    return result

