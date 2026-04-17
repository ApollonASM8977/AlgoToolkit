package csc;

public class FindMax {

	public static void main(String[] args) {

		int[] array = { 12, 5, 6, 78, 9 };

		int max = array[0];

		for (int i = 0; i < array.length; i++) {
			if (max < array[i])
				max = array[i];
		}

		System.out.println("max: " + max);

	}

}
