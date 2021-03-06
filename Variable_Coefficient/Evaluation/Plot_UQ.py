import numpy as np
import matplotlib.pyplot as plt
import csv
import os
import argparse

import scipy.special as special

def main(LAPLACE=False, CAUCHY=False):
    

    legend_entries = []

    #plt.rc('text', usetex=True)
    #plt.rc('font', family='serif')
    
    def smooth(vals, N=20):
        new_vals = vals.copy()
        for n in range(0,vals.size):
            padding = (vals.size - n) - N
            if padding < 0:
                window = [n+k for k in range(padding,vals.size-n)]
            else:
                window = [n+k for k in range(0,N)]
            window_vals = vals[window]
            new_vals[n] = np.mean(window_vals)
        return new_vals

    if LAPLACE:
        filename = "Laplace_UQ_Bounds.csv"
    elif CAUCHY:
        filename = "Cauchy_UQ_Bounds.csv"
    else:
        filename = "Normal_UQ_Bounds.csv"

    stds = []
    t_uqs = []
    v_uqs = []
    with open(filename, "r") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in csvreader:
            std, t_uq, t_std, v_uq, v_std = row
            stds.append(std)
            t_uqs.append(t_uq)
            v_uqs.append(v_uq)
            
    stds = np.array(stds).astype(np.float32)
    t_uqs = 100*np.array(t_uqs).astype(np.float32)
    v_uqs = 100*np.array(v_uqs).astype(np.float32)

    """
    original_losses = losses.copy()
    original_losses = remove_outliers(original_losses)
    ## Smooth out losses
    SMOOTH = True
    if SMOOTH:
        losses = smooth(losses)
        losses = remove_outliers(losses)
    """

    if LAPLACE or CAUCHY:
        plt.plot(stds, t_uqs, linewidth=3.0, color="C0", label="Training")
        plt.plot(stds, v_uqs, linewidth=3.0, color="C1", label='Validation')
    else:
        plt.plot(stds, t_uqs, linewidth=3.0, color="C0", label="Training Dataset")
        plt.plot(stds, v_uqs, linewidth=3.0, color="C1", label='Validation Dataset')

    alpha = 0.1
    y1 = np.zeros(t_uqs.shape)
    plt.fill_between(stds, y1, t_uqs, where=t_uqs >= y1, facecolor="C0", alpha=alpha, interpolate=True, label=None)#, hatch="X", edgecolor="white")
    
    alpha = 0.1
    y1 = np.zeros(v_uqs.shape)
    plt.fill_between(stds, y1, v_uqs, where=v_uqs >= y1, facecolor="C1", alpha=alpha, interpolate=True, label=None)

    
    #plt.scatter(steps, losses, alpha=0.75, marker="s", edgecolor='black', s=100)
    #ax = plt.gca()
    #ax.set_yscale('log')
    #legend_entries.append('%d Training Points' %(data_per_file*k))

    ax = plt.gca()

    # Plot parameters
    linewidth = 3
    titlesize = 24
    ylabelsize = 24
    xlabelsize = 24
    xticksize = 18
    yticksize = 16
    ylabelpad = 20
    xlabelpad = 20

    ax.tick_params(axis='x', labelsize=xticksize)     
    ax.tick_params(axis='y', labelsize=yticksize)

    if LAPLACE or CAUCHY:
        ax.set_xlabel('Scale Parameter', fontsize=xlabelsize, labelpad=20)
    else:
        ax.set_xlabel('Standard Deviations', fontsize=xlabelsize, labelpad=20)
    ax.set_ylabel('Percentage of Dataset', color='k', fontsize=ylabelsize, labelpad=ylabelpad)

    # Dataset Percentage Ticks
    ticks = [n*20 for n in [0,1,2,3,4,5]]
    labels = tuple(["{0:}%".format(n) for n in ticks])
    plt.yticks(ticks, labels, fontsize=yticksize)


    # Scale Paramater Ticks
    ticks = [n*0.5 for n in [1,2,3,4,5,6]]
    if LAPLACE:
        #ticks = [n for n in [1,2,3,4,5,6]]
        labels = tuple([r"{0:}$b$".format(n).replace(".0"," ",1) for n in ticks])
    elif CAUCHY:
        #ticks = [n for n in [1,2,3,4,5,6]]
        labels = tuple([r"{0:}$\gamma$".format(n).replace(".0"," ",1) for n in ticks])
    else:
        #ticks = [n*0.5 for n in [1,2,3,4,5,6]]
        labels = tuple([r"{0:}$\sigma$".format(n).replace(".0"," ",1) for n in ticks])
    #labels = tuple([r"{0:}$\sigma$".format(n).replace(".0"," ",1) for n in ticks])
    plt.xticks(ticks, labels, fontsize=xticksize)
    

    # Retrieve 1-2-3 standard deviation percentages
    training_vals = [t_uqs[i-1] for i in [10,20,30]]
    validation_vals = [v_uqs[i-1] for i in [10,20,30]]
    
    #training_vals = [0.73471046, 0.96861186, 0.99774161]
    #validation_vals = [0.68202384, 0.94649767, 0.99434461]

    #alpha=0.85
    alpha=1.0

    if (not LAPLACE) and (not CAUCHY):
        textstr = '\n'.join((
            #r"3$\sigma$",
            r"Training:    {:.2f}".format(training_vals[2]),
            r"Validation: {:.2f}".format(validation_vals[2])))
        props = dict(boxstyle='round', facecolor='white', alpha=alpha)
        ax.text(0.8, 1.04, textstr, transform=ax.transAxes, fontsize=18,
                verticalalignment='top', bbox=props)

        textstr = '\n'.join((
            #r"3$\sigma$",
            r"Training:    {:.2f}".format(training_vals[1]),
            r"Validation: {:.2f}".format(validation_vals[1])))
        props = dict(boxstyle='round', facecolor='white', alpha=alpha)
        #ax.text(0.635, 0.855, textstr, transform=ax.transAxes, fontsize=18,
        ax.text(0.49, 1.015, textstr, transform=ax.transAxes, fontsize=18,
                verticalalignment='top', bbox=props)

        textstr = '\n'.join((
            #r"3$\sigma$",
            r"Training:    {:.2f}".format(training_vals[0]),
            r"Validation: {:.2f}".format(validation_vals[0])))
        props = dict(boxstyle='round', facecolor='white', alpha=alpha)
        #ax.text(0.345, 0.625, textstr, transform=ax.transAxes, fontsize=18,
        ax.text(0.17, 0.8, textstr, transform=ax.transAxes, fontsize=18,
                verticalalignment='top', bbox=props)


    sigma = 1.0
    #func = lambda x: 2.*100.*(0.5*(1 + special.erf(x/(sigma*np.sqrt(2)))) - 0.5)

    ###
    #    Note:  IR ~ Interquartile Range / VAR ~ variance
    ###
    #
    #  IR_Normal  =  27/20*sigma
    #  IR_Laplace =  2*ln(2)*b      
    #  IR_Cauchy  =  2*gamma
    #
    #  VAR_Normal  =  sigma**2
    #  VAR_Laplace =  2*b**2
    #  VAR_Cauchy  =  DNE
    
    if LAPLACE:
        func = lambda x: 100.*(1.0 - np.exp(-x/sigma))
        # Comparison with normal distribution (using variance)
        #normal_scaling = np.sqrt(2)

        ## EMPIRICAL BIAS
        #normal_scaling = 0.8

        ## TRUE BIAS
        ## http://home.iitk.ac.in/~kundu/paper98.pdf
        ##
        ##  b = sqrt(2/pi)*sigma  ==>  P(|x|<b) = P(|x|<sqrt(2/pi)*sigma)
        ##
        normal_scaling = np.sqrt(2./np.pi)
        
        func_2 = lambda x: 100.*special.erf(x*normal_scaling/np.sqrt(2))
        #true_label=r"$P(|\operatorname{Laplace}(0,b)| \, < \, x)$"
        #true_label="Laplace"
        #true_label=r"$P(|\mathcal{L}(0,b)| \, < \, x)$"
        true_label=r"$P(|\operatorname{Laplace}(0,b)| \, < \, x)$"
    elif CAUCHY:
        func = lambda x: 100.*2./np.pi*np.arctan(x)

        # Test implementation
        #print(func(6.0))
        #print( 100.*( (1./np.pi*np.arctan(6.) + 0.5) - (1./np.pi*np.arctan(-6.) + 0.5) ) )
        
        # Comparison with normal distribution (using interquartile range)
        #normal_scaling = 2.*20./27.

        ## EMPIRICAL BIAS
        # http://www.maths.uq.edu.au/MASCOS/Talks/ASC10.pdf
        # https://stats.stackexchange.com/questions/105934/how-to-calculate-the-scale-parameter-of-a-cauchy-random-variable
        #
        #   "On the unimodality of the likelihood for the Cauchy distribution" by J.B. Copas
        #
        #   MLE(gamma) = gamma s.t. int_R gamma^2/(x^2+gamma^2) * p_N(x) dx =  1/2
        #
        #   For calculation of integral, see Equation 7 of:
        #   https://nvlpubs.nist.gov/nistpubs/jres/73b/jresv73bn1p1_a1b.pdf
        #
        #   Simple WolframAlpha check:
        #   int(0.612003^2/(x^2+0.612003^2)*1/sqrt(2*pi)*e^(-x^2/2),x,-5000,5000)
        #
        normal_scaling = 0.612003
        func_2 = lambda x: 100.*special.erf(x*normal_scaling/np.sqrt(2))
        
        true_label=r"$P(|\operatorname{Cauchy}(0,\gamma)| \, < \, x)$"
        #true_label="Cauchy"
    else:
        func = lambda x: 100.*special.erf(x/np.sqrt(2))
        true_label=r"$P(|\mathcal{N}(0,\sigma)| \, < \, x)$"

    #plt.plot(stds, func(stds), 'r--', linewidth=2, alpha=0.5, zorder=0, label=r"$P(|\mathcal{N}(0,\sigma)| \, < \, x)$")
    
    
    if LAPLACE:
        normal_label=r"$P(|\mathcal{N}(0,\sqrt{\pi\,/\,2}\cdot b)| \, < \, x)$"
        plt.plot(stds, func(stds), 'r--', linewidth=2.5, alpha=0.5, zorder=0, label=true_label)
        plt.plot(stds, func_2(stds), 'k--', linewidth=2.5, alpha=1.0, zorder=0, label=normal_label)
    elif CAUCHY:
        #normal_label=r"$P(|\mathcal{N}(0,0.612\cdot \gamma)| \, < \, x)$"
        normal_label=r"$P(|\mathcal{N}(0,1.634\cdot \gamma)| \, < \, x)$"
        plt.plot(stds, func(stds), 'r--', linewidth=2.5, alpha=0.5, zorder=0, label=true_label)
        plt.plot(stds, func_2(stds), 'k--', linewidth=2.5, alpha=1.0, zorder=0, label=normal_label)
    else:
        plt.plot(stds, func(stds), 'r--', linewidth=2, alpha=0.5, zorder=0, label=true_label)
        
    #plt.plot(stds, func(stds), 'r--', linewidth=2, alpha=0.5, zorder=0, label=r"$\operatorname{erf}(x/\sqrt{2})$")
    
    
    # Add dots at 1/2/3 standard deviation points
    """
    if LAPLACE or CAUCHY:
        xvals = [2,4,6]
    else:
        xvals = [1,2,3]
    """
    xvals = [1,2,3]
    #coords = [73.471046, 96.861186, 99.774161]
    coords = training_vals
    plt.scatter(xvals,coords, color='C0', s=60, zorder=5)

    #coords = [68.202384, 94.649767, 99.434461]
    coords = validation_vals
    plt.scatter(xvals,coords, color='C1', s=60, zorder=9)


    # Add dashed lines
    alpha = 0.25
    #plt.plot([1, 1], [0.0, 73.47], 'k--', lw=2, alpha=alpha)
    #plt.plot([2, 2], [0.0, 96.86], 'k--', lw=2, alpha=alpha)
    #plt.plot([3, 3], [0.0, 99.77], 'k--', lw=2, alpha=alpha)
    """
    if LAPLACE or CAUCHY:
        x_coords = [[2,2],[4,4],[6,6]]
    else:
        x_coords = [[1,1],[2,2],[3,3]]
    """
    x_coords = [[1,1],[2,2],[3,3]]
    plt.plot(x_coords[0], [0.0, training_vals[0]], 'k--', lw=2, alpha=alpha)
    plt.plot(x_coords[1], [0.0, training_vals[1]], 'k--', lw=2, alpha=alpha)
    plt.plot(x_coords[2], [0.0, training_vals[2]], 'k--', lw=2, alpha=alpha)

    
    #ax.legend(legend_entries, fontsize=24)
    #ax.legend(fontsize=24)
    #ax.legend(fontsize=24, loc=(0.05,0.85), framealpha=1.0)
    if LAPLACE or CAUCHY:
        ncol=2
    else:
        ncol=1
    ax.legend(fontsize=24, loc=(0.05,0.88), framealpha=1.0, ncol=ncol)
    plt.show()




    
# Run main() function when called directly
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--laplace", default=False, action="store_true", help="Use Laplace distribution")
    parser.add_argument("--cauchy", default=False, action="store_true", help="Use Cauchy distribution")
    args = parser.parse_args()    
    main(args.laplace, args.cauchy)
