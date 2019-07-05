import scipy.stats
# Uses fbmpy from https://github.com/kjetil-lye/fractional_brownian_motion
# (this is also a part of alsvinn)
def init_global(rho, ux, uy, p, nx, ny, nz, ax, ay, az, bx, by, bz):
    Y = scipy.stats.norm.ppf(X)
    dux = fbmpy.fractional_brownian_bridge_2d(hurst_index, nx,
                                              Y[:nx**2]).reshape(nx+1, nx+1)
    duy = fbmpy.fractional_brownian_bridge_2d(hurst_index, nx,
                                              Y[nx**2:]).reshape(nx+1, nx+1)
    rho[:,:,0] = 4*ones_like(rho[:,:,0])
    ux[:,:,0] = dux[:-1,:-1]
    uy[:,:,0] = duy[:-1,:-1]
    p[:,:,0] = 2.5*ones_like(rho[:,:,0])



