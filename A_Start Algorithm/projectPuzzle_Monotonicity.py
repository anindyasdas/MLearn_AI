import time
import random
f = open('goal.txt','r')
final_state = [[int(num) for num in line.split(' ')] for line in f]

class Puzzle:

    def __init__(self):
        # heuristic value of the node
        self._h = 0
        # depth of the node
        self._g = 0
        # parent node
        self._parent = None
        self.mat = []
        for i in range(3):
            self.mat.append(final_state[i][:])

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        else:
            return self.mat == other.mat
        
            
    def __str__(self):  #to print matrix in a format
        fmt = ''
        for row in range(3):
            fmt += ' '.join(map(str, self.mat[row]))
            fmt += '\r\n'
        return fmt
    def solvable(self):  #to print matrix in a format
        a=[]
        b=[]
        rec1=[]
        rec2=[]
        inverse=0
        for row in range(3):
            for col in range(3):
                a.append(self.mat[row][col])
                b.append(final_state[row][col])
        for index1 in range(9):
            item1=a[index1]
            item2=b[index1]
            if index1<8: 
               for index2 in range(index1+1,9):
                   if item1> a[index2] and a[index2]>0:
                       rec1.append((item1,a[index2]))
                   if item2> b[index2] and b[index2]>0:
                       rec1.append((item2,b[index2]))
        for item in rec1:
            if item not in rec2:
                inverse+=1
        print("start state:")
        print(self)
        g = Puzzle()
        g.mat=final_state
        print("goal state:")
        print(g)
        if(inverse%2 !=0):
            print("the puzzle is unsolvable, as number of inverses is odd")
            input("press enter to exit")
            exit()
        else:
            print("the Puzzle is solvable, starting computing")
                   
         
    def inPut(self):
    #    mat=[[[] for j in range(3)] for i in range(3)]
     #   print("enter the puzzle")
     #   for i in range(3):
     #       print("for row:",i)
     #       for j in range(3):
     #           self.mat[i][j]=(int(input()))
        f = open('start.txt','r')
        self.mat = [[int(num) for num in line.split(' ')] for line in f]

     #   print("input",self.mat)
    def _positionZero(self,value):
        for r in range(3):
            for c in range(3):
                if self.mat[r][c]==value:
                   return (r,c)
    def _findMoves(self,row,col):
        # find possible moves
        moves=[]
        if row > 0:
            moves.append((row - 1, col))
        if col > 0:
            moves.append((row, col - 1))
        if row < 2:
            moves.append((row + 1, col))
        if col < 2:
            moves.append((row, col + 1))
        return moves    

    def _solve(self,parameter):
         self._h=parameter(self.mat)
         openlist=[self]
         closedlist=[]
         count = 0
         mono = "monotonic restriction is maintained"
         #for ab in range(5):
         while len(openlist)>0:
             x=openlist.pop(0)
             count+=1 
          #   print("popped",x)
          #   print("g_val:",x._g)
          #   print("h_val:",x._h)      
          #   print("final_state",final_state)
          #   print(x.mat == final_state)
             if x.mat == final_state:
          #       print("matched")
                 return (closedlist,x,count,(x._g),mono)
               #  return (closedlist,x,count,(x._g+x._h))
 
             else:
                zero= x._positionZero(0)
                if zero == None:
                    raise Exception("Zero position not found in input Given Puzzle")
           #     print("position of zero",zero)
                moves=x._findMoves(*zero)
            #    print("number of moves",moves)
                for i in moves:
                    #chk_ol = -1
                    p=x.clone_swap(i,zero)
                    p._g = x._g + 1
                    p._h=parameter(p.mat)
                    parent1=p._parent
                    if parent1._h > 1 + p._h:
                        mono = "monotonic restriction is not maintained"
                        print("\n monotonic restriction is violated")
                        print("parent is :")
                        print(parent1)
                        print("h(parent) is: ", parent1._h)
                        print("child is : ")
                        print(p)
                        print("cost from parent to child is 1")
                        print("h(child)",p._h)
                    else:
                        mono = "monotonic restriction is  maintained"
                        print("\n monotonic restriction is maintained")
                        print("parent is :")
                        print(parent1)
                        print("h(parent) is: ", parent1._h)
                        print("child is : ")
                        print(p)
                        print("cost from parent to child is 1")
                        print("h(child)",p._h)
                        
                    chk_ol = find_ol(p,openlist) # checking openlist if the Node is present in OL
                    if chk_ol != None:   # if it is found in Openlist
                        c = openlist[chk_ol]
                        if (p._g + p._h) < (c._g + c._h): # if Node is present in OL and if new f_value is less than previous update
                            parent = c._parent
                            mono = "monotonic restriction is not maintained"
                            '''
                            print("monotonic restriction is violated")
                            print("parent is :")
                            print(parent)
                            print("h(parent) is: ", parent._h)
                            print("child is : ")
                            print(c)
                            print("cost from parent to child is 1")
                            print("h(child)",c._h)'''    
                            c._h = p._h
                            c._g = p._g
                            c._parent =p._parent
                    else:
                        chk_cl = find_ol(p,closedlist)
                        if chk_cl == None: # if it is not found in closed list then append else ignore
                            openlist.append(p)
                        else:
                            c =closedlist[chk_cl]
                            if (p._g + p._h) < (c._g + c._h):# if Node is present in CL and if new f_value is less than previous update
                                parent = c._parent
                                mono = "monotonic restriction is not maintained"
                                '''
                                print("monotonic restriction is violated")
                                print("parent is :")
                                print(parent)
                                print("h(parent) is: ", parent._h)
                                print("child is : ")
                                print(c)
                                print("cost from parent to child is 1")
                                print("h(child)",c._h)'''
                                closedlist.remove(c)
                                openlist.append(p)
                openlist = sorted(openlist, key=lambda s: s._h + s._g)   # use of lambda unnamed function then sorting the openlist based on key
                closedlist.append(x)
               
    def clone_swap(self,i,zero):
           p=Puzzle()
           for it0 in range(3):
             p.mat[it0] = self.mat[it0][:]
           p._swap(*i,*zero)
           p._parent=self
     #      print("after swap",p.mat)
           return p
    def _swap(self,row,col,row1,col1):
     #     print("pozition to be swapped",row,col)
     #     print("zero positions",row1,col1)
          temp=self.mat[row][col]
          self.mat[row][col]=self.mat[row1][col1]
          self.mat[row1][col1]=temp

