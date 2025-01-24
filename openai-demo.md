# Run
### Start llama-server
From a Jupyter Notebook, Open JupyterLab from the top of the Notebook. Once in JupyterLab, select File -> New -> Terminal. Move to the llama.cpp directory and start llama-server
```
cd /home/<username>/llama.cpp
./build/bin/llama-server -m ./models/Llama-3.2-3B-Instruct-Q5_K_M.gguf --port 8080 --alias Llama-3.2-3B-Instruct-Q5_K_M
```
### Import all relevant packages
```
import openai
import os
import csv
import time
import pandas as pd
from datetime import datetime
import json
import pyarrow as pa
import pyarrow.parquet as pq
```
### Setup client
```
client = openai.OpenAI(
    base_url="http://localhost:8080/v1",
    api_key = "no-key-required"
)

# Read the CSV file
synthetic_df = pd.read_csv('notes/synthetic.csv')
output_dir = 'notes'

# Ensure output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
```
### Create system prompt
```
system_prompt = '''
    You are tasked with creating structured data elements from unstructured 
    clinical notes. Return a JSON object with the following keys: 
    "age", "diagnosis", "summary".
'''
```
### Define get_response
```
# Function that accepts a user prompt and returns a response
def get_response(user_prompt):
    # Send a completion call to generate an answer
    response = client.chat.completions.create(
        model="model",
        temperature=0.5,
        # This is to enable JSON mode, making sure responses are valid json objects
        response_format={ 
            "type": "json_object"
        },
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    )
    
    # Return the generated response
    return response
```
### Iterate through synthetic notes
```
results = []
start_time = time.time()

for i, row in synthetic_df[:10].iterrows():
    print(f"Row {i+1}/{len(synthetic_df)+1}")
    try:
        response = get_response(row['note'])
        #print(response)
        result = response.choices[0].message.content
        # Convert the JSON response to a dictionary
        response_dict = json.loads(result)
        prompt_tokens = response.usage.prompt_tokens
        completion_tokens = response.usage.completion_tokens
        total_tokens = response.usage.total_tokens

        # append the results to the list
        results.append({
            'system_prompt': system_prompt,
            'note': row['note'],
            'age': response_dict['age'],
            'diagnosis': response_dict['diagnosis'],
            'summary': response_dict['summary'],
            'prompt_tokens': prompt_tokens,
            'completion_tokens': completion_tokens,
            'total_tokens': total_tokens
        })
    except Exception as e:
        print(f"Error occurred for row {i+1}, skipping the row.")
        print(f"Error message: {str(e)}")
        continue
        
end_time = time.time()
execution_time = end_time - start_time
execution_time_minutes = execution_time / 60
print(f"Execution time: {execution_time_minutes} minutes")
print('Job completed. Writing results to file.')
```
### Convert to dataframe and save as parquet
```
# Convert results to a DataFrame
results_df = pd.DataFrame(results)

# Designate data types
results_df['age'] = pd.to_numeric(results_df['age'], errors='coerce')
results_df['diagnosis'] = results_df['diagnosis'].astype(str)
results_df['summary'] = results_df['summary'].astype(str)

print(results_df.head())

# Generate the output file path with a timestamp
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
filename = f"results_{timestamp}.parquet"
output_path = os.path.join(output_dir, filename)

# Convert DataFrame to Parquet file
results_df.to_parquet(output_path, engine='pyarrow')
```
