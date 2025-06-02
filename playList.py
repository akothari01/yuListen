class playNode:
    def __init__(self, playLink):
        self.playLink = playLink
        self.next = None
    
class playList:
    def __init__(self):
        self.head = None
    
    def insert(self, playN):
        if self.head == None:
            self.head = playNode(playN)
        else:
            node = self.head
            while node.next != None:
                node = node.next
            node.next = playN

    def insertImmediate(self, playN):
        node = self.head.next
        self.head.next = playNode(playN)
        self.head.next.next = node
    
    def removeCurrent(self):
        self.head = self.head.next
    
    def clearList(self):
        self.head = None

    def printList(self):
        node = self.head
        while node!= None:
            print(node.playLink)
            node = node.next

