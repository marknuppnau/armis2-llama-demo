# Run
### Start llama-server
From a Jupyter Notebook, Open JupyterLab from the top of the Notebook. Once in JupyterLab, select File -> New -> Terminal. Move to the llama.cpp directory and start llama-server
```
cd /home/<username>/llama.cpp
./build/bin/llama-server -m ./models/Llama-3.2-3B-Instruct-Q5_K_M.gguf --port 8080 --alias Llama-3.2-3B-Instruct-Q5_K_M
```
