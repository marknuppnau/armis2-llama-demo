import openai
import os
import csv

client = openai.OpenAI(
    base_url="http://localhost:8080/v1",
    api_key = "no-key-required"
)

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Create a CSV file to store the results
csv_file_name = "notes.csv"

# Open the CSV file in write mode
with open(csv_file_name, mode='w', newline='') as csvfile:

    # Create a CSV writer object
    csv_writer = csv.writer(csvfile)

    # Write the header to the CSV file (customize as per the actual data structure)
    csv_writer.writerow(['id', 'note'])  # Example headers, replace with actual headers
    
    for i in range(1, 10):
        # Make a GET request to the API
        response = client.chat.completions.create(
            model="Llama-3.2-3B-Instruct-Q6_K_L",
            # This is to enable JSON mode, making sure responses are valid json objects
            #response_format={ 
            #    "type": "json_object"
            #},
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Write a synthetic clinical note that does not exceed 200 words."}
            ]
            )

        #print(response.choices[0].message.content)
        data = response.choices[0].message.content
        csv_writer.writerow([i, data])
        

print(f"Data has been successfully written to {csv_file_name}")