package zyl.leetCode;

import java.util.HashMap;
import java.util.Map;

/**
 * Given a string, find the length of the longest substring without repeating
 * characters. For example, the longest substring without repeating letters for
 * "abcabcbb" is "abc", which the length is 3. For "bbbbb" the longest substring
 * is "b", with the length of 1.
 * 
 * @author zhengyaolin
 * 
 */

public class LSWRC {
	public int lengthOfLongestSubstring(String s) {
		int slow = 0;
		int fast = 0;
		int max = 0;
		Map<Character, Integer> map = new HashMap<Character, Integer>();

		while (fast < s.length()) {
			char ch = s.charAt(fast);

			if (slow == fast) {
				map.put(ch, fast);
				fast++;
				continue;
			}

			if (!map.containsKey(ch)) {
				map.put(ch, fast);
				fast++;
			} else {
				max = Math.max(max, fast - slow);
				int newSlow = map.get(ch) + 1;
				// remove chars
				for (int i = slow; i < newSlow; i++) {
					map.remove(s.charAt(i));
				}
				slow = newSlow;
			}
		}
		return Math.max(max, fast - slow);
	}

	public static void main(String arg[]) {
		LSWRC lswrc = new LSWRC();
		String s = "abcb";
		System.out.println(lswrc.lengthOfLongestSubstring(s));
	}
}
