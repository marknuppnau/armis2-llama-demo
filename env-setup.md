# Environment Setup

## JupyterLab (easy)
1. Navigate browser to <https://armis2.arc-ts.umich.edu/pun/sys/dashboard> (requires UMVPN or UMHSVPN)
2. Under **Interactive Apps**, choose JupyterLab
3. Populate the following fields:
   - Python distribution - **mamba/py3.10**
   - Slurm account - can be project specific or **precisionhealth_owned1** if eligible
   - Partition - **gpu** or **precisionhealth** if eligible
   - Number of hours - **6**
   - Number of cores - **40**
   - Memory (GB) - **40**
   - Number of GPUs - **1**
   - Module commands - **load gcc/10.3.0 cuda/11.8.0 cudnn/11.8-v8.7.0**
4. Click **Launch**

## VS Code (intermediate)
1. Navigate browser to <https://armis2.arc-ts.umich.edu/pun/sys/dashboard>
2. Login to ARMIS2 login node via shell access
3. Run the following commands:
    - mkdir llm-testing
    - cd llm-testing
    - nano llama_env_setup.sh
4. Paste script below (located in llama_env_setup.sh)
```
#!/bin/bash
module load python gcc cuda cudnn

# Create and source the virtual environment
python -m venv myenv
source myenv/bin/activate
```
5. Exit (ctrl+x), y
6. Run the command **chmod +x llama_env_setup.sh**
