class Node:
  def __init__(self, content):
    self.value = content
    self.next = None
    self.previous = None

  def __str__(self):
    return ('CONTENT:{}\n'.format(self.value))

  __repr__=__str__


class ContentItem:
  '''
    >>> content1 = ContentItem(1000, 10, "Content-Type: 0", "0xA")
    >>> content2 = ContentItem(1004, 50, "Content-Type: 1", "110010")
    >>> content3 = ContentItem(1005, 18, "Content-Type: 2", "<html><p>'CMPSC132'</p></html>")
    >>> content4 = ContentItem(1005, 18, "another header", "111110")
    >>> hash(content1)
    0
    >>> hash(content2)
    1
    >>> hash(content3)
    2
    >>> hash(content4)
    1
  '''
  def __init__(self, cid, size, header, content):
    self.cid = cid
    self.size = size
    self.header = header
    self.content = content

  def __str__(self):
    return f'CONTENT ID: {self.cid} SIZE: {self.size} HEADER: {self.header} CONTENT: {self.content}'

  __repr__=__str__

  def __eq__(self, other):
    if isinstance(other, ContentItem):
      return self.cid == other.cid and self.size == other.size and self.header == other.header and self.content == other.content
    return False

  def __hash__(self):
    total_sum = 0      #create the sum 
    for value in self.header:  #literate through the header 
      total_sum += ord(value)    #add the ord of character to the sum
    return total_sum % 3  #at the end modulo by 3 so it can return 0,1,2




