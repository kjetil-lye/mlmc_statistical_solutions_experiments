import netCDF4
import numpy as np
import plot_info
import matplotlib.pyplot as plt

def load(filename):
    samples = []
    variables = ['rho', 'mx', 'my', 'E']
    
    with netCDF4.Dataset(filename) as f:
        for attr in f.ncattrs():
            plot_info.add_additional_plot_parameters(filename.replace("/", "_") + "_" + attr, f.getncattr(attr))
        
        sample = 0
        shape = f.variables['sample_0_rho'][:,:,0].shape
        while f'sample_{sample}_rho' in f:
            data = np.zeros((*shape, len(variables)))
            for n, variable in enumerate(variables):
                key = f'sample_{sample}_{variable}'
                data[:,:,n] = f.variables[key][:,:,0]
            samples.append(data)
            sample += 1
                
                
    return np.array(samples)

def compute_variance_decay_normed(resolutions, basenames, norm_ord):
    variances = []
    variances_details = []
    
    for resolution in resolutions:
        data = load(basenames.format(resolution=resolution))
        variance_single_level = np.linalg.norm(np.var(data, axis=0), ord=norm_ord)
        
        variances.append(variance_single_level)
        if resolution > resolutions[0]:
            detail = data - data_coarse
            
            variance_detail = np.linalg.norm(np.var(detail, axis=0), ord=norm_ord)
            
            
            variances_details.append(variance_detail)
        data_coarse = np.repeat(np.repeat(data,2,1), 2, 2)
            
    return variances, variances_details


def plot_variance_decay_normed(title, resolutions, basenames, norm_ord):
    variances, variances_details = compute_variance_decay_normed(resolutions, basenames, norm_ord)
    
    plt.loglog(resolutions, variances, '-o', 
               label=f'$||\\mathrm{{Var}}(u^{{N}})||_{{L^{{{norm_ord}}}}}$')
    
    
    plt.loglog(resolutions[1:], variances_details, '-*', 
               label=f'$||\\mathrm{{Var}}(u^{{N}}-u^{{N/2}})||_{{L^{{{norm_ord}}}}}$',
               basex=2, basey=2)
    
    plt.legend()
    
    plt.xlabel("Resolution ($N\\times N$)")
    
    plt.ylabel("Variance")
    
    plt.xticks(resolutions, [f'${r}\\times {r}$' for r in resolutions])
    
    plt.title(f'Variance decay\n{title}')
    
    plot_info.savePlot(f'variance_decay_{norm_ord}_{title}')
    
    plot_info.saveData(f'variance_details_{norm_ord}_{title}.txt', variances_details)

    plot_info.saveData(f'variance_{norm_ord}_{title}.txt', variances)
    
    plot_info.saveData(f'variance_decay_resolutions_{norm_ord}_{title}.txt', resolutions)
            
    
if __name__ == '__main__':
    
    
    import argparse

    parser = argparse.ArgumentParser(description="""
Computes the variance decay
            """)

    parser.add_argument('--input_basename', type=str, required=True,  
                        help='Input filename (should have a format string {resolution})')

    parser.add_argument('--title', type=str, required=True,
                        help='Title of plot')



    parser.add_argument('--starting_resolution', type=int, default=32,
                        help='Starting resolution (smallest resolution)')
    

    parser.add_argument('--max_resolution', type=int, default=1024,
                        help='Maximum resolution')
    
    parser.add_argument('--norm_order', type=int, default=2,
                        help='The norm order')
    
    args = parser.parse_args()


    resolutions = 2**np.arange(int(np.log2(args.starting_resolution)),
                               int(np.log2(args.max_resolution)+1))
    
    
    plot_variance_decay_normed(args.title, resolutions,
                               args.input_basename, args.norm_order)