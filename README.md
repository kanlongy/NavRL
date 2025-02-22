# NavRL


## Installation
```
git clone https://github.com/Zhefan-Xu/NavRL

echo 'export ISAACSIM_PATH="path/to/isaac_sim"' >> ~/.bashrc

cd isaac-training
bash setup.sh
```

## Run Example

```
conda activate NavRL

cd isaac-training/training/script
python train.py
```

![isaac-training-window](https://github.com/user-attachments/assets/14a4d8a8-e607-434f-af9d-42d0d945e8d7)



Train with 1024 robots with 350 static obstacles and 80 dynamic obstacles 
```
cd isaac-training/training/script
python train.py headless=True env.num_envs=1024 env.num_obstacles=350 \
env_dyn.num_obstacles=80 wandb.mode=online

```

https://github.com/user-attachments/assets/2294bd94-69b3-4ce8-8e91-0118cfae9bcd















