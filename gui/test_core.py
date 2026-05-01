import borshtanga_core


params = borshtanga_core.BorshtangaParams()
params.G = 8.1e10           
params.rho = 7850.0         
params.Jp = 1.0e-7          
params.Jr = 0.01            
params.L = 2.5             
params.delta1 = 1.0e-5      

result = borshtanga_core.compute_delta_hat(params, omega=100.0)
print(f"δ̂ при ω=100: {result}")
print(f"  Re(δ̂) = {result.real:.4f}")
print(f"  Im(δ̂) = {result.imag:.4f}")


curve = borshtanga_core.build_d_curve(params, omega_min=-500, omega_max=500, num_points=1000)
print(f"\nПостроена кривая из {len(curve)} точек")
print(f"Первые 3 точки: {curve[:3]}")
print(f"Последние 3 точки: {curve[-3:]}")