
public class Ex3_10 {

	public static void main(String[] args) {
		long a = 1_000_000 * 1_000_000;
		long b = 1_000_000 * 1_000_000L;
		
		System.out.println("a="+a); // 오버플로우 발생
		System.out.println("b="+b);
	}
}
