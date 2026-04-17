public class IntList 
{
    int element;
    IntList next;
    public final IntList nil=null;
    public IntList (int newElement, IntList oldList)
    {
        element=newElement;
        next=oldList;
    }
    public IntList (int newElement )
    {
        element=newElement;
        next=nil;
    }
    public int first ()
    {
        return element;
    }
    public IntList rest()
    {
        return next; 
    }
}
