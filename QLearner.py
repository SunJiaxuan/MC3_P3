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
        verbose = False):

        self.verbose = verbose
        self.num_actions = num_actions
        self.s = 0
        self.a = 0
        
        self.rar=rar
        self.radr=radr
        self.alpha=alpha
        self.gamma=gamma
        self.dyna=dyna
        self.num_states=num_states
        
        
        self.q={}
        
        self.T={}
        self.R={}
        
      #  print self.rar,self.verbose,self.dyna,self.num_states,self.alpha,self.gamma,self.radr
        
        for s,a in  np.ndindex((num_states,num_actions)): self.q[(s,a)]=np.random.random_integers(-1, 1)
    

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
        
        newQmax=max([self.q.get((s_prime, a_prime),0.0) for a_prime in range(self.num_actions)]) 
           
        self.q[(self.s,self.a)]=((1-self.alpha)*(self.q[(self.s,self.a)])+self.alpha*(r+self.gamma*(newQmax)))
        
        if np.random.random()<self.rar:
            action = rand.randint(0, self.num_actions-1)
        else:
            actions=[self.q.get((s_prime, i), 0.0) for i in range(self.num_actions)]
            max_A=max(actions)
            action= np.random.choice([i for i, j in enumerate(actions) if j == max_A])

          
        self.rar *=self.radr
            
        # blend of highest value + random choice
        
        
        if self.verbose: print "s =", s_prime,"a =",action,"r =",r,'q(sp,a)=',self.q[(self.s,self.a)]
        self.a=action
        self.s=s_prime
        
        return action

if __name__=="__main__":
    print "Remember Q from Star Trek? Well, this isn't him"
