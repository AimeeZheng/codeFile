class NumArray(object):
    def __init__(self, nums):
        """
        initialize your data structure here.
        :type nums: List[int]
        """
        n = len(nums)
        if n > 0:
            self.sum = [0 for i in range(n+1)]
            self.sum[0] = nums[0]
            for i in range(1, n):
                self.sum[i] = self.sum[i-1] + nums[i]

    def sumRange(self, i, j):
        """
        sum of elements nums[i..j], inclusive.
        :type i: int
        :type j: int
        :rtype: int
        """
        if i == 0:
            return self.sum[j]
        return self.sum[j] - self.sum[i - 1]