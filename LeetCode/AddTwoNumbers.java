package zyl.leetCode;

/**
 * You are given two linked lists representing two non-negative numbers. The
 * digits are stored in reverse order and each of their nodes contain a single
 * digit. Add the two numbers and return it as a linked list.
 * 
 * @author zhengyaolin
 * 
 */

public class AddTwoNumbers {
	class ListNode {
		int val;
		ListNode next;

		ListNode(int x) {
			val = x;
		}
	}

	public ListNode addTwoNumbers(ListNode l1, ListNode l2) {
		ListNode resultHead = null;
		ListNode resultNode = null;
		ListNode n1 = l1;
		ListNode n2 = l2;
		int carry = 0;
		while (n1 != null || n2 != null) {
			int sum = carry;
			// 不等长
			if (n1 != null) {
				sum += n1.val;
				n1 = n1.next;
			}
			if (n2 != null) {
				sum += n2.val;
				n2 = n2.next;
			}
			// 进位
			if (sum >= 10) {
				carry = 1;
				sum = sum % 10;
			} else {
				carry = 0;
			}

			// 结果
			ListNode item = new ListNode(sum);
			if (resultHead == null) {
				resultHead = item;
			} else {
				resultNode.next = item;
			}
			resultNode = item;
		}
		if (carry != 0) {
			resultNode.next = new ListNode(1);
		}
		return resultHead;
	}

}
