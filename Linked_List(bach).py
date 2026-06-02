class Node():
    def __init__(self,data,next):
        self.data = str(data)
        self.next = None

class LinkedList():
    def __init__(self):
        self.head = None
 
    def insert(self,data):
        if not self.head:
            self.head = Node(data,None)
            return 
        cur = self.head
        while cur.next != None:
            cur = cur.next
        cur.next = Node(data,self.head)

    def delete(self,data):
        if self.head == None:
            return "Empty list"
        elif self.head.data == data:
            self.head = self.head.next
            return print("Deleted" )
        else:
            cur = self.head
            while cur is not None:
                if cur.next.data != data:
                    cur = cur.next
                else:
                    cur.next = cur.next.next
                    cur = cur.next
                    return print("Deleted" )
            return print("No exist")

    def show(self):
        cur = self.head
        temp = ""
        while cur.next is not None:
            temp += str(cur.data)
            cur = cur.next
        print(temp + str(cur.data))
