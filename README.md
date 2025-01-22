# Running local LLMs on the ARMIS2 HPC Cluster
This repository contains the documentation and code used in the generative AI tutorial, "Best Practices for Using local Large Language Models with the UM High-Performance Computing Cluster".

# Prerequisites
* Access to an ARMIS2 Slurm account (for billing purposes)
    * UM Research Computing Package (UMRCP)
    * Precision Health membership
* Some experience with Python and Shell (command line interface)

# Environment setup
* Follow the instructions in [environment setup](env-setup.md)

# Run
Either start from scratch and follow the steps below (GPU access required) or use the [llama-cpp notebook](llama-cpp.ipynb)

# Install packages
After completing the environment setup, run each of the commands below in your environment\
**Shell**
```
CMAKE_ARGS="-DGGML_CUDA=on" pip install llama-cpp-python
pip install openai langchain langchain-community
```
**Jupyter Notebook**
```
!CMAKE_ARGS="-DGGML_CUDA=on" pip install llama-cpp-python
!pip install openai langchain langchain-community
```

# Build llama.cpp framework
Clone the llama.cpp repository and build (or run [llama_cpp_setup.sh](llama_cpp_setup.sh))\
**Shell**
```
git clone https://github.com/ggerganov/llama.cpp/
cd llama.cpp
cmake -B build -DGGML_CUDA=ON -DGGML_CUDA_F16=ON
cmake --build build --config Release --parallel $(nproc)
```
**Jupyter Notebook**
```
!git clone https://github.com/ggerganov/llama.cpp/
%cd llama.cpp
!cmake -B build -DGGML_CUDA=ON -DGGML_CUDA_F16=ON
!cmake --build build --config Release --parallel $(nproc)
```
Replace $(nproc) with the number of cores selected in the environment setup to run jobs in parallel

# Download and test Llama 3.2 3B Instruct
Move to the models directory and download the Llama 3.2 3B model\
**Shell**
```
cd models
wget https://huggingface.co/MaziyarPanahi/Llama-3.2-3B-Instruct-GGUF/resolve/main/Llama-3.2-3B-Instruct.Q5_K_M.gguf?download=true -q -O Llama-3.2-3B-Instruct-Q5_K_M.gguf --show-progress
cd ..
./build/bin/llama-cli -m models/Llama-3.2-3B-Instruct-Q5_K_M.gguf --n_gpu_layers 1500 -no-cnv -p "Please create a three-paragraph synthetic clinical note for a patient who presents with sepsis.
```
**Jupyter Notebook**
```
%cd models
!wget https://huggingface.co/MaziyarPanahi/Llama-3.2-3B-Instruct-GGUF/resolve/main/Llama-3.2-3B-Instruct.Q5_K_M.gguf?download=true -q -O Llama-3.2-3B-Instruct-Q5_K_M.gguf --show-progress
%cd ..
!./build/bin/llama-cli -m models/Llama-3.2-3B-Instruct-Q5_K_M.gguf --n_gpu_layers 1500 -no-cnv -p "Please create a three-paragraph synthetic clinical note for a patient who presents with sepsis.
```

# Download synthetic notes to use with the demonstrations below
**Shell**
```
mkdir notes
cd notes
wget https://huggingface.co/datasets/starmpcc/Asclepius-Synthetic-Clinical-Notes/resolve/main/synthetic.csv?download=true
mv 'synthetic.csv?download=true' synthetic.csv
cd ..
```
**Jupyter Notebook**
```
%mkdir notes
%cd notes
!wget https://huggingface.co/datasets/starmpcc/Asclepius-Synthetic-Clinical-Notes/resolve/main/synthetic.csv?download=true
%mv 'synthetic.csv?download=true' synthetic.csv
%cd ..
```
# Demo1: OpenAI API Framework

# Demo2: Langchain Framework
* Follow the instructions in [langchain demo](langchain-demo.md)

