# mlops-zoomcamp

This repo contains all solutions and notes to MLOps zoomcamp.

## Index

1. [Introduction](01-intro/)
2. [Experiment tracking and model management](02-tracking/)
3. [Workflow Orchestration](03-orchestration/)
4. [Model Deployment](04-deployment/)

## Environment setup (EC2)

Launch an EC2 instance.

Change permissions of ssh file.

```
chmod 400 <key-file-name>
```

if doesn't exist, create a config file inside `.ssh` folder.

```
touch config
```

Then, add a configuration to avoid typing the same command to connect to the instance. Configuration looks as follows:

```
Host mlops-zoomcamp
    HostName <public-ip>
    User <ec2-user (amazon linux) or ubuntu (ubuntu)>
    IdentityFile <identity file path>
    StrictHostKeyChecking no
```

Connect via ssh.

```
ssh mlops-zoomcamp
```

Download and install conda. Go to https://www.anaconda.com/products/distribution

```
wget https://repo.anaconda.com/archive/Anaconda3-2022.05-Linux-x86_64.sh
bash <name of file>
```

Clone repo:

```
git clone <https repo url>
```

Create and activate environment:

```
conda env create -f environment.yaml
conda activate mlops-zoomcamp
```

To interact with the repo inside the EC2 instance using vscode, `Remote - SSH` plugin can be used.

To interact with jupyter notebook:

- Configure security group.
- In vscode configure the port mapping.

## Environment setup (Local)

```
conda env create -f environment.yaml
conda activate mlops-zoomcamp
```
