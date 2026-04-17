public class ListClient 
{
    public static void main(String[] args)
    {
        IntList L= new IntList(1);
        System.out.println("List L first element: " + L.first());
        System.out.println("List L second element: " + L.rest());
        IntList L1= new IntList(2,L);
        System.out.println("List L first element: " + L1.first());
        System.out.println("List L second element: " + L1.rest().first());
    }
}