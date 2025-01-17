import openai
import os
import csv
import time
import pandas as pd
import datetime
import json

client = openai.OpenAI(
    base_url="http://localhost:8080/v1",
    api_key = "no-key-required"
)

os.chdir(os.path.dirname(os.path.abspath(__file__)))

system_prompt = '''
    You are tasked with generating synthetic healthcare data that encompasses a patients documented stay from admission through discharge and output the requested data elements in a JSON object.
'''

user_prompt = '''
    Return a JSON object with the following elements:

    {
    "patient_id", // random 9 digit real number
    "patient_last", // Last name of the patient
    "patient_first", // First name of the patient
    "admitting_diagnosis", // A short description of the reason for surgery
    "procedures", // A short description of the procedures being performed
    "history_and_physical", // History and physical assessment
    "operative_note", // Operative note with the details of the surgery
    "discharge_note", // Discharge summary
    }
'''

# Function that returns the categories of the SQL content
def get_response(system_prompt, user_prompt):
    # Send a completion call to generate an answer
    response = client.chat.completions.create(
        model="Llama-3.2-3B-Instruct-Q6_K_L",
        temperature=0.2,
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
    #return response.choices[0].message.content
    return response

results = []
start_time = time.time()

for i in range(1, 10):
    #print(f"Row {i+1}/{len(df)+1}")
    try:
        response = get_response(system_prompt, user_prompt)
        #print(response)
        result = response.choices[0].message.content
        # Convert the JSON response to a dictionary
        response_dict = json.loads(result)
        #prompt_tokens = response.usage.prompt_tokens
        #completion_tokens = response.usage.completion_tokens
        #total_tokens = response.usage.total_tokens

        # append the results to the list
        results.append({
            'system_prompt': system_prompt,
            'user_prompt': user_prompt,
            'patient_id': response_dict['patient_id'],
            'patient_last': response_dict['patient_last'],
            'patient_first': response_dict['patient_first'],
            'admitting_diagnosis': response_dict['admitting_diagnosis'],
            'procedures': response_dict['procedures'],
            'history_and_physical': response_dict['history_and_physical'],
            'operative_note': response_dict['operative_note'],
            'discharge_note': response_dict['discharge_note']
            #'prompt_tokens': prompt_tokens,
            #'completion_tokens': completion_tokens,
            #'total_tokens': total_tokens
        })
    except Exception as e:
        print(f"Error occurred for row {i}, skipping the row.")
        print(f"Error message: {str(e)}")
        continue
        
end_time = time.time()
execution_time = end_time - start_time
execution_time_minutes = execution_time / 60
print(f"Execution time: {execution_time_minutes} minutes")
print('Job completed. Writing results to file.')

# Convert results to a DataFrame
results_df = pd.DataFrame(results)

# Generate timestamp
timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

# Append timestamp to the XLSX filename
filename = f"results_{timestamp}.xlsx"

# Write results to the XLSX file
results_df.to_excel(filename, header=True, index=False)
