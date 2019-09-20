import netCDF4
import numpy as np
import plot_info
import matplotlib.pyplot as plt
import sys


def speedup_mlmc(variances, levels, work):

    # We assume we use 10 000 samples on the finest level for MC
    # and find the work for MLMC using said error tolerance
    Mbase = 10000
    workBase = work[-1]*Mbase
    errorMCBase = variances[-1]/Mbase

    maxLevel = len(variances)

    bestConfiguration = {'L':0,
                         'M': [Mbase],
                         'Speedup' : 1,
                         'variance' : max(variances),
                         'work' : [work[-1]],
                         'sigma2':[variances[-1]],
                         'workBase' : workBase,
                         'error': errorMCBase}

    for L in range(1, maxLevel):
        sigmas2 = np.zeros(L+1)
        sigmas2[0] = variances[-L-1]
        sigmas2[1:] = levels[-L:]
        workLocal = work[-L-1:]
        sumSigmaWork = np.sum(np.sqrt(sigmas2*workLocal))
        M = np.zeros(L+1)
        M = 1.0/errorMCBase * (np.sqrt(sigmas2/workLocal))*sumSigmaWork
        M = np.ceil(M)
        workConfiguration = np.sum(M*workLocal) + np.sum(M[1:]*workLocal[:-1])
        speedup = workBase/workConfiguration

        errorMLMC = np.sum(sigmas2/M)


        # We actually get some floating point errors, therefore, we need to adjust our expectations a bit
        epsilon = 10*max(errorMCBase*(np.finfo(type(errorMCBase)).eps), errorMLMC*np.finfo(type(errorMCBase)).eps)

        if  errorMLMC > errorMCBase + epsilon:
            raise Exception("MLMC could not match MC error, MLMC_Error=%s, MC_error=%s" %
                            (np.float64(errorMLMC), np.float64(errorMCBase)))



        if speedup > bestConfiguration['Speedup']:
            bestConfiguration = {'L' : L,
                                 'M':M,
                                 'Speedup':speedup,
                                'variance':max(variances),
                                 'work' : workLocal,
                                 'sigma2':sigmas2,
                                 'workBase' : workBase,
                                  'error': errorMCBase}


    return bestConfiguration


def compute_speedup(resolutions, variance_single_level, variance_multilevel):
    resolutions = np.array(resolutions)
    
    work = resolutions**3
    
    best_speedup = speedup_mlmc(variance_single_level, variance_multilevel, work)
    
    
    return best_speedup['Speedup']
    

def load(filename, variable):
    samples = []
    
    if variable == 'all':
        variables = ['rho', 'mx', 'my', 'E']
    else:
        variables = [variable]
    
    with netCDF4.Dataset(filename) as f:
        for attr in f.ncattrs():
            plot_info.add_additional_plot_parameters(filename.replace("/", "_") + "_" + attr, f.getncattr(attr))
        
        sample = 0
        shape = f.variables['sample_0_rho'][:,:,0].shape
        next_sample_to_print = 1
        while f'sample_{sample}_rho' in f.variables.keys():
            if sample % 80 > next_sample_to_print:
                sys.stdout.write("#")
                sys.stdout.flush()
                next_sample_to_print += 1
            
            data = np.zeros((*shape, len(variables)))
            for n, variable in enumerate(variables):
                key = f'sample_{sample}_{variable}'
                data[:,:,n] = f.variables[key][:,:,0]
            samples.append(data)
            sample += 1
                
    print()
    return np.array(samples)

def compute_variance_decay_normed(resolutions, basenames, norm_ord, variable):
    variances = []
    variances_details = []
    
    for resolution in resolutions:
        print(f"Resolution: {resolution}")
        data = load(basenames.format(resolution=resolution), variable)
        variance_single_level = np.linalg.norm(np.var(data, axis=0).flatten(), ord=norm_ord)/float(resolution)**(2/norm_ord)
        
        variances.append(variance_single_level)
        if resolution > resolutions[0]:
            detail = data - data_coarse
            
            variance_detail = np.linalg.norm(np.var(detail, axis=0).flatten(), ord=norm_ord)/float(resolution)**(2/norm_ord)
            
            
            variances_details.append(variance_detail)
        if resolution < resolutions[-1]:
            data_coarse = np.repeat(np.repeat(data,2,1), 2, 2)
            
    return variances, variances_details


