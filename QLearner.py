"""
Template for implementing QLearner  (c) 2015 Tucker Balch
"""

import numpy as np
import random as rand

class QLearner(object):

    def __init__(self, \
        num_states=100, \
        num_actions = 4, \
        alpha = 0.2, \
        gamma = 0.6, \
        rar = 0.8, \
        radr = 0.9, \
        dyna = 0, \
        alphar=0.2,\
        verbose = False):

        self.verbose = verbose
        self.num_actions = num_actions
        num_actions1=num_actions+1
        self.num_actions1=num_actions1
        self.s = 0
        self.a = 0
        
        self.rar=rar
        self.radr=radr
        self.alpha=alpha
        self.gamma=gamma
        self.dyna=dyna
        self.num_states=num_states
        self.alphar=alphar
        
        
        
        self.q={}
        
        self.T={}
        self.Tc={}
        self.R={}
        
#initiallize Q table, Tc, and R table
                    
        for s,a in  np.ndindex((num_states,num_actions)): self.q[(s,a)]=np.random.random_integers(-1, 1) 
        
        if self.dyna>0:
            
            for i,j,iprime in  np.ndindex((num_states,num_actions,num_actions1)): 
                self.Tc[(i,j,iprime)]=.000001
          #+1 account for n,w,s,e and same state      
            for i,j,iprime in  np.ndindex((num_states,num_actions,num_actions1)):   
               self.T[(i,j,iprime)]=self.Tc.get((i,j,iprime),0.0)/sum(self.Tc.get((i,j,k),0.0) for k in range(self.num_actions1))
            probabilities=[self.T.get((i,j,k),0.0) for k in range(self.num_actions1)]
            print probabilities
            for i,j in np.ndindex((num_states,num_actions)):self.R[(i,j)]=0.0             

    def querysetstate(self, s):
        """
        @summary: Update the state without updating the Q-table
        @param s: The new state
        @returns: The selected action
        """
        self.s = s
        #action = rand.randint(0, self.num_actions-1)
        actions=[self.q.get((s, i), 0.0) for i in range(self.num_actions)]
        action= np.random.choice([i for i, j in enumerate(actions) if j == max(actions)])        
        
        if self.verbose: print "s =", s,"a =",action
        return action

    def query(self,s_prime,r):
        """
        @summary: Update the Q table and return an action
        @param s_prime: The new state
        @param r: The ne state
        @returns: The selected action
        """
        #update q table
        newQmax=max([self.q.get((s_prime, a_prime),0.0) for a_prime in range(self.num_actions)]) 
        self.q[(self.s,self.a)]=((1-self.alpha)*(self.q[(self.s,self.a)])+self.alpha*(r+self.gamma*(newQmax)))
    
    
    
        if np.random.random()<self.rar:
            action = rand.randint(0, self.num_actions-1)
    
        else:
            actions=[self.q.get((s_prime, i), 0.0) for i in range(self.num_actions)]
            max_A=max(actions)
            action= np.random.choice([i for i, j in enumerate(actions) if j == max_A])     
        self.rar *=self.radr
       
       
#-------------------------Dyna Part
        if self.dyna>0:
            print s_prime-self.s
            if s_prime-self.s == -10: #north
                    s_prime_A = 0
            elif s_prime-self.s == +1: #east
                    s_prime_A = 1
            elif s_prime-self.s == +10: #east
                    s_prime_A = 2
            elif s_prime-self.s == -1: #east
                    s_prime_A = 3
            elif s_prime-self.s == 0: #no move
                    s_prime_A = 4
            
            self.Tc[(self.s,self.a,s_prime_A)]+=1
            for i,j,iprime in  np.ndindex((self.num_states,self.num_actions,self.num_actions1)):   
                self.T[(i,j,iprime)]=self.Tc.get((i,j,iprime),0.0)/sum(self.Tc.get((i,j,k),0.0) for k in range(self.num_actions+1))
           # self.T[(self.s,self.a,s_prime)]=self.Tc.get((self.s,self.a,s_prime),0.0)/sum(self.Tc.get((self.s,self.a,i),0.0) for i in range(self.num_states))
            self.R[(self.s,self.a)]=(1-self.alphar)*self.R[(self.s,self.a)]+(self.alphar*r)

            
            s_random=np.random.random_integers(0,self.num_states-1,self.dyna)
            a_random=np.random.random_integers(0,self.num_actions-1,self.dyna)
            
            for i in range(0,self.dyna):
               # print i
                probabilities=[self.T.get((s_random[i],a_random[i],j),0.0) for j in range(self.num_actions+1)]
               
                a_choose=np.random.choice(self.num_actions1,1,p=probabilities)
              #  print (probabilities),a_choose,'i= ',i
                if a_choose[0] == 0: #north
                    s_prime_random = s_random[i] - 10
                elif a_choose[0] == 1: #east
                    s_prime_random = s_random[i] + 1
                elif a_choose[0] == 2: #south
                    s_prime_random = s_random[i] + 10
                elif a_choose[0]  == 3: #west
                    s_prime_random = s_random[i] - 1
                elif a_choose[0] == 4: #no move
                    s_prime_random = s_random[i]
              #  print s_random[i],a_random[i],s_prime_random
                
                r_update=self.R.get((s_random[i],a_random[i]))
                Qmaxupdate=max([self.q.get((s_prime_random, a_prime2),0.0) for a_prime2 in range(self.num_actions)])
                self.q[(s_random[i],a_random[i])]=((1-self.alpha)*(self.q[(s_random[i],a_random[i])])+self.alpha*(r_update+self.gamma*(Qmaxupdate))) 
 
 
 #-------------------------Dyna Part
        
        
        if self.verbose: print "s =", s_prime,"a =",action,"r =",r,'q(sp,a)=',self.q[(self.s,self.a)]
        self.a=action
        self.s=s_prime
        return action

if __name__=="__main__":
    print "Remember Q from Star Trek? Well, this isn't him"
