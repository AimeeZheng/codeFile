class Solution(object):
    def moveZeroes(self, nums):
        """
        :type nums: List[int]
        :rtype: void Do not return anything, modify nums in-place instead.
        """
        n = len(nums)
        if n < 2:
            return
        zeros = []
        cnt = 0
        for i in range(n):
            if nums[i] == 0:
                cnt += 1
                zeros.append(i)
            else:
                if len(zeros) > 0:
                    nums[zeros[0]] = nums[i]
                    zeros.append(i)
                    zeros = zeros[1:]
        for i in range(n - cnt, n):
            nums[i] = 0