class CacheList:
  ''' 
    >>> content1 = ContentItem(1000, 10, "Content-Type: 0", "0xA")
    >>> content2 = ContentItem(1004, 50, "Content-Type: 1", "110010")
    >>> content3 = ContentItem(1005, 180, "Content-Type: 2", "<html><p>'CMPSC132'</p></html>")
    >>> content4 = ContentItem(1006, 18, "another header", "111110")
    >>> content5 = ContentItem(1008, 2, "items", "11x1110")
    >>> lst=CacheList(200)
    >>> lst
    REMAINING SPACE:200
    ITEMS:0
    LIST:
    <BLANKLINE>
    >>> lst.put(content1, 'mru')
    'INSERTED: CONTENT ID: 1000 SIZE: 10 HEADER: Content-Type: 0 CONTENT: 0xA'
     >>> lst.put(content2, 'lru')
    'INSERTED: CONTENT ID: 1004 SIZE: 50 HEADER: Content-Type: 1 CONTENT: 110010'
    >>> lst.put(content4, 'mru')
    'INSERTED: CONTENT ID: 1006 SIZE: 18 HEADER: another header CONTENT: 111110'
    >>> lst.put(content5, 'mru')
    'INSERTED: CONTENT ID: 1008 SIZE: 2 HEADER: items CONTENT: 11x1110'
    >>> lst.put(content3, 'lru')
    "INSERTED: CONTENT ID: 1005 SIZE: 180 HEADER: Content-Type: 2 CONTENT: <html <p>'CMPSC132'</p></html>"
    >>> lst.put(content1, 'mru')
    'INSERTED: CONTENT ID: 1000 SIZE: 10 HEADER: Content-Type: 0 CONTENT: 0xA'
    >>> 1006 in lst
    True
    >>> contentExtra = ContentItem(1034, 2, "items", "other content")
    >>> lst.update(1008, contentExtra)
    'UPDATED: CONTENT ID: 1034 SIZE: 2 HEADER: items CONTENT: other content'
    >>> lst
    REMAINING SPACE:170
    ITEMS:3
    LIST:
    [CONTENT ID: 1034 SIZE: 2 HEADER: items CONTENT: other content]
    [CONTENT ID: 1006 SIZE: 18 HEADER: another header CONTENT: 111110]
    [CONTENT ID: 1000 SIZE: 10 HEADER: Content-Type: 0 CONTENT: 0xA]
    <BLANKLINE>
    >>> lst.tail.value
    CONTENT ID: 1000 SIZE: 10 HEADER: Content-Type: 0 CONTENT: 0xA
    >>> lst.tail.previous.value
    CONTENT ID: 1006 SIZE: 18 HEADER: another header CONTENT: 111110
    >>> lst.tail.previous.previous.value
    CONTENT ID: 1034 SIZE: 2 HEADER: items CONTENT: other content
    >>> lst.tail.previous.previous is lst.head
    True
    >>> lst.tail.previous.previous.previous is None
    True
    >>> lst.clear()
    'Cleared cache!'
    >>> lst
    REMAINING SPACE:200
    ITEMS:0
    LIST:
    <BLANKLINE>
  '''

  def __init__(self, size):
      
      self.head = None
      self.tail = None
      self.maxSize = size
      self.remainingSpace = size
      self.numItems = 0

  def __str__(self):
      
      listString = ""
      current = self.head
      while current is not None:
          listString += "[" + str(current.value) + "]\n"
          current = current.next
      return 'REMAINING SPACE:{}\nITEMS:{}\nLIST:\n{}'.format(self.remainingSpace, self.numItems, listString)

  __repr__ = __str__

  def __len__(self):
      return self.numItems

  def put(self, content, evictionPolicy):     

    if content.size > self.maxSize:  #As Gabriel mention on review check if content is to big to be put into Cache list if it is we return Insertion not allowed
      return "Insertion not allowed"
    elif self.__contains__(content.cid) == True: #we checking if the cid is already in the linklist if it is we return Content {id} already in cache, insertion not allowed, I used the __contains__ we wrote before to make it easier
      return f"Content {content.cid} already in cache, insertion not allowed"

    while self.remainingSpace < content.size: #we will try to make space to insert the thing by evict as mention by gabriel
      if evictionPolicy == "mru":  #either by mruEvict
        self.mruEvict()    #called the written function
      elif evictionPolicy == "lru":#or either lruEvict
        self.lruEvict()    #called the written function 
      

    new_node = Node(content) #remember when we get to this point we have enough space so we make a new node
    if self.head is None:  #if the link list is empty 
      self.head = new_node # we make the head and tail into the new node cause thats the only node we adding
      self.tail = new_node
    else:                        #if the link list is not empty meaning we have something
      new_node.next = self.head   #in a link list we want to add the new node in the front so the new node next is the current head 
      self.head.previous = new_node #now the head previous we need to link to the new node
      self.head = new_node #male the head to new_node

    self.remainingSpace -= content.size #remainingSpace must be decreased by the size of the content we added
    self.numItems += 1 #the number of item increase by 1

    return f'INSERTED: {content}' #return INSERTED: {content}

  def __contains__(self, cid):  
    current = self.head  #set current to head

    while current is not None:  #while current is not None
      if current.value.cid == cid: #compare the cid
        self.update(current.value.cid, current.value) #I got help with this line by TA Sabih 
        return True  #return true if cid is found
      current = current.next #update current to next node 
    return False  #otherwise return False

  

  def update(self, cid, content):
    head = self.head  # set head to head
    while head is not None:  #literate through the link list
      if head.value.cid == cid: #check if the cid is the same
        previous_content = head.value.size  #set the previous content to the size of the content
        if content.size <= self.remainingSpace + previous_content: #check if there is enough space for the new content
          if self.maxSize >= self.remainingSpace + previous_content - content.size: #make sure there is enough space for the new content 
            self.remainingSpace += previous_content - content.size #update the remainingSpace 
            head.value = content #update the head value to content which is the new value

                      
            if head != self.head: #make sure the current node is not the head 
              previous = head.previous #set previous to the head previous
              next_head = head.next  #next_head is the head next 

              if next_head is not None: #make sure the next head is not None

                next_head.previous = previous #link the next_head to the previous 
              else:
                self.tail = previous  #if the next_head is None in a link list we can link the tail to the previous


              #let me just write this in one sentence. I am trying to rearrange the link list trying to make the head the updated one and make it in order cause if it is not in order it gives me error for some reason so I just make it in order like making the head value the one we updtaed 
              if previous is not None:
                previous.next = next_head
              else:
                self.head = next_head

              head.next = self.head
              head.previous = None
              self.head.previous = head
              self.head = head

            return f'UPDATED: {content}' #if we get here we updated the thing so return the updated:{}
          else:
            return 'Cache miss!'  #if it exceed max size we return 'Cache miss!'
        else:
          return 'Cache miss!'   #content is to big so return 'Cache miss!'
      head = head.next #move the head to next node 
    return 'Cache miss!' #when cid not found in the linklist so return 'Cache miss!'





  def mruEvict(self): #revise
    if len(self) == 0:  #if the list is empty there nothing to delete cause head is already none so return None
      return None
    
    self.numItems -= 1    # if the size is not None we decrease the number of item by 1
    self.remainingSpace += self.head.value.size  #increase the remaining space by the size of the head
    head = self.head  #head is current head
    next_head = self.head.next #make the next_head the next value
    next_head.previous = None   #unlink the previous node
    head.next = None    #remember it is a double link list so we unlink the head.next

    self.head = next_head #set the head to the new head
  
  def lruEvict(self):
    if len(self) == 0: #As gabriel mention the edge case when len is 0 return None
      return None
    elif len(self) == 1: #As gabriel mention the edge case when len is 1
      head = self.head #set the head to the current head
      self.head = None #the head and tail will be None if the len is 1
      self.tail = None
      self.remainingSpace += head.value.size #same logic as mruEvict we add the value to remainingSpace
      self.numItems -= 1  #subtract 1 from the numItems
      return None
    else:
      previous = None  #In a double link list we set a previous and a head to literate through the link list
      current_tail = self.tail #this current_head is the head

      
      previous = current_tail.previous #unlink the previous value by setting the next to None
      previous.next = None

      self.tail = previous #set the tail reference to the previous value
      self.remainingSpace += current_tail.value.size  #same reason I explain earlier
      self.numItems -= 1  #same reason i explain earlier

  

  def clear(self): #revise
    self.remainingSpace = self.maxSize #when clearing, there is no space being use so it will remain space will be the max possible space avalible
    self.numItems = 0  #the number of item is 0 since we clearing everything
    self.tail = None #in a link-list when both head and tail are None it means the link list is empty so I set the tail to None then head to None
    self.head = None
    return f'Cleared cache!'   #return 'Cleared cache!' when this function is called


