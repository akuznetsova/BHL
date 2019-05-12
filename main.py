from pylab import *
import numpy as np
import output as out
from ipywidgets import FloatProgress
from IPython.display import display

# Main Evolution and Computation Functions #

#----------------------------------------------------------------------------------------------
# Initialize Distributions
#----------------------------------------------------------------------------------------------


## pulls *N* samples from an initial m0 distribution centered at *mu* with a width *sigma*
## kwargs: p => if True plots the distribution 

def get_m0(mu,sigma,N,p=False):
    m0 = np.random.normal(mu, sigma, N)
    if p == True:
        hist(m0,log=True,histtype='step',lw=2,bins=np.linspace(-2,2,40))
        xr = np.arange(-4,1)+2.5
        yr = [10**3,100, 10, 1,0.1]
        plot(xr,yr,'k--')
        ylim(1,N/2)
        xlim(-2,2)
        xlabel('$\log$ $M_{0}$ $[M_{\odot}]$',fontsize=12)
        ylabel('$dN/d{\log M_{0}}$',fontsize=12)
        show()
    return 10**m0

## pulls *N* samples from an alpha distribution centered at *alpha_mu* with a width *alpha_sig*
## kwargs: log => if True distribution is log-normal with the input being a log
##         p   => if True plots the alpha distribution

def get_alpha(alpha_mu,alpha_sig,N,log=True, p=False):
    alphai = np.random.normal(alpha_mu,alpha_sig,N)
    if log==True:
        alpha = 10**alphai
    if log == False:
        alpha = np.abs(alphai)
    if p == True:
            hist(np.log10(alpha),log=True,histtype='step',lw=2)
            xlabel(r'$ \log \alpha_0$')
            ylabel(r'$dN/d{\log \alpha_{0}}$',fontsize=12)
    return alpha

# -----------------------------------------------------------------------------------------------
# Evolution
#------------------------------------------------------------------------------------------------

def test_m(m): # test whether any mass is bad
    if np.isinf(m).any():
        return 1
    else:
        return 0

def delete_inf(m):
    return m[~np.isinf(m)]

#---------------------------------------------------------------------------------------------------------------------------
# Main Function #
#---------------------------------------------------------------------------------------------------------------------------

def main(m0,tend,dt = 5,alpha=6.0e-6,eps=False,progress=True):
    t = 0
    out_dt = tend/100.
	## advances integrated mass and time 
	## kwargs: alpha_dep => if True, then the threshold mass criterion kicks in and drops alpha for 
	##                      high mass stars
    def get_mi(m,alpha,t,dt,alpha_dep=True): #get the next mass for growth
	    dm = alpha*(m**2)
	    # evolve masses
	    if alpha_dep == True: #depletes alpha for massive stars
		i = np.where(m >= 8.) 
		if isinstance(alpha,float):
		    dm[i] = (alpha/(20.*(t/tend + 1.)))*(m[i]**2)
		else:
		    dm[i] = (alpha[i]/(20.*(t/tend + 1. )))*(m[i]**2)
	    else:
		i = np.where(m >= 80.) #does not let stars exceed highest mass limits
		dm[i] = 10**(-18) #token accretion rates
	    m += dm*dt
	    t += dt
	    return t, dm/dt, m
    #if you put in list of m0 properties, you can create variable sfr
    if isinstance(m0,list):
        m0_mu = m0[0]
        m0_sig = m0[1]
        N0 = m0[2]
        sfr = m0[3] #cadence of sfr in time units for N0 stars in that time
        m = get_m0(m0_mu,m0_sig,N0,p=False)
    #if you just put in an m0 array, there is no variable sfr, all are created at once
    else:
        m = (m0.copy())
	N0 = len(m)
    #Progress Bar
    if progress == True:
        f = FloatProgress(min=0, max=100)
        display(f)
    #Main integration loop
    while t <= tend-dt:
        if t == 0:
            out.print_stat(t,0,m) # initial print statement
        # Error contingency
        if test_m(m) == 1:
            m = delete_inf(m)
            print '----- OVERFLOW MASS THROWN OUT -----'
            out.print_stat(t,dmdt,m)
       
        # number of stars
        N = len(m)
        ##-------------------------------------------------------
        ## Alpha distributions
        ##--------------------------------------------------------
        # if you just put in one number, alpha is a constant
        if isinstance(alpha,float):
            alpha_in = alpha
        #if you put in a tuple (mu,sig), it will draw the distribution with the values of the tuple
        elif isinstance(alpha,tuple):
            alpha_mu0 = alpha[0]
            alpha_sig0 = alpha[1]
            alpha_in = get_alpha(alpha_mu0,alpha_sig0,N,log=True,p=False)
        #if you put in a 4 element list you can define a simple power law for the mean of alpha to follow with time
        elif isinstance(alpha,list):
            alpha_mu0 = alpha[0]
            alpha_sig0 = alpha[1]
            alpha_slope = alpha[2]
            alpha_power = alpha[3]
            alpha_in = get_alpha(alpha_mu0- alpha_slope*(t/tend)**(alpha_power),alpha_sig0,N,log=True,p=False) 
        # ----------------------------------------------------------------
        #Advance the integration
        t, dmdt,m = get_mi(m,alpha_in,t,dt)
         # Regular outputs
        if t%(out_dt) == 0:
            if progress == True:
                f.value +=1
            #plot_acc(t,dmdt,m)
            if isinstance(m0, list):
                out.plot_mf(t,m,N0*(tend/sfr),m,imf=False)
            else:
                out.plot_mf(t,m,N0,m0) # WARNING: will make a ton of pngs to make the movies out of in your folder
            out.plot_acc(t,dmdt,m)
        #Make a vector graphic every 10 dumps
        if eps == True:
            if t%(out_dt*10) == 0:
                out.plot_acc(t,dmdt,m,ext='.eps')
                if isinstance(m0,list):
                    out.plot_mf(t,m,N0*(tend/sfr),m,imf=False,ext='.eps')
                else:
                    out.plot_mf(t,m,N0,m0,ext='.eps')

        #Make new stars if you need to
        if isinstance(m0,list):
            if t%(sfr) == 0:
                m = np.append(m,get_m0(m0_mu,m0_sig,N0,p=False))
                dmdt = np.append(dmdt,np.ones(N0)*10**(-20))

        #Ending stats
        if tend -t < dt:
            out.print_stat(t,dmdt,m,alpha=alpha_in)
            #plot_acc(t,dmdt,m)
    return t, dmdt,m