def heur_uninformed(mat1):
    h=0
    return h
          
          
def heur_displaced_tiles(mat1):
    h=0
    for k in range(3):
        for l in range(3):
            if not mat1[k][l]==final_state[k][l] and mat1[k][l] >0 :
                h+=1                                  #calculating displaced tiles
    return h

def heur_manhattan(mat1):
    h=0
    for i1 in range(3):
        for j1 in range(3):
            item = mat1[i1][j1] # storing the value to be searched
            for i2 in range(3):
                for j2 in range(3):
                    if final_state[i2][j2]==item and item > 0:
                        h+= abs(i1-i2) + abs(j1-j2)
    return h                   
def heur_displaced_tiles_zero(mat1):
    h=0
    for k in range(3):
        for l in range(3):
            if not mat1[k][l]==final_state[k][l] :
                h+=1                                  #calculating displaced tiles
    return h

def heur_manhattan_zero(mat1):
    h=0
    for i1 in range(3):
        for j1 in range(3):
            item = mat1[i1][j1] # storing the value to be searched
            for i2 in range(3):
                for j2 in range(3):
                    if final_state[i2][j2]==item :
                        h+= abs(i1-i2) + abs(j1-j2)
    return h                   
                    
def heur_pessimistic(mat1):
    h=0
    for i1 in range(3):
        for j1 in range(3):
            item = mat1[i1][j1] # storing the value to be searched
            for i2 in range(3):
                for j2 in range(3):
                    if final_state[i2][j2]==item and item > 0:
                 #   if final_state[i2][j2]==item : 
                        h+= abs(i1-i2) + abs(j1-j2) + random.randint(1,10)
    #print(h)
    return h

def heur_inverse(mat1):
    h=0
    a=[]
    b=[]
    rec1=[]
    rec2=[]
    for row in range(3):
        for col in range(3):
            a.append(mat1[row][col])
            b.append(final_state[row][col])
    for index1 in range(9):
        item1=a[index1]
        item2=b[index1]
        if index1<8: 
            for index2 in range(index1+1,9):
                if item1> a[index2] and a[index2]>0:
                    rec1.append((item1,a[index2]))
                if item2> b[index2] and b[index2]>0:
                    rec1.append((item2,b[index2]))
    for item in rec1:
        if item not in rec2:
            h+=1
        
    #print(h)
    return h               
                    
        
    
