import java.util.*;

public class Ex11_7 {

	public static void main(String[] args) {
		String[] strArr = {"cat", "Dog", "Lion", "tiger"};
		
		Arrays.sort(strArr);
		System.out.println("strArr=" + Arrays.toString(strArr));
		
		Arrays.sort(strArr, String.CASE_INSENSITIVE_ORDER); // 대소문자 구분x
		System.out.println("strArr=" + Arrays.toString(strArr));
		
		Arrays.sort(strArr, new Descending()); // 역순 정렬
		System.out.println("strArr=" + Arrays.toString(strArr));
	}
}

class Descending implements Comparator {
	public int compare(Object o1, Object o2) {
		if (o1 instanceof Comparable && o2 instanceof Comparable) {
			Comparable c1 = (Comparable)o1;
			Comparable c2 = (Comparable)o2;
			return c1.compareTo(c2)*-1; // 기본 정렬방식의 역으로 변경(c2.compareTo(c1)과 동일)
		}
		return -1;
	}
}