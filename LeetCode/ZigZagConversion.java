package zyl.leetCode;

/**
 * The string "PAYPALISHIRING" is written in a zigzag pattern on a given number
 * of rows like this: (you may want to display this pattern in a fixed font for
 * better legibility)
 * 
 * @author zhengyaolin
 * 
 */
public class ZigZagConversion {

	public static String convert(String s, int numRows) {
		int n = s.length();
		char[] a = s.toCharArray();
		int h = numRows * 2 - 2;
		// 列数
		int col = 0;
		if (n - h * n / h > numRows)
			col = n / h + 2;
		else {
			col = col + 1;
		}
		char[] ch = new char[n];
		for (int i = 0; i < n; i++) {
			// 第一行
			if (i <= col / 2)
				ch[i] = a[i * h];
			// 第二到row-1行

		}
		return ch.toString();
	}

	public static void main(String args[]) {
		String s = "PAYPALISHIRING";
		convert(s, 3);
	}
}
