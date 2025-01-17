cd models
wget https://huggingface.co/bartowski/Llama-3.2-3B-Instruct-GGUF/resolve/main/Llama-3.2-3B-Instruct-Q6_K_L.gguf?download=true –o Llama-3.2-3B-Instruct-Q6_K_L.gguf
cd ..

./build/bin/llama-server -m ./models/Llama-3.2-3B-Instruct-Q6_K_L.gguf --port 8080 --alias Llama-3.2-3B-Instruct-Q6_K_L
