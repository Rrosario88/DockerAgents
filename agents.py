# agents.py


# import library
import os
import csv
import anthropic
from prompts import *
# Set up the Anthropic client
if not os.getenv("ANTHROPIC_API_KEY"):
    os.environ["ANTHROPIC_API_KEY"] = input("Please enter your anthropic API key: ")

# Create the client
client = anthropic.anthropic()
sonnet = "claude-3-5-sonnet-20240620"


# Function to read the CSV file from the user
def read_csv(file_path):
    data = []
    with open(file_path, "r", newline="") as csvfile: #open the csv file
        csv_reader = csv.reader(csvfile) #read the csv file
        for row in csv_reader: #Create a CSV reader object
            data.append(row) #add each row to the data
    return data

#Function to save the generated data to a new CSV file
def save_to_csv(data, output_file, headers=None):
    mode = "w" if headers else "a" #set the file mode: "w" (write) if headers are provided, "a" (append) otherwise
    with open(output_file, mode, newline="") as f: #open the output file
        writer = csv.writer(f) #create a CSV writer object
        if headers: #if headers are provided
            writer.writerow(headers) #write the headers to the csv file
        for row in csv.reader(data.splitlines()): #split the data into rows
            writer.writerow(row) #write the data to the csv file

# Create the analyzer Agent
def analyzer_agent(sample_data):
    message = client.messages.create(
        model=sonnet,
        max_tokens=400
        temperature=0.1,
        system=ANALYZER_SYSTEM_PROMPT # Use the predefined system prompt for the analyzer
        messages=[
            {
                "role: "user",
                "content": ANALYZER_USER_PROMPT.format(sample_data=sample_data)
                # format the user prompt with the provided sample data

            }

        ],
    )
    return message.content[0].text #Return the text content of the first message 

# Create the Generator Agent
def generator_agent (analysis_result, sample_data, num_rows=30):
    message = client.messages.create(
        model-sonnet,
        max_tokens=1500, # Allow for a longer response (1500 tokens)
        temperature=1，# Set a high temperature for more creative, diverse output
        system=GENERATOR_SYSTEM_PROMPT, 
        messages=[
            {
                "role": "user",
                "content": GENERATOR_USER_PROMPT.format(
                    num_rows=num_rows,
                    analysis_result=analysis_result,
                    sample_data sample_data
                )
                # Format the user prompt with the number of rows to generate,
                # the analysis result, and the sample data
            }
        ]
    )
    return message.content[0].text