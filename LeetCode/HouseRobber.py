def rob(nums):
    """
    :type nums: List[int]
    :rtype: int
    """
    n = len(nums)
    if n < 1:
        return 0
    if n == 1:
        return nums[0]
    money = [0 for i in range(n)]
    money[0] = nums[0]
    money[1] = max(nums[0], nums[1])
    for i in range(2, n):
        money[i] = max(money[i - 2] + nums[i], money[i - 1])
    return money[n - 1]