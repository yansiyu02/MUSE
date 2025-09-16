import json
import re
import argparse
from jinja2 import Template

# Define the template
template = """You are provided with a dialogue history that revolves around a potentially sensitive question "{malicious_question}". Your task is to identify the potential risks associated with the question and to formulate a safer response to the last turn of the dialogue history. This should be done to prevent the model from being prompted to address the sensitive question.

Dialogue History: {conversation_history}

Please craft a safer response that underscores the importance of safety in relation to {latest_question} to avoid prompting the model to answer the sensitive question. Output in JSON format, like this: ```\n{{"key_point": "...","answer": "..."}}\n```.
"""

def llama3_8b_instruct_generate(dialog_history, latest_question):
    # User-defined model call
    pass

# Function to process each line in the JSONL file
def process_line(line):
    data = json.loads(line)
    
    # Extract necessary fields
    malicious_question = data["target"]
    conversation_history = "\n".join(data["history"])
    latest_question = data["history"][-2]
    
    # Fill the template
    filled_template = template.format(
        malicious_question=malicious_question,
        conversation_history=conversation_history,
        latest_question=latest_question
    )
    
    return filled_template

# Extract JSON from the response text using regex
def extract_json_from_response(response_text):
    match = re.search(r'```\n({.*?})\n```', response_text, re.DOTALL)
    if match:
        json_str = match.group(1)
        return json.loads(json_str)
    return None

def process_and_merge_files(input_file_path, output_file_path):
    # First process the input file and store results in a list
    intermediate_data = []

    try:
        with open(input_file_path, 'r', encoding='utf-8') as infile:
            for line in infile:
                try:
                    record = json.loads(line.strip())
                    q = record['Q']
                    n = record['N']
                    level = record['level']
                    if level > 0 and n > 1 and q/n > 0.5:
                        intermediate_data.append(record)
                except KeyError as e:
                    print(f"KeyError: {e} in record: {record}")
                except json.JSONDecodeError as e:
                    print(f"JSONDecodeError: {e} in line: {line}")
    except FileNotFoundError:
        print(f"File not found: {input_file_path}")
        return

    # Then process the intermediate data and write to the final output file
    combined_results = []
    for record in intermediate_data:
        line = json.dumps(record)
        result = process_line(line)
        answer = None
        attempts = 0
        max_attempts = 20  # Maximum number of attempts to generate a valid response

        while answer is None and attempts < max_attempts:
            response_text = llama3_8b_instruct_generate(result)
            print(response_text)
            attempts += 1
            try:
                extracted_json = extract_json_from_response(response_text)           
                answer = extracted_json["answer"]
                break
            except:
                pass

        # Combine input line and result
        combined_result = {**record, "result": answer if answer else 'fail'}
        combined_results.append(combined_result)

    # Write combined results to the final output file
    with open(output_file_path, 'w', encoding='utf-8') as outfile:
        for result in combined_results:
            outfile.write(json.dumps(result) + '\n')

def main():
    parser = argparse.ArgumentParser(description="Process and merge JSONL files.")
    parser.add_argument('--input', type=str, required=True, help='Path to the input JSONL file.')
    parser.add_argument('--output', type=str, required=True, help='Path to the output JSONL file.')
    args = parser.parse_args()

    process_and_merge_files(args.input, args.output)

if __name__ == "__main__":
    main()