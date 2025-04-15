import torch
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

num_steps = 1000
alpha = 0.6
alpha_dir = 0.8  #alpha决定变化平滑程度
base_speed = 3
std = 2  #决定高斯采样范围
min_speed = 0.0
max_speed = 10  #截断范围10～15 （也可计算出无人机最大推力）

wind_speed = torch.full((1,), base_speed)
wind_direction = torch.nn.functional.normalize(torch.randn(3), dim=0) 
speed_history = []
direction_history = []

for t in range(num_steps):

    new_speed = torch.normal(mean=base_speed, std=std, size=(1,))
    new_speed = torch.clamp(new_speed, min=min_speed, max=max_speed)
    wind_speed = alpha * wind_speed + (1 - alpha) * new_speed

    new_direction = torch.randn(3)
    new_direction = torch.nn.functional.normalize(new_direction, dim=0)
    wind_direction = alpha_dir * wind_direction + (1 - alpha_dir) * new_direction
    wind_direction = wind_direction / wind_direction.norm()

    speed_history.append(wind_speed.item())
    direction_history.append((wind_direction * wind_speed).tolist())

direction_history = torch.tensor(direction_history)
x, y, z = direction_history[:, 0], direction_history[:, 1], direction_history[:, 2]

plt.figure(figsize=(10, 4))
plt.plot(speed_history, label='Wind Speed (m/s)', color='green')
plt.axhline(y=base_speed, color='gray', linestyle='--', label='Base Speed')
plt.axhline(y=max_speed, color='red', linestyle='--', label='Max = 3.0')
plt.axhline(y=min_speed, color='blue', linestyle='--', label='Min = 0.0')
plt.xlabel('Time Step')
plt.ylabel('Speed (m/s)')
plt.title('Wind Speed Magnitude Over Time')
plt.legend()
plt.grid(True)
plt.tight_layout()

fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(111, projection='3d')
ax.quiver(
    [0]*len(x), [0]*len(y), [0]*len(z),
    x, y, z,
    length=1.0, normalize=True, color='blue', linewidth=0.5
)
ax.set_xlim([-1, 1])
ax.set_ylim([-1, 1])
ax.set_zlim([-1, 1])
ax.set_title("Wind Direction Vectors (Full Sphere)")
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.tight_layout()

plt.show()
