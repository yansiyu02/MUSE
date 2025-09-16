import os
import json
import random
import argparse

def extract_successful_entries(input_file_path, output_file_path):
    # Open the output file for writing
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        # Read all lines from the input file once
        with open(input_file_path, 'r', encoding='utf-8') as input_file:
            lines = input_file.readlines()
        
        # Process each line
        for line in lines:
            try:
                entry = json.loads(line.strip())
                if entry.get('result') != 'success':
                    continue
                
                target_question = entry.get('target_question')
                if not target_question:
                    continue

                fail_answers = []
                # Find fail entries for the same target_question
                for search_line in lines:
                    try:
                        search_entry = json.loads(search_line.strip())
                        if (search_entry.get('score') > 8.0 and 
                            search_entry.get('target_question') == target_question):
                            fail_answers.append(search_entry['attack_answer'])
                    except json.JSONDecodeError:
                        continue
                
                # Randomly select a 'fail' entry's chosen_answer if available
                entry['chosen_answer'] = random.choice(fail_answers) if fail_answers else "I'm sorry, but I cannot assist with it."
                
                # Write the successful entry with the chosen answer to the output file
                output_file.write(json.dumps(entry, ensure_ascii=False) + '\n')
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from file {input_file_path}: {e}")

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Extract successful entries from a JSONL file.')
    parser.add_argument('input_file_path', type=str, help='Path to the input JSONL file.')
    parser.add_argument('output_file_path', type=str, help='Path to the output JSONL file.')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Call the function with parsed arguments
    extract_successful_entries(args.input_file_path, args.output_file_path)

if __name__ == '__main__':
    main()