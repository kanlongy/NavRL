# RLDrones
The official documentation [webpage](https://omnidrones.readthedocs.io/en/latest/installation.html) and [github](https://github.com/btx0424/OmniDrones) for OmniDrones.

## Installation
```
git clone --recursive https://github.com/Zhefan-Xu/RLDrones
```

a. Install [Isaac Sim](https://docs.omniverse.nvidia.com/isaacsim/latest/installation/install_workstation.html) ```2023.1.0-hotfix.1```. The version is important.

b. Set the environment variable to ```~/.bashrc```
```
# Isaac Sim root directory
export ISAACSIM_PATH="${HOME}/.local/share/ov/pkg/isaac_sim-*"
```

c. This project needs virtual environment, so install miniconda
```
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
~/miniconda3/bin/conda init bash
```

d. Create virtual environment and verify:
```
conda create -n sim python=3.10
conda activate sim

# at OmniDrones/
cp -r conda_setup/etc $CONDA_PREFIX
# re-activate the environment
conda activate sim

# verification
python -c "from omni.isaac.kit import SimulationApp"
# which torch is being used
python -c "import torch; print(torch.__path__)"
```

e. Install [orbit]([https://github.com/Zhefan-Xu/warp.git](https://github.com/Zhefan-Xu/orbit?tab=readme-ov-file))
```
cd orbit
ln -s ${ISAACSIM_PATH} _isaac_sim
./orbit.sh --conda sim
conda activate sim
sudo apt install cmake build-essential
./orbit.sh --install  # or "./orbit.sh -i"
./orbit.sh --extra  # or "./orbit.sh -e"
```

f. Install [TensorDict](https://github.com/Zhefan-Xu/tensordict) and [TorchRL](https://github.com/Zhefan-Xu/rl)
```
# TensorDict
cd tensordict
pip install tomli # if No module named 'tomli'
python setup.py develop

# TorchRL
cd rl
python setup.py develop
```

g. Install OmniDrones:
```
cd OmniDrones
pip install -e .
```

f. Intall Warp:
```
python build_lib.py
pip install -e .
```
## Run Example

```
cd navigation/script
python train.py
```

## Ignore
```
python train_lidar.py headless=false eval_interval=200 task=Forest task.lidar_range=4. task.lidar_vfov=[-10.,20.] wandb.entity=zhefanx
```

if import ```tensordict``` gives error, it might be due to tensordict is not the one we built (but from pip). Not sure why, but at this point, just pip uninstall tensordict.

if forgot localhost account, create one and use ```admin``` as both account and password as [here](https://forums.developer.nvidia.com/t/cannot-log-into-localhost-nucleus-wrong-credentials-or-the-user-does-not-exist/272431/2)
