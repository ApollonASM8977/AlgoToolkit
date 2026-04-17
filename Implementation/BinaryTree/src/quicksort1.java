import java.util.Scanner;

public class quicksort1
{
    static int partition (int [] E , int first , int last)
    {
        int low ;
        int high ;
        low = first ;
        high = last ; 
        int i = ( low + 1); // index of smaller element and my pivot
        for (int j=i ; j <= high ; j++) 
        {
            while (j < high && E[j]<E[low])
            j++; // this one is checking from the left to the right
            while (high > low && E[high]>E[low])
            high--;// this one is checking from the right to the left
            if (j < high) 
            {
                int temp = E[j];
                E[j] = E[high];
                E[high] = temp;
            }
            else 
            break;
        }
        int temp = E[low];
        E[low] = E[high];
        E[high] = temp;
        return high;

    }// the function for sorting the elements
    static void sort (int[] E, int first , int last)
    {
        if (first < last)
        {
            int splitP = partition(E ,first, last);
            sort ( E, first ,splitP-1 );
            sort ( E, splitP+1 , last );


        }
    } // The function for printing 
    public static void print(int E[])
    {
        for (int i = 0; i < E.length; i++)
        {
            System.out.println(E[i]+" ");
        }
    }
    public static void main (String args [])
    {
        int n ,i;
        Scanner s = new Scanner(System.in);
        System.out.println("Enter the numbers of elements : ");
        n=s.nextInt();
        int E [] = new int [n];
        System.out.println("Enter your " + n + " elements ");
        for (i=0; i<n;i++)
        {
            E[i]=s.nextInt();
        }
       
        sort(E, 0, n-1 );
        System.out.println("The sorted array are : ");
        print(E);
    }
}
