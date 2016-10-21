def twoSum(nums, target):
    """
    :type nums: List[int]
    :type target: int
    :rtype: List[int]
    """
    n = len(nums)
    dic = dict()
    for i in range(n):
        if target - nums[i] in dic:
            return [i, dic[target - nums[i]]]
        dic[nums[i]] = i

def twoSum2(numbers, target):
    """
    :type numbers: List[int]
    :type target: int
    :rtype: List[int]
    """
    n = len(numbers)
    d = dict()
    for i in range(n):
        if target - numbers[i] in d:
            return [d[target - numbers[i]] + 1, i + 1]
        d[numbers[i]] = i