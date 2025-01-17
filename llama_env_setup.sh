#!/bin/bash
module load python gcc cuda cudnn

# Create and source the virtual environment
python -m venv myenv
source myenv/bin/activate