def find_ol(p1,o1):
    mat_list = []
    for m in o1:
        mat_list.append(m.mat)
    if p1.mat in mat_list:
        return mat_list.index(p1.mat)
    


    

def trace(clist,y):
    t = []
    it1= 0
    t.append(y)
    y= y._parent
    while y != None:
        if y in clist:
            t.append(y)
            y=y._parent
    #print(len(t))
    print("OPTIMAL PATH:")
    for arr in reversed(t):
        it1+=1
        print("step",it1,":")
        print(arr)
    #    print("h_val",arr._h)
     #   print("g._val",arr._g)
    return it1

def print_stats(count,fval,op_state,duration,m):
    #print("the Optimal Path is:")
    #for e in path:
    #    print(e)
    print("total number of states explored:", count)
    print("total number of states in optimal path:",op_state)
    print("optimal cost of the path:",fval)
    print("Total time taken for execution:",duration)
    print(m)
    print("*************************************************")
    
        
        
        
    
    
        
           
################################MAIN######################################################################
##########################################################################################################

p = Puzzle()
p.inPut()
p.solvable()
#print(p)
#############################################manhattan_distance###################################################
print("from manhattan_distance Heurestic SEARCH:")
start = time.time()
(clist1,y,count,fval,mono)=p._solve(heur_manhattan)
op_state=trace(clist1,y)
end = time.time()
print_stats(count,fval,op_state,(end-start),mono)
#############################################manhattan_distance###################################################
print("from manhattan_distance Heurestic SEARCH with ADDED ZERO TILES:")
start = time.time()
(clist,y,count,fval,mono)=p._solve(heur_manhattan_zero)
op_state=trace(clist,y)
end = time.time()
print_stats(count,fval,op_state,(end-start),mono)

############################################Displaced_tiles#####################################################
print("For displaced tiles Heurestic SEARCH:")
start = time.time()
(clist2,y,count,fval,mono)=p._solve(heur_displaced_tiles)
op_state=trace(clist2,y)
end = time.time()
print_stats(count,fval,op_state,(end-start),mono)
############################################Displaced_tiles#####################################################
print("For displaced tiles Heurestic SEARCH with ADDED ZERO TILES:")
start = time.time()
(clist,y,count,fval,mono)=p._solve(heur_displaced_tiles_zero)
op_state=trace(clist,y)
end = time.time()

print_stats(count,fval,op_state,(end-start),mono)
count1=0
print("Manhattan distance closed list number of nodes:",len(clist1))
print("Displaced tiles closed list number of nodes:",len(clist2))
for i in range(len(clist1)):
    if clist1[i] in clist2:
        count1+=1

print("matched content:",count1)
#print(set(clist1).issubset(clist2))
'''    print(clist1[i])
print("*******")    
for j in range (len(clist2)):
    print(clist2[j])
    
#print("list1:",np.array(clist1))
#print("list2:",np.array(clist2))
#print(set(clist1).issubset(clist2))


###########################################Uninformed#####################################################
print("For UNINFORMED SEARCH:")
start = time.time()
(clist,y,count,fval,mono)=p._solve(heur_uninformed)
op_state=trace(clist,y)
end = time.time()
print_stats(count,fval,op_state,(end-start),mono)

#############################################Pessimistic h(n)>h*(n)###################################################
print("from Pessimestic Heurestic SEARCH  h(n) > h*(n):")
start = time.time()
(clist,y,count,fval,mono)=p._solve(heur_inverse)
op_state=trace(clist,y)
end = time.time()
print_stats(count,fval,op_state,(end-start),mono)
input("press enter to exit")


#############################################Pessimistic h(n)>h*(n)###################################################
print("from Pessimestic Heurestic SEARCH  h(n) > h*(n):")
start = time.time()
(clist,y,count,fval,mono)=p._solve(heur_pessimistic)
op_state=trace(clist,y)
end = time.time()
print_stats(count,fval,op_state,(end-start),mono)
input("press enter to exit")'''
input("press enter to exit")
