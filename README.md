# Running local LLMs on the ARMIS2 HPC Cluster
This repository contains the documentation and code used in the generative AI tutorial, "Best Practices for Using local Large Language Models with the UM High-Performance Computing Cluster".

# Prerequisites
* Access to an ARMIS2 Slurm account (for billing purposes)
    * UM Research Computing Package (UMRCP)
    * Precision Health membership
* Some experience with Python and Shell (command line interface)

# Environment Setup
* Follow the instructions in [environment setup](env-setup.md)

# Build llama.cpp framework (Shell)
* After completing the environment setup, run each of the commands below in your environment (or run [llama_cpp_setup.sh](llama_cpp_setup.sh))
```
git clone https://github.com/ggerganov/llama.cpp/
cd llama.cpp
cmake -B build -DGGML_CUDA=ON -DGGML_CUDA_F16=ON
cmake --build build --config Release --parallel $(nproc)
```
Replace $(nproc) with the number of cores selected in the environment setup to run jobs in parallel

# Download and Test Llama 3.2B Instruct

# Demo1: OpenAI API Framework

# Demo2: Langchain Framework