def plot_variance_decay_normed(title, resolutions, basenames, norm_ord, variable):
    variances, variances_details = compute_variance_decay_normed(resolutions, 
                                                                 basenames,
                                                                 norm_ord,
                                                                 variable)
    
    
    speedups = [1]
    
    for n in range(1, len(resolutions)):
        local_resolutions = resolutions[:n+1]
        
        speedup = compute_speedup(local_resolutions, 
                                  variances[:n+1],
                                  variances_details[:n])
        
        speedups.append(speedup)
        
        
    
    if variable == 'all':
        variable_latex = 'u'
    elif variable == 'rho':
        variable_latex = '\\rho'
    elif variable == 'mx':
        variable_latex = 'm_x'
    elif variable == 'my':
        variable_latex = 'm_y'
    else:
        variable_latex = variable
    
    
        
    fig, ax1 = plt.subplots()
    ax1.loglog(resolutions, variances, '-o', 
               label=f'$||\\mathrm{{Var}}({variable_latex}^{{N}})||_{{L^{{{norm_ord}}}}}$')
    
    
    ax1.loglog(resolutions[1:], variances_details, '-*', 
               label=f'$||\\mathrm{{Var}}({variable_latex}^{{N}}-{variable_latex}^{{N/2}})||_{{L^{{{norm_ord}}}}}$',
               basex=2, basey=2)
    
    ax1.legend()
    
    ax1.set_xlabel("Resolution ($N\\times N$)")
    
    ax1.set_ylabel("Variance")
    
    ax1.set_xticks(resolutions, [f'${r}\\times {r}$' for r in resolutions])
    
    plt.title(f'Variance decay\n{title}\nVariable: {variable}')
    
    plot_info.savePlot(f'variance_decay_{norm_ord}_{title}_{variable}')
    
    plot_info.saveData(f'variance_details_{norm_ord}_{title}_{variable}.txt', variances_details)

    plot_info.saveData(f'variance_{norm_ord}_{title}_{variable}.txt', variances)
    
    plot_info.saveData(f'variance_decay_resolutions_{norm_ord}_{title}_{variable}.txt', resolutions)
    
    ax2 = ax1.twinx()

    
    
    ax2.plot(resolutions, speedups, '--x', label='MLMC Speedup')
    ax2.legend(loc=0)
    ax2.set_ylabel("Potential MLMC speedup")
    ax2.set_xticks(resolutions, [f'${r}\\times {r}$' for r in resolutions])
            
    plot_info.savePlot(f'variance_decay_with_speedup_{norm_ord}_{title}_{variable}')
    
    plot_info.saveData(f'variance_decay_speedups_{norm_ord}_{title}_{variable}.txt', speedups)
     
if __name__ == '__main__':
    
    
    import argparse

    parser = argparse.ArgumentParser(description="""
Computes the variance decay
            """)

    parser.add_argument('--input_basename', type=str, required=True,  
                        help='Input filename (should have a format string {resolution})')

    parser.add_argument('--title', type=str, required=True,
                        help='Title of plot')



    parser.add_argument('--starting_resolution', type=int, default=64,
                        help='Starting resolution (smallest resolution)')
    

    parser.add_argument('--max_resolution', type=int, default=1024,
                        help='Maximum resolution')
    
    parser.add_argument('--norm_order', type=int, default=2,
                        help='The norm order')
    
    parser.add_argument('--variable', type=str, default='all',
                        help='The variable to use (rho, mx, my, E)')
    
    args = parser.parse_args()


    resolutions = 2**np.arange(int(np.log2(args.starting_resolution)),
                               int(np.log2(args.max_resolution)+1))
    
    
    plot_variance_decay_normed(args.title, resolutions,
                               args.input_basename, args.norm_order,
                               args.variable)
