from pylab import *
import numpy as np
import os
from IPython.display import Image
from IPython.display import display

def print_stat(t,dmdt,m,alpha=0):
    print '-----------------------------'
    print 'time = {}'.format(t)
    print 'N={}'.format(len(m))
    print '-----------------------------'
    print 'Median M [Msol]: {}'.format(np.median(m))
    print 'Min/Max M [Msol]: {} to {}'.format(np.amin(m),np.amax(m))
    print '-----------------------------'
    print 'Median  dm/dt: {}'.format((np.median(dmdt)))
    print 'Min/Max dm/dt: {} to {}'.format((np.amin(dmdt)),(np.amax(dmdt)))
    print '-----------------------------'
    print 'Median alpha: {}'.format(np.median(alpha))
    print 'Min/max alpha: {} to {}'.format(np.amin(alpha),np.amax(alpha))

def zero(t): #yeah yeah this function is dumb
    t = int(t)
    if t < 10:
        return '000000' + str(t)
    elif t < 100:
        return '00000' + str(t)
    elif t < 1000:
        return '0000' + str(t)
    elif t < 10000:
        return '000' + str(t)
    elif t < 100000:
        return '00'+ str(t)
    elif t < 1000000:
        return '0' + str(t)
    else:    
        return str(t)

def plot_acc(t,dmdt,m,ext='.png'):
    f,ax = subplots(1)
    #cval = t/tend
    #ax.scatter(np.log10(m),np.log10(dmdt),c=cm.plasma_r(cval))
    ax.scatter(np.log10(m),np.log10(dmdt),c='k')
    ax.plot(np.linspace(-2,2,10), np.linspace(-2,2,10)*2 - 8, 'k--')
    ax.set_xlabel('$\log$ $M$ $[M_{\odot}]$',fontsize=12)
    ax.set_ylabel('$\log$ $\dot{M}$ $[M_{\odot} yr^{-1}]$',fontsize=12)
    ax.set_xlim(-2,2)
    ax.set_ylim(-12,-4)
    f.savefig('f_acc_'+zero(t)+ext)
    close(f)
    
def plot_mf(t,m,N0,m0,imf=True,ext='.png'): #default plots the original M0 distribution
    f,ax = subplots(1)
    #cval = t/tend
    N = len(m[~np.isinf(m)])
    ax.text(1.,N0/3,'Time:{} Myr'.format(np.round(t/1.0e6,3)))
    ax.text(1.,N0/4,'N:{}'.format(N))
    ax.hist(np.log10(m),log=True,histtype='step',lw=2,bins=np.linspace(-2,2,25),color='k')
    if imf == True:
        ax.hist(np.log10(m0),log=True,histtype='step',lw=2,bins=np.linspace(-2,2,25),color='gray')
    xr = np.arange(-4,1)+2.5
    yr = [10**3,100, 10, 1,0.1]
    ax.plot(xr,yr,'k--')
    ax.set_ylim(1,N0/2.)
    ax.set_xlim(-2,2)
    ax.set_xlabel('$\log$ $M$ $[M_{\odot}]$',fontsize=12)
    ax.set_ylabel('$dN/d\log M$',fontsize=12)
    f.savefig('f_mf_'+zero(t)+ext)
    close(f)

def clear_png():
    os.system('rm f_*.png')

def clear_gif():
    os.system('rm f_*.gif')

def movie(path):
    with open(path,'rb') as f:
        display(Image(data=f.read(), format='png'))
