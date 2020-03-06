######################################################Modus Ponens Theory proover##############################################################
#Read me instruction
# OR is denoted by V
# AND is denoted by ^
# NOT is denoted by ~
# Implications are denoted by >
#P implies Q is noted as (P>Q), (NOT)P implies Q is denoted as (~P>Q)
#README instruction:
#In the main function put the expression you want to prove as expression1
#eg. if you want to prove  (P>Q)>((~Q>P)>Q), then put in main expression1 = '((P>Q)>((~Q>P)>Q))' 


def left_hand_manager(exp):
    left_hand_side = []
    expanded_exp = expanding_expression(exp)
    while expanded_exp != 'F': #check if right hand side is 'F' or not
        (left, right) = clause_isolator(expanded_exp)
        if left == None: # when only one term is left at the right, left is returned as 'None' by parse_clause_isolator
            if right != 'F':
                # when only one term is present at right it is expressed with help of negation as Q = (Q>F)>F
                left_new = "(" + right + ">" + "F)"
                left_hand_side.append(left_new)
                right = "F"
        else:
            left_hand_side.append(left)
        expanded_exp = right
    return(left_hand_side,expanded_exp)


def expanding_expression(exp):
    #This will simplify given expression break AND/OR /~ clauses

    #First we will be expanding the expression around implication sign
    if exp[0] == '(':
        length=len(exp)
        exp = exp[1:(length-1)]
    count_brackets = 0
    for i, item in enumerate(exp):
        if item == '(':
            count_brackets += 1
        elif item == ')':
            count_brackets -= 1
        elif item == '>':
            if count_brackets == 0:
            #when bracket are balanced we recursively call two parts around '>'
                return "(" + expanding_expression(exp[0:i]) + ">" +  expanding_expression(exp[i+1:])+")"

    #if length is 1 return
    if len(exp) == 1:
        return exp


    
    # # Expand the ----not (~) operator
    if exp[0] == '~':
        expanded_exp = expanding_expression(exp[1:])   
        return "(" + expanded_exp + ">" + "F"   + ")"
    
    #Expand the and/ or operator
    count1_brackets = 0
    for i,item in enumerate(exp):
        if item == '(':
            count1_brackets += 1
        elif item == ')':
            count1_brackets -= 1
        elif item == 'V' or item == '^' :
            if count1_brackets == 0:
                expanded_exp1 = expanding_expression(exp[0:i])
                expanded_exp2 = expanding_expression(exp[i+1:])
                if item == 'V' : # it is the OR value
                    return "((" + expanded_exp1 + ">" + "F)>" + expanded_exp2 + ")"
                else:
                    return "((" + expanded_exp1 + ">(" + expanded_exp2 + ">F))>F)" 
    return  "(" + exp + ")"
    
    

def clause_isolator(exp):
    if exp[0] == '(':
        length=len(exp)
        exp = exp[1:(length-1)]
    count_brackets = 0
    for i, item in enumerate(exp):
        if item == '(':
            count_brackets += 1
        elif item == ')':
            count_brackets -= 1
        elif item == '>':
            if count_brackets == 0:
               return (exp[0:i], exp[i+1:])
    return (None, exp)# when only one term is left at the right, left is returned as 'None' by parse_clause_isolator

def modus_ponens(left_hand_side , iterations):
    # this function apply modus ponens to Generated Left hand side expression
    modus_ponens_set = set()
    for i in range(iterations):
        for h1 in left_hand_side:
            for h2 in left_hand_side:
                if h1 != h2 :
                    modus_ponens_set.add(h1)
                    modus_ponens_set.add(h2)
                    (left, right) = clause_isolator(h2)
                    if left == h1 : #(application of modus ponens h2:P>Q ,h1:P)
                        modus_ponens_set.add(right)
        left_hand_side = modus_ponens_set.copy()
        #print("left_hand_side",left_hand_side)            
    return (left_hand_side)

def theorem_checker(modus_ponens_results,left_hand_side):
    if 'F' in modus_ponens_results:
        print("moduls poenes gives",modus_ponens_results)
        print(" since modus ponens derives F , the theorem is true")
        return
    else:
        temp=set()# stores left side of complex expressionwith right side as F
        found=set()#stores entire expression with right as F
        flag=0
        for item in modus_ponens_results:
            if len(item)>5:
                (left,right)=clause_isolator(item)
                if right=='F':
        #            if left in modus_ponens_results:
                        temp.add(left)
                        found.add(item)
                        flag=1
        if flag==1:
            print("I can't prove the theorem, with given information , can you provide any subtheorem between the following expressions ?")
            print(temp)
            print(set(left_hand_side).difference(found))
            x=input("yes/no? \n ")
            if x=='yes':
                sub_list=[]
                sub=input("Provide subtheorem:")
                sub_list.append(expanding_expression(sub))
                new_left_hand_side = left_hand_side + sub_list
                new_modus_ponens_results = modus_ponens(new_left_hand_side, len(new_left_hand_side))
                theorem_checker(new_modus_ponens_results,new_left_hand_side)
            else:
                print("moduls poenes gives:",modus_ponens_results)
                print("the theorem can't be proven with available information")
                return
        else:
            print("moduls poenes gives",modus_ponens_results)
            print("this is not a theorem since 'F' can't be derived")
            return
                
    
def main():
    expression1 = '((P>Q)>((~Q>P)>Q))' # True
    #expression1 = '(P>(PVQ))' #True
    #expression1 = '((P^Q)>(PVP))' #True but requires sub theorem
    #expression1= '(P>(P>Q))' #False
    #expression1 = '((P>Q)>((~Q>P)>P))' #False
    print("the chosen expression is :" ,expression1)
    (left_hand_side,right_hand_side)=left_hand_manager(expression1)
    #print(right_hand_side)
    print("the left hand side clauses are:",set(left_hand_side))
    modus_ponens_results = modus_ponens(left_hand_side, len(left_hand_side))
    theorem_checker(modus_ponens_results,left_hand_side)
    input("please press Enter to exit")

if __name__ == "__main__":
        main()

    


    

