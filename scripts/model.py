# -*- coding: utf-8 -*-
import logging
import requests
import json
import random

def create_message_list(dialog_history, latest_question):
    messages_list = []
    messages = []
    
    for i in range(0, len(dialog_history), 2):
        messages.append({
            "role": "user",
            "content": dialog_history[i]
        })
        if i + 1 < len(dialog_history):
            messages.append({
                "role": "assistant",
                "content": dialog_history[i + 1]
            })
    
    messages.append({
        "role": "user",
        "content": latest_question
    })
    
    messages_list.append(messages)
    
    return messages_list

def llama3_8b_instruct_generate(dialog_history, latest_question):
    # User-defined model call
    pass

def llama3_70b_instruct_generate(dialog_history, latest_question):
    # User-defined model call
    pass

def qwen25_7b_instruct_generate(dialog_history, latest_question):
    # User-defined model call
    pass

def wizardlm_30b_generate(text):
    # User-defined model call
    pass

def gpt4o_generate(text, temp=1.0):
    # User-defined model call
    pass

def gpt4o_multiturn_generate(dialog_history, latest_question, temp=0.0):
    # User-defined model call
    pass

def claude_multiturn_generate(dialog_history, latest_question):
    # User-defined model call
    pass

def get_answer(target_model_name, history, query):
    if 'llama3_8b' in target_model_name:
        answer = llama3_8b_instruct_generate(history, query)
    elif 'llama3_70b' in target_model_name:
        answer = llama3_70b_instruct_generate(history, query)
    elif '4o' in target_model_name:
        answer = gpt4o_multiturn_generate(history, query)
    elif 'claude' in target_model_name:
        answer = claude_multiturn_generate(history, query)
    elif 'qwen' in target_model_name:
        answer = qwen25_7b_instruct_generate(history, query)
    return answer