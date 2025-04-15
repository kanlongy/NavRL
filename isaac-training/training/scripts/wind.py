import torch

class WindModel:
    def __init__(self, device, num_envs, 
             base_speed=1.0, 
             base_direction=torch.tensor([1.0, 0.0, 0.0]), 
             variable_speed=False, 
             variable_direction=False,
             fluid_density=1.225, 
             drag_coefficient=0.102, 
             cross_section_area=0.181,
             drag_scale_range=(0.8, 1.2),
             area_scale_range=(0.9, 1.1)):
        
        self.device = device
        self.num_envs = num_envs
        self.base_speed = base_speed
        self.base_direction = base_direction.to(device).float()
        self.variable_speed = variable_speed
        self.variable_direction = variable_direction
        self.rho = fluid_density
        self.C_D = drag_coefficient * torch.empty(num_envs, device=device).uniform_(*drag_scale_range)
        self.area = cross_section_area * torch.empty(num_envs, device=device).uniform_(*area_scale_range)
        self.t = 0.0
        self.local_wind_direction = torch.nn.functional.normalize(
        torch.randn(num_envs, 3, device=device), dim=1)
        self.local_wind_strength = torch.full((num_envs,), self.base_speed, device=device)
        self.wind_velocity_buffer = torch.zeros(num_envs, device=device)

    def step(self, dt):
        self.t += dt

        if self.variable_speed:
            #1. The magnitude follows a Beta distribution, with a bias toward gentle breezes and occasional strong winds.
            #new_strength = torch.distributions.Beta(2.0, 5.0).sample((self.num_envs,)).to(self.device) 
            #alpha = 0.8  # The larger, the more stable 
            #self.local_wind_strength = alpha * self.local_wind_strength + (1 - alpha) * new_strength
            #self.wind_velocity_buffer = self.base_speed * 1.5 * self.local_wind_strength

            #2. The magnitude follows a Gaussian distribution
            mean=self.base_speed      
            std = 2                      # control fluctuation
            min_speed = 0.0
            max_speed = 10.0
            scale = 1.0                   # optional multiplier if needed

            new_strength = torch.normal(mean=mean, std=std, size=(self.num_envs,), device=self.device)
            new_strength = torch.clamp(new_strength, min=min_speed, max=max_speed)
            alpha = 0.6
            self.local_wind_strength = alpha * self.local_wind_strength + (1 - alpha) * new_strength
            self.wind_velocity_buffer = self.local_wind_strength * scale
        
        if self.variable_direction:
            # Random direction covering full sphere + smoothed update
            new_dirs = torch.randn(self.num_envs, 3, device=self.device)
            new_dirs = torch.nn.functional.normalize(new_dirs, dim=1)
            
            alpha_dir = 0.8
            self.local_wind_direction = torch.nn.functional.normalize(
                alpha_dir * self.local_wind_direction + (1 - alpha_dir) * new_dirs,
                dim=1
            )
        else:
            self.local_wind_direction = self.base_direction.expand(self.num_envs, 3)


    def get_wind(self):
        if not self.variable_speed and not self.variable_direction:
            return self.base_speed * self.base_direction.expand(self.num_envs, 3)

        return self.wind_velocity_buffer.unsqueeze(-1) * self.local_wind_direction
