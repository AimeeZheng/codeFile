package zyl.leetCode;

import java.util.ArrayList;
import java.util.List;

public class LSWRC1 {
	public int lengthOfLongestSubstring(String s) {
		int max = 0;
		int len = 0;
		boolean repeat = false;
		int n = s.length();

		for (int i = 0; i < n; i++) {
			List<Character> list = new ArrayList<Character>();
			for (int j = i; j < n; j++) {
				Character ch = new Character(s.charAt(j));
				if (!list.contains(ch))
					list.add(ch);
				else {
					len = list.size();
					repeat = true;
					break;
				}
			}
			if (!repeat)
				len = n - i;
			max = Math.max(len, max);
		}
		return max;
	}

	public static void main(String arg[]) {
		LSWRC1 lswrc = new LSWRC1();
		String s = "abcb";
		String s1 = "abcabca";
		String s2 = "aaabcabceksa";
		String s3 = "";
		String s4 = "abcde";
		System.out.println(lswrc.lengthOfLongestSubstring(s));
		System.out.println(lswrc.lengthOfLongestSubstring(s1));
		System.out.println(lswrc.lengthOfLongestSubstring(s2));
		System.out.println(lswrc.lengthOfLongestSubstring(s3));
		System.out.println(lswrc.lengthOfLongestSubstring(s4));
	}
}
