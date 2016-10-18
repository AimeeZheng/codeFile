def majorityElement(nums):
    """
    :type nums: List[int]
    :rtype: int
    """
    n = len(nums)
    if n == 1:
        return nums[0]
    nums = sorted(nums)
    cnt = 1
    last = nums[0]
    for num in nums[1:]:
        if num == last:
            cnt += 1
        else:
            if cnt > n//2:
                return last
            last = num
            cnt = 1
    if cnt > n//2:
        return last