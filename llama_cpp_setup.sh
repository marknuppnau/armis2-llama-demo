#!/bin/bash
git clone https://github.com/ggerganov/llama.cpp/
cd llama.cpp
cmake -B build -DGGML_CUDA=ON -DGGML_CUDA_F16=ON
cmake --build build --config Release --parallel $(nproc)
echo "llama.cpp is ready!"