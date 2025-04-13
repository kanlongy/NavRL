import torch

class WindModel:
    def __init__(self, device, num_envs, 
                 base_speed=1.0, 
                 base_direction=torch.tensor([1.0, 0.0, 0.0]), 
                 variable_speed=False, 
                 variable_direction=False,
                 fluid_density=1.225, 
                 drag_coefficient=0.8, 
                 cross_section_area=0.05):
        """
        base_speed: scalar, base wind speed
        base_direction: tensor of shape (3,), wind direction
        variable_speed: if True, wind speed will vary over time
        variable_direction: if True, wind direction will vary over time
        """
        self.device = device
        self.num_envs = num_envs
        self.base_speed = base_speed
        self.base_direction = base_direction.to(device).float()
        self.variable_speed = variable_speed
        self.variable_direction = variable_direction
        self.rho = fluid_density
        self.C_D = drag_coefficient
        self.area = cross_section_area
        self.t = 0.0
        self.freq = 0.2  # frequency of change
        self.noise_scale = 0.3

    def step(self, dt):
        self.t += dt

    def get_wind(self):
        if not self.variable_speed and not self.variable_direction:
            return self.base_speed * self.base_direction.expand(self.num_envs, 3)

        speed = self.base_speed
        direction = self.base_direction

        if self.variable_speed:
            speed = self.base_speed + self.noise_scale * torch.sin(self.freq * self.t)  # Sin change

        if self.variable_direction:
            angle = torch.tensor(self.freq * self.t, device=self.device)
            # rotating around Z-axis for 2D wind direction change
            rot_x = torch.cos(angle) * direction[0] - torch.sin(angle) * direction[1]
            rot_y = torch.sin(angle) * direction[0] + torch.cos(angle) * direction[1]
            direction = torch.stack([rot_x, rot_y, direction[2]])

        direction = direction / torch.norm(direction).clamp(min=1e-6)
        return speed * direction.expand(self.num_envs, 3)
