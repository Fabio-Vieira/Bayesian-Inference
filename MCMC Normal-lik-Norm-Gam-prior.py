#Bayesian Inference for the parameters of a normal distribution, using a normal-gamma prior.
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

x = np.random.normal(loc = 5.7, scale = 4, size = 100)
plt.hist(x)

#print(x.var())
#print(x.mean())

#Initial values
init = [0.0, 1.0]

#Prior hyperparameters
priorMu = [0.0, 100.0]
priorSig = [0.1, 0.1]

#Defining functions for MCMC

#Function to update the mean
def updateMu(sig, x, priorMu):
    n = len(x)
    sigMuPost = 1/(n/sig + 1/priorMu[1])
    mMuPost = sigMuPost * (sum(x)/sig + priorMu[0]/priorMu[1])
    
    return np.random.normal(loc = mMuPost, scale = math.sqrt(sigMuPost), size = 1)

#Function to update the variance
def updateSig(mu, x, priorSig):
    n = len(x)
    aPost = n/2 + priorSig[0]
    sumsq = sum((x - mu)**2)
    bPost = sumsq/2 + priorSig[1]
    
    return 1/np.random.gamma(shape = aPost, scale = 1/bPost, size = 1)

#Defining MCMC function
def MCMC(x, priorMu, priorSig, init, niter = 50000, burnin = 25000):
    post = np.zeros(shape = (niter, 2))
    for i in range(niter):
        if i == 0 :
            post[i,0] = updateMu(init[1], x, priorMu)
            post[i,1] = updateSig(init[0], x, priorSig)
        else :
            post[i,0] = updateMu(post[i-1,1], x, priorMu)
            post[i,1] = updateSig(post[i-1,0], x, priorSig)
        print(i)
    
    return pd.DataFrame(post[(burnin):,], columns = ["mean", "variance"])
      
#How do I indicate I got out of the function?    
df = MCMC(x, priorMu, priorSig, init)
df.head()
df.mean()
df.var()

plt.plot(df[["mean"]])
plt.plot(df[["variance"]])
