import netCDF4
import numpy as np
import plot_info
import matplotlib.pyplot as plt
import sys

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
        variance_single_level = np.linalg.norm(np.var(data, axis=0).flatten(), ord=norm_ord)/resolution**2
        
        variances.append(variance_single_level)
        if resolution > resolutions[0]:
            detail = data - data_coarse
            
            variance_detail = np.linalg.norm(np.var(detail, axis=0).flatten(), ord=norm_ord)/resolution**2
            
            
            variances_details.append(variance_detail)
        if resolution < resolutions[-1]:
            data_coarse = np.repeat(np.repeat(data,2,1), 2, 2)
            
    return variances, variances_details


def plot_variance_decay_normed(title, resolutions, basenames, norm_ord, variable):
    variances, variances_details = compute_variance_decay_normed(resolutions, 
                                                                 basenames,
                                                                 norm_ord,
                                                                 variable)
    
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
    
    
        
    
    plt.loglog(resolutions, variances, '-o', 
               label=f'$||\\mathrm{{Var}}({variable_latex}^{{N}})||_{{L^{{{norm_ord}}}}}$')
    
    
    plt.loglog(resolutions[1:], variances_details, '-*', 
               label=f'$||\\mathrm{{Var}}({variable_latex}^{{N}}-{variable_latex}^{{N/2}})||_{{L^{{{norm_ord}}}}}$',
               basex=2, basey=2)
    
    plt.legend()
    
    plt.xlabel("Resolution ($N\\times N$)")
    
    plt.ylabel("Variance")
    
    plt.xticks(resolutions, [f'${r}\\times {r}$' for r in resolutions])
    
    plt.title(f'Variance decay\n{title}\nVariable: {variable}')
    
    plot_info.savePlot(f'variance_decay_{norm_ord}_{title}_{variable}')
    
    plot_info.saveData(f'variance_details_{norm_ord}_{title}_{variable}.txt', variances_details)

    plot_info.saveData(f'variance_{norm_ord}_{title}_{variable}.txt', variances)
    
    plot_info.saveData(f'variance_decay_resolutions_{norm_ord}_{title}_{variable}.txt', resolutions)
            
    
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
