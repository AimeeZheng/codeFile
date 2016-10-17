def rotate0(nums, k):
    """
    Exceed Time limit
    """
    n = len(nums)
    if n < 2 or k == 0:
   	    return
    cnt = 0
    while cnt < k:
        tmp = nums[n - 1]
        for i in range(n-1, 0, -1):
            nums[i] = nums[i - 1]
        nums[0] = tmp
        cnt += 1

def rotate1(nums, k):
    """
    :type nums: List[int]
    :type k: int
    :rtype: void Do not return anything, modify nums in-place instead.
    """
    n = len(nums)
    if k == 0:
        return
    if k % n == 0:
        return
    k = k % n
    tmp = nums[n-k:n]
    for i in range(n-1, k-1, -1):
        nums[i] = nums[i - k]
    for i in range(k):
        nums[i] = tmp[i]

def rotate2(nums, k):
    """
    Equal operation: 3 times reverse
    """
    n = len(nums)
    if k == 0:
        return
    if k % n == 0:
        return
    k = k % n
    reverse(nums, 0, n-k-1)
    reverse(nums, n-k, n-1)
    nums.reverse()
 
def reverse(nums, i, j):
    while i < j:
        tmp = nums[i]
        nums[i] = nums[j]
        nums[j] = tmp
        i += 1
        j -= 1
    