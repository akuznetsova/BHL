from pylab import *
import numpy as np

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
