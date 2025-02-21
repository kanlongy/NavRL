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

Train with 1024 robots with 350 static obstacles and 80 dynamic obstacles 
```
cd isaac-training/training/script
python train.py headless=True env.num_envs=1024 env.num_obstacles=350 \
env_dyn.num_obstacles=80 wandb.mode=online

```

