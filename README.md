
# Big Data Energy

The required components were installed manually for the sake of the PoC.

## Installation
### Software requirements of the base environment:

 - sudo apt update && sudo apt upgrade -y
 - sudo apt install python3-pip
 - sudo apt install build-essential

**Anaconda**
 - wget https://repo.anaconda.com/archive/Anaconda3-2024.10-1-Linux-x86_64.sh
 - bash Anaconda3-2024.02-1-Linux-x86_64.sh

**Python vnenv**
 - sudo apt install python3-venv

**FFMPG**
 - sudo apt install ffmpeg

### Installation of components

#### MatAnyone
Commands required for installation:
 - git clone https://github.com/pq-yang/MatAnyone.git
 - cd MatAnyone/
 - python3 -m venv myenv
 - source myenv/bin/activate
 - pip install pip --upgrade
 - pip install setuptools wheel cython
 - pip install cchardet
 - pip install -e .
 - pip install -r hugging_face/requirements.txt

#### RollingDepth
Commands required for installation:
 - git clone https://github.com/prs-eth/RollingDepth.git
 - cd RollingDepth/ 
 - python3 -m venv myvenv
 - source myvenv/bin/activate  
 - pip install setuptools wheel cython
 - pip install -r requirements.txt
 - cd diffusers/
 - pip install -e ".[dev]"

#### Seamless
Commands required for installation:
 - mkdir seamless_huggingface
 - cd seamless_huggingface/
 - python3 -m venv myvenv 
 - source myvenv/bin/activate
 - pip install git+https://github.com/huggingface/transformers.git sentencepiece scipy protobuf
 - pip install torch torchaudio
 - wget https://raw.githubusercontent.com/sedthh/ByborgHackathon/refs/heads/main/seamless_workaround.py

#### OpenVoice
Commands required for installation:
 - conda create -n openvoice python=3.9
 - conda activate openvoice
 - git clone https://github.com/myshell-ai/OpenVoice.git
 - cd OpenVoice
 - pip install -e .
 - wget https://myshell-public-repo-host.s3.amazonaws.com/openvoice/checkpoints_1226.zip
 - unzip checkpoints_1226.zip
 - wget https://raw.githubusercontent.com/sedthh/ByborgHackathon/refs/heads/main/openvoice.py

#### TheoremExplainAgent
TheoremExplainAgent (TEA) is an innovative AI system designed to generate long-form explanatory videos for mathematical and scientific theorems using Manim animations. It employs a two-agent architecture: a planner agent that constructs structured narratives and a coding agent that translates them into Python animation scripts. To assess the quality of these AI-generated explanations, TheoremExplainBench (TEB) was introduced, covering 240 theorems across multiple STEM disciplines with five evaluation metrics. Results show that agentic planning significantly improves video coherence, with the o3-mini agent achieving a 93.8% success rate. However, minor layout issues persist in the generated videos. Notably, multimodal explanations help uncover deeper reasoning flaws that text-based methods often miss, emphasizing the importance of integrating visual elements in theorem explanations.
This is a very new model that currently relies on paid services. There will likely be a free version available in the future. 
Source: https://tiger-ai-lab.github.io/TheoremExplainAgent/


## Pipeline

In its current state, the procedure can be fully executed by running the `start_process.sh` bash script.

## Further development possibilities
### Orchestration
A central control layer is needed, which would be the orchestration. This receives the input content and initiates the subprocesses.

### Scalability
The pipeline consists of process components, each of which can be placed in separate Docker containers. Some of these containers handle tasks that can be parallelized, while others cannot. To manage this efficiently, an orchestration layer is essential. This backend software coordinates process execution, synchronizes results, and ultimately generates the final video feed.

### AI-based educational material enhancement based on feedback
Create a review test from the learning material to check if you have understood everything. Based on this, it can either review or elaborate on certain topics.
