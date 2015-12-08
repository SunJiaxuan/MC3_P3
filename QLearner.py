"""
Template for implementing QLearner  (c) 2015 Tucker Balch

QLearner (c) 2015 Frank DiMeo
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
        self.itter=0
        
        self.q={}      
        self.R={}
        
#initiallize Q table, Tc, and R table
                    
        for s,a in  np.ndindex((num_states,num_actions)): self.q[(s,a)]=np.random.random_integers(-1, 1) 
        
        if self.dyna>0:
            
            self.Tc=np.empty(num_states*num_actions*num_states).reshape(num_states,num_actions,num_states)
            self.Tc.fill(0.00001)
            self.T=self.Tc/self.Tc.sum(axis=2,keepdims=True)  

            for i,j in np.ndindex((num_states,num_actions)):self.R[(i,j)]=-1             

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
        @param r: The reward
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
        self.itter+=1
       
       
#-------------------------Dyna Part
        if self.dyna>0:
            
            self.Tc[self.s,self.a,s_prime]+=1
            self.T=self.Tc/self.Tc.sum(axis=2,keepdims=True) 
            self.R[(self.s,self.a)]=(1-self.alphar)*(self.R[(self.s,self.a)])+(self.alphar*r)

            # initiallizes array of s,a for use in dyna loop
            dyna_s=np.random.random_integers(0,self.num_states-1,self.dyna)
            dyna_a=np.random.random_integers(0,self.num_actions-1,self.dyna)
          
        if self.dyna>0 and self.itter>10:
        # seeds first couple of itterations before starting dyna looping     
            for i in range(0,self.dyna):
              
                #dyna_s_prime=np.random.choice(self.num_states,1,replace=True,p=self.T[dyna_s[i],dyna_a[i],])
                #the avbove step is the rate limiting method call, 
                dyna_s_prime=np.random.multinomial(1, self.T[dyna_s[i],dyna_a[i],]).argmax()
                #the above is about 4-5 times faster than choice method
                dyna_r=self.R.get((dyna_s[i],dyna_a[i]),0.0)
                Qmaxupdate=max([self.q.get((dyna_s_prime, a_prime2),0.0) for a_prime2 in range(self.num_actions)])
                self.q[(dyna_s[i],dyna_a[i])]=((1-self.alpha)*(self.q[(dyna_s[i],dyna_a[i])])+self.alpha*(dyna_r+self.gamma*(Qmaxupdate))) 
 
 
 #-------------------------Dyna Part
        
        
        if self.verbose: print "s =", s_prime,"a =",action,"r =",r,'q(sp,a)=',self.q[(self.s,self.a)]
        self.a=action
        self.s=s_prime
        return action

if __name__=="__main__":
    print "Remember Q from James Bond? Well, this IS him"
