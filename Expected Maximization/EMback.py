#----------Function Defination-------------------------------------
def generateSeq(N,P,P1,P2) :   
 #logic for generating random sequence with given probability
   for i in range(N):
       r= random.random()
       if r < P:
          C.append('C1')
          s = random.random()
          if s < P1:
             seq.append(1)
          else :
             seq.append(0)
       else :    
          C.append('C2')
          t = random.random()
          if t < P2:
              s = random.random()
              seq.append(1)
          else :
              seq.append(0)
   time.sleep(1)           
   print("Randomly generated coin sequence C1:first coin, C2:second coin")           
   print(C)
   time.sleep(1)
   print("Randomly generated HEAD/TAIL sequence :1 represeants HEAD, 0 represents TAIL")
   print(seq)
   return(seq)
#Logic for estimating Algorithm
def estimateProb(ON,OP,OP1,OP2,seq1) :
    print("Starting the EM algorithm")
    time.sleep(1)
    PP = PP1 =PP2 = 0
    for h in range(1000):
#    while (PP != OP or PP1 != OP1 or PP2 != OP2):
          sumEz = sum1 = M = 0
          for x in seq1:
              #E-STEP ------------------------------------------------
              NUM1 = OP*(OP1**x)*((1-OP1)**(1-x))
              NUM2 = (1-OP)*(OP2**x)*((1-OP2)**(1-x))
              Ez =NUM1/(NUM1 +NUM2) #
              #End E-Step----------------------------------------------
              sumEz += Ez # Summation of E(zi)
              sum1 += x*Ez       # Summation of xiE(zi)
              M += x    
          PP = OP
          PP1 = OP1
          PP2 = OP2
          # M-Step-------------------------------------------
          OP = sumEz/ ON
          OP1 = sum1/sumEz
          OP2 = (M - sum1)/(ON - sumEz)
          #End MStep----------------------------------------------
     #     print(OP,OP1,OP2)
     #     if abs(OP-PP)< 0.05 and abs (OP1-PP1) < 0.05 and (OP2-PP2) < 0.05:
     #         break
    print("EM algorithm estimates the Probability: ") 
    print("Estimated P  : ",OP)
    print("Estimated P1 : ",OP1)
    print("Estimated P2 : ",OP2)
    
    
#************************Program***************************** 
#************************************************************
import time
import random
N=int(input(" Provide input  , Number of trials: "))
P=float(input(" Two Coins C1, C2, Provide probability of occuring C1 i.e P = "))
P1=float(input("Provide probability of Head in coin C1 i.e P1 = "))
P2=float(input("Provide probability of Head in coin C1 i.e P2 = "))
C= list()
seq= list()
if type(N) == int and P>= 0 and P <=1 and P1 >= 0 and P1 <=1 and P2 >=0 and P2 <= 1:
   seq1 = generateSeq(N,P,P1,P2)
#   P=float(input(" Two Coins C1, C2, Provide probability of occuring C1 i.e P = "))
#   P1=float(input("Provide probability of Head in coin C1 i.e P1 = "))
#   P2=float(input("Provide probability of Head in coin C1 i.e P2 = "))
   estimateProb(N,P,P1,P2,seq1)
   input("Press enter to exit")
else:
   input("You have provided INAPPROPRIATE probability values: Press enter to exit")
