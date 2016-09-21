package zyl.leetCode;

import java.util.HashMap;

public class TwoSum {
	public int[] twoSum(int[] A, int sum) {
		int n = A.length;
		int[] indices = new int[2];
		HashMap<Integer, Integer> b = new HashMap<Integer, Integer>();
		for (int i = 0; i < n; i++) {
			if (!b.containsKey(sum - A[i]))
				b.put(A[i], i);
			else {
				indices[0] = b.get(sum - A[i]);
				indices[1] = i;
			}
		}
		return indices;
	}

	public static void main(String[] args) {
		TwoSum testTwoSum = new TwoSum();
		int[] nums = { 3, 2, 4 };
		int[] results = testTwoSum.twoSum(nums, 6);
		System.out.println("[" + results[0] + ", " + results[1] + "]");
	}
}
