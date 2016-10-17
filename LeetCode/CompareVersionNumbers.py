class Solution(object):
    def compareVersion(self, version1, version2):
        """
        :type version1: str
        :type version2: str
        :rtype: int
        """
        v1 = version1.split('.')
        v2 = version2.split('.')
        l1 = len(v1)
        l2 = len(v2)
        n = max(l1, l2)
        for i in range(n):
            num1 = int(v1[i])
            num2 = int(v2[i])
            if num1 > num2:
                return 1
            elif num1 < num2:
                return -1
            elif i + 2 > l2 and i + 2 <= l1:
                for j in v1[i + 1:]:
                    if int(j) != 0:
                        return 1
                return 0
            elif i + 2 > l1 and i + 2 <= l2:
                for j in v2[i + 1:]:
                    if int(j) != 0:
                        return -1
                return 0
        return 0