class Cache:
    """
        >>> cache = Cache(205)
        >>> content1 = ContentItem(1000, 10, "Content-Type: 0", "0xA")
        >>> content2 = ContentItem(1003, 13, "Content-Type: 0", "0xD")
        >>> content3 = ContentItem(1008, 242, "Content-Type: 0", "0xF2")
        >>> content4 = ContentItem(1004, 50, "Content-Type: 1", "110010")
        >>> content5 = ContentItem(1001, 51, "Content-Type: 1", "110011")
        >>> content6 = ContentItem(1007, 155, "Content-Type: 1", "10011011")
        >>> content7 = ContentItem(1005, 23, "Content-Type: 2", "<html><p>'CMPSC132'</p></html>")
        >>> content8 = ContentItem(1002, 14, "Content-Type: 2", "<html><h2>'PSU'</h2></html>")
        >>> content9 = ContentItem(1006, 170, "Content-Type: 2", "<html><button>'Click Me'</button></html>")

        >>> cache.insert(content1, 'lru')
        'INSERTED: CONTENT ID: 1000 SIZE: 10 HEADER: Content-Type: 0 CONTENT: 0xA'
        >>> cache.insert(content2, 'lru')
        'INSERTED: CONTENT ID: 1003 SIZE: 13 HEADER: Content-Type: 0 CONTENT: 0xD'
        >>> cache.insert(content3, 'lru')
        'Insertion not allowed'

        >>> cache.insert(content4, 'lru')
        'INSERTED: CONTENT ID: 1004 SIZE: 50 HEADER: Content-Type: 1 CONTENT: 110010'
        >>> cache.insert(content5, 'lru')
        'INSERTED: CONTENT ID: 1001 SIZE: 51 HEADER: Content-Type: 1 CONTENT: 110011'
        >>> cache.insert(content6, 'lru')
        'INSERTED: CONTENT ID: 1007 SIZE: 155 HEADER: Content-Type: 1 CONTENT: 10011011'

        >>> cache.insert(content7, 'lru')
        "INSERTED: CONTENT ID: 1005 SIZE: 23 HEADER: Content-Type: 2 CONTENT: <html><p>'CMPSC132'</p></html>"
        >>> cache.insert(content8, 'lru')
        "INSERTED: CONTENT ID: 1002 SIZE: 14 HEADER: Content-Type: 2 CONTENT: <html><h2>'PSU'</h2></html>"
        >>> cache.insert(content9, 'lru')
        "INSERTED: CONTENT ID: 1006 SIZE: 170 HEADER: Content-Type: 2 CONTENT: <html><button>'Click Me'</button></html>"
        >>> cache
        L1 CACHE:
        REMAINING SPACE:182
        ITEMS:2
        LIST:
        [CONTENT ID: 1003 SIZE: 13 HEADER: Content-Type: 0 CONTENT: 0xD]
        [CONTENT ID: 1000 SIZE: 10 HEADER: Content-Type: 0 CONTENT: 0xA]
        <BLANKLINE>
        L2 CACHE:
        REMAINING SPACE:50
        ITEMS:1
        LIST:
        [CONTENT ID: 1007 SIZE: 155 HEADER: Content-Type: 1 CONTENT: 10011011]
        <BLANKLINE>
        L3 CACHE:
        REMAINING SPACE:21
        ITEMS:2
        LIST:
        [CONTENT ID: 1006 SIZE: 170 HEADER: Content-Type: 2 CONTENT: <html><button>'Click Me'</button></html>]
        [CONTENT ID: 1002 SIZE: 14 HEADER: Content-Type: 2 CONTENT: <html><h2>'PSU'</h2></html>]
        <BLANKLINE>
        <BLANKLINE>
        >>> cache.hierarchy[0].clear()
        'Cleared cache!'
        >>> cache.hierarchy[1].clear()
        'Cleared cache!'
        >>> cache.hierarchy[2].clear()
        'Cleared cache!'
        >>> cache
        L1 CACHE:
        REMAINING SPACE:205
        ITEMS:0
        LIST:
        <BLANKLINE>
        L2 CACHE:
        REMAINING SPACE:205
        ITEMS:0
        LIST:
        <BLANKLINE>
        L3 CACHE:
        REMAINING SPACE:205
        ITEMS:0
        LIST:
        <BLANKLINE>
        <BLANKLINE>
        >>> cache.insert(content1, 'mru')
        'INSERTED: CONTENT ID: 1000 SIZE: 10 HEADER: Content-Type: 0 CONTENT: 0xA'
        >>> cache.insert(content2, 'mru')
        'INSERTED: CONTENT ID: 1003 SIZE: 13 HEADER: Content-Type: 0 CONTENT: 0xD'
        >>> cache[content1].value
        CONTENT ID: 1000 SIZE: 10 HEADER: Content-Type: 0 CONTENT: 0xA
        >>> cache[content2].value
        CONTENT ID: 1003 SIZE: 13 HEADER: Content-Type: 0 CONTENT: 0xD
        >>> cache[content3]
        'Cache miss!'
        >>> cache.insert(content5, 'lru')
        'INSERTED: CONTENT ID: 1001 SIZE: 51 HEADER: Content-Type: 1 CONTENT: 110011'
        >>> content6 = ContentItem(1007, 160, "Content-Type: 1", "10011011")
        >>> cache.insert(content6, 'lru')
        'INSERTED: CONTENT ID: 1007 SIZE: 160 HEADER: Content-Type: 1 CONTENT: 10011011'
        >>> cache.insert(content4, 'lru')
        'INSERTED: CONTENT ID: 1004 SIZE: 50 HEADER: Content-Type: 1 CONTENT: 110010'
        >>> cache.insert(content7, 'mru')
        "INSERTED: CONTENT ID: 1005 SIZE: 23 HEADER: Content-Type: 2 CONTENT: <html><p>'CMPSC132'</p></html>"
        >>> cache.insert(content8, 'mru')
        "INSERTED: CONTENT ID: 1002 SIZE: 14 HEADER: Content-Type: 2 CONTENT: <html><h2>'PSU'</h2></html>"
        >>> cache.insert(content9, 'mru')
        "INSERTED: CONTENT ID: 1006 SIZE: 170 HEADER: Content-Type: 2 CONTENT: <html><button>'Click Me'</button></html>"
        >>> cache
        L1 CACHE:
        REMAINING SPACE:182
        ITEMS:2
        LIST:
        [CONTENT ID: 1003 SIZE: 13 HEADER: Content-Type: 0 CONTENT: 0xD]
        [CONTENT ID: 1000 SIZE: 10 HEADER: Content-Type: 0 CONTENT: 0xA]
        <BLANKLINE>
        L2 CACHE:
        REMAINING SPACE:155
        ITEMS:1
        LIST:
        [CONTENT ID: 1004 SIZE: 50 HEADER: Content-Type: 1 CONTENT: 110010]
        <BLANKLINE>
        L3 CACHE:
        REMAINING SPACE:12
        ITEMS:2
        LIST:
        [CONTENT ID: 1006 SIZE: 170 HEADER: Content-Type: 2 CONTENT: <html><button>'Click Me'</button></html>]
        [CONTENT ID: 1005 SIZE: 23 HEADER: Content-Type: 2 CONTENT: <html><p>'CMPSC132'</p></html>]
        <BLANKLINE>
        <BLANKLINE>
        >>> cache.clear()
        'Cache cleared!'
        >>> contentA = ContentItem(2000, 52, "Content-Type: 2", "GET https://www.pro-football-reference.com/boxscores/201802040nwe.htm HTTP/1.1")
        >>> contentB = ContentItem(2001, 76, "Content-Type: 2", "GET https://giphy.com/gifs/93lCI4D0murAszeyA6/html5 HTTP/1.1")
        >>> contentC = ContentItem(2002, 11, "Content-Type: 2", "GET https://media.giphy.com/media/YN7akkfUNQvT1zEBhO/giphy-downsized.gif HTTP/1.1")
        >>> cache.insert(contentA, 'lru')
        'INSERTED: CONTENT ID: 2000 SIZE: 52 HEADER: Content-Type: 2 CONTENT: GET https://www.pro-football-reference.com/boxscores/201802040nwe.htm HTTP/1.1'
        >>> cache.insert(contentB, 'lru')
        'INSERTED: CONTENT ID: 2001 SIZE: 76 HEADER: Content-Type: 2 CONTENT: GET https://giphy.com/gifs/93lCI4D0murAszeyA6/html5 HTTP/1.1'
        >>> cache.insert(contentC, 'lru')
        'INSERTED: CONTENT ID: 2002 SIZE: 11 HEADER: Content-Type: 2 CONTENT: GET https://media.giphy.com/media/YN7akkfUNQvT1zEBhO/giphy-downsized.gif HTTP/1.1'
        >>> cache.hierarchy[2]
        REMAINING SPACE:66
        ITEMS:3
        LIST:
        [CONTENT ID: 2002 SIZE: 11 HEADER: Content-Type: 2 CONTENT: GET https://media.giphy.com/media/YN7akkfUNQvT1zEBhO/giphy-downsized.gif HTTP/1.1]
        [CONTENT ID: 2001 SIZE: 76 HEADER: Content-Type: 2 CONTENT: GET https://giphy.com/gifs/93lCI4D0murAszeyA6/html5 HTTP/1.1]
        [CONTENT ID: 2000 SIZE: 52 HEADER: Content-Type: 2 CONTENT: GET https://www.pro-football-reference.com/boxscores/201802040nwe.htm HTTP/1.1]
        <BLANKLINE>
        >>> cache[contentC].value
        CONTENT ID: 2002 SIZE: 11 HEADER: Content-Type: 2 CONTENT: GET https://media.giphy.com/media/YN7akkfUNQvT1zEBhO/giphy-downsized.gif HTTP/1.1
        >>> cache.hierarchy[2]
        REMAINING SPACE:66
        ITEMS:3
        LIST:
        [CONTENT ID: 2002 SIZE: 11 HEADER: Content-Type: 2 CONTENT: GET https://media.giphy.com/media/YN7akkfUNQvT1zEBhO/giphy-downsized.gif HTTP/1.1]
        [CONTENT ID: 2001 SIZE: 76 HEADER: Content-Type: 2 CONTENT: GET https://giphy.com/gifs/93lCI4D0murAszeyA6/html5 HTTP/1.1]
        [CONTENT ID: 2000 SIZE: 52 HEADER: Content-Type: 2 CONTENT: GET https://www.pro-football-reference.com/boxscores/201802040nwe.htm HTTP/1.1]
        <BLANKLINE>
        >>> cache[contentA].next.previous.value
        CONTENT ID: 2000 SIZE: 52 HEADER: Content-Type: 2 CONTENT: GET https://www.pro-football-reference.com/boxscores/201802040nwe.htm HTTP/1.1
        >>> cache.hierarchy[2]
        REMAINING SPACE:66
        ITEMS:3
        LIST:
        [CONTENT ID: 2000 SIZE: 52 HEADER: Content-Type: 2 CONTENT: GET https://www.pro-football-reference.com/boxscores/201802040nwe.htm HTTP/1.1]
        [CONTENT ID: 2002 SIZE: 11 HEADER: Content-Type: 2 CONTENT: GET https://media.giphy.com/media/YN7akkfUNQvT1zEBhO/giphy-downsized.gif HTTP/1.1]
        [CONTENT ID: 2001 SIZE: 76 HEADER: Content-Type: 2 CONTENT: GET https://giphy.com/gifs/93lCI4D0murAszeyA6/html5 HTTP/1.1]
        <BLANKLINE>
        >>> cache[contentC].next.previous.value
        CONTENT ID: 2002 SIZE: 11 HEADER: Content-Type: 2 CONTENT: GET https://media.giphy.com/media/YN7akkfUNQvT1zEBhO/giphy-downsized.gif HTTP/1.1
        >>> cache.hierarchy[2]
        REMAINING SPACE:66
        ITEMS:3
        LIST:
        [CONTENT ID: 2002 SIZE: 11 HEADER: Content-Type: 2 CONTENT: GET https://media.giphy.com/media/YN7akkfUNQvT1zEBhO/giphy-downsized.gif HTTP/1.1]
        [CONTENT ID: 2000 SIZE: 52 HEADER: Content-Type: 2 CONTENT: GET https://www.pro-football-reference.com/boxscores/201802040nwe.htm HTTP/1.1]
        [CONTENT ID: 2001 SIZE: 76 HEADER: Content-Type: 2 CONTENT: GET https://giphy.com/gifs/93lCI4D0murAszeyA6/html5 HTTP/1.1]
        <BLANKLINE>
        >>> contentD = ContentItem(2002, 11, "Content-Type: 2", "GET https://media.giphy.com/media/YN7akkfUNQvT1zEBhO/giphy-downsized.gif HTTP/1.1")
        >>> cache.insert(contentD, 'lru')
        'Content 2002 already in cache, insertion not allowed'
        >>> contentE = ContentItem(2000, 103, "Content-Type: 2", "GET https://www.pro-football-reference.com/boxscores/201801210phi.htm HTTP/1.1")
        >>> cache[2000] = contentE
        >>> cache.hierarchy[2]
        REMAINING SPACE:15
        ITEMS:3
        LIST:
        [CONTENT ID: 2000 SIZE: 103 HEADER: Content-Type: 2 CONTENT: GET https://www.pro-football-reference.com/boxscores/201801210phi.htm HTTP/1.1]
        [CONTENT ID: 2002 SIZE: 11 HEADER: Content-Type: 2 CONTENT: GET https://media.giphy.com/media/YN7akkfUNQvT1zEBhO/giphy-downsized.gif HTTP/1.1]
        [CONTENT ID: 2001 SIZE: 76 HEADER: Content-Type: 2 CONTENT: GET https://giphy.com/gifs/93lCI4D0murAszeyA6/html5 HTTP/1.1]
        <BLANKLINE>
        >>> cache.hierarchy[2].tail.value
        CONTENT ID: 2001 SIZE: 76 HEADER: Content-Type: 2 CONTENT: GET https://giphy.com/gifs/93lCI4D0murAszeyA6/html5 HTTP/1.1
        >>> cache.hierarchy[2].tail.previous.value
        CONTENT ID: 2002 SIZE: 11 HEADER: Content-Type: 2 CONTENT: GET https://media.giphy.com/media/YN7akkfUNQvT1zEBhO/giphy-downsized.gif HTTP/1.1
        >>> cache.hierarchy[2].tail.previous.previous.value
        CONTENT ID: 2000 SIZE: 103 HEADER: Content-Type: 2 CONTENT: GET https://www.pro-football-reference.com/boxscores/201801210phi.htm HTTP/1.1
        >>> cache.hierarchy[2].tail.previous.previous is cache.hierarchy[2].head
        True
        >>> cache.hierarchy[2].tail.previous.previous.previous is None
        True
    """

    def __init__(self, lst_capacity):
        self.hierarchy = [CacheList(lst_capacity), CacheList(lst_capacity), CacheList(lst_capacity)]
        self.size = 3

    def __str__(self):
        return ('L1 CACHE:\n{}\nL2 CACHE:\n{}\nL3 CACHE:\n{}\n'.format(self.hierarchy[0], self.hierarchy[1], self.hierarchy[2]))

    __repr__=__str__


    def clear(self):
      for item in self.hierarchy:
        item.clear()
      return 'Cache cleared!'


    def insert(self, content, evictionPolicy):
      return self.hierarchy[content.__hash__()].put(content, evictionPolicy) # As gabriel mention we trying to get the proper Cahcelist index by hashing the content.__hash__() and use thar index to access self.hierarchy and apply put

    def __getitem__(self, content):
      cachelist = self.hierarchy[content.__hash__()]# As gabriel mention we trying to get the proper Cahcelist index by hashing the content.__hash__() and use thar index to access self.hierarchy 
      if CacheList.__contains__(cachelist, content.cid): #determine if the content is in the cachelist 
          return cachelist.head.value #if it does return the Node object
      else:
          return "Cache miss!"    #else return Cache miss!

    def __setitem__(self, cid, content):

      #this __setitem__ is really similar to upate but instead of using head we using self.head we using Cachelist.head
      cachelist = self.hierarchy[content.__hash__()]#we trying to get the proper Cahcelist index by hashing the content.__hash__() and use thar index to access self.hierarchy
      head = cachelist.head #we set this variable to the head of the cachelist

      while head is not None: #we iterate through the cachelist until we find the cid
        if head.value.cid == content.cid:#check if the cid is the same
          previous_size = head.value.size  #set the previous content to the size of the content
          if content.size <= cachelist.remainingSpace + previous_size: #make sure the content size is less than our remaining space and previous size
            if cachelist.maxSize >= cachelist.remainingSpace + previous_size - content.size: #make sure we don't go over maxSize
              cachelist.remainingSpace += previous_size - content.size #update the remaining space
              head.value = content #set this to the content the value of head so we can put it in update

                    
              cachelist.update(head.value.cid, head.value) # use this function we written before to update the cachelist instead of writing the same thing

                    
                
        head = head.next #update the head
      

      
    