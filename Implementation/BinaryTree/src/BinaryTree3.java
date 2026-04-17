
public class BinaryTree3
{
    private Node root;
    public BinarysearchTree()
    {
        root =null;
    }
    public static class Node 
    {
        int data;
        Node left;
        Node right;
        public final Node nil = null;
        public Node ( int newData , Node oldLT , Node oldRT)
        {
            data = newData;
            left =  oldLT;
            right =  oldRT;
        }
        public Node ( int newData )
        {
            data = newData;
            left = nil;
            right = nil;
        }
        public void display ()
        {
            System.out.println(data+"");
        }   
    }
    
    public void insert (int i)
    {
        root = insert(root , i);

    }
    public Node insert ( Node node , int data)
    {
        if (node == null)
        {
            return new Node(data);
        }
        if (data < node.data)
        {
            node.left = insert(node.left , data);
        }
        else if(data > node.data)  
        {  
            node.right = insert(node.right, data);  
        }  
        return node; 
    }
     // Search node in binary search tree  
    public Node find(int searchedData)  
    {  
        Node current = root;  
        while(current.value != searchedData)  
        {  
        if(searchedData < current.data)  
            // Move to the left if searched value is less  
            current = current.left;  
        else  
            // Move to the right if searched value is >=  
            current = current.right;  
        if(current == null)  
        {  
            return null;  
        }  
        }  
        return current;  
    }  
     // For traversing in order  
  public void inOrder(Node node)  
  {  
    if(node != null)  
    {  
      inOrder(node.left);  
      node.displayData();  
      inOrder(node.right);  
    }  
  }  
  // Preorder traversal  
  public void preOrder(Node node)  
  {  
    if(node != null){  
      node.displayData();  
      preOrder(node.left);             
      preOrder(node.right);  
    }  
  }  
  // Postorder traversal  
  public void postOrder(Node node)  
  {  
    if(node != null)  
    {  
      postOrder(node.left);  
      postOrder(node.right);  
      node.displayData();            
    }  
  }  
  public static void main(String[] args)   
  {  
    BinaryTree a = new BinarySearchTest();  
    a.insert(34);  
    a.insert(56);  
    a.insert(12);  
    a.insert(89);  
    a.insert(67);  
    a.insert(90);  
    System.out.println("Inorder traversal of binary tree");  
    a.inOrder(a.root);  
    System.out.println();  
    System.out.println("Preorder traversal of binary tree");  
    a.preOrder(a.root);  
    System.out.println();  
    System.out.println("Postorder traversal of binary tree");  
    a.postOrder(a.root);  
    System.out.println();  
  }  
}  

    
    

}

