package zyl.leetCode;

/**
 * Given an array of integers, return indices of the two numbers such that they
 * add up to a specific target.
 * 
 * @author zhengyaolin
 * 
 */

public class TwoSum1 {
	public int[] twoSum(int[] nums, int target) {
		int n = nums.length;
		int[] indices = new int[2];
		for (int i = 0; i < n; i++) {
			for (int j = i + 1; j < n; j++) {
				if (nums[j] == target - nums[i]) {
					indices[0] = i;
					indices[1] = j;
				}
			}
		}
		return indices;
	}

	public static void main(String[] args) {
		TwoSum1 testTwoSum = new TwoSum1();
		int[] nums = { 3, 2, 4 };
		int[] results = testTwoSum.twoSum(nums, 6);
		System.out.println("[" + results[0] + ", " + results[1] + "]");
	}
}
