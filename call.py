# General Imports
from openai import OpenAI
import instructor
import os

import json
import csv

from pydantic import ValidationError

import comperator
# My Modules
import validator
import connection

#region VARIABLES AND KEY
os.environ["OPENAI_API_KEY"] = open("API_keys/my_openai_key.txt", "r", encoding="utf-8").read()
print_output = False

# Report Id Handling (for error_log)
report_id = None
raw_output = None

# Model paramteres
openai_model="gpt-4-turbo-preview"         # gpt-4-turbo-preview   gpt-3.5-turbo-0125
seed=42
temperature=0
max_tokens=4095
top_p=1
frequency_penalty=0
presence_penalty=0

#Token Usage
completion_tokens_extract_pilot_info=0
prompt_tokens_extract_pilot_info=0
total_tokens_etract_pilot_info=0

completion_tokens_extract_equipment_info = 0
prompt_tokens_extract_equipment_info = 0
total_tokens_extract_equipment_info = 0

completion_tokens_extract_weather_info=0
prompt_tokens_extract_weather_info=0
total_tokens_extract_weather_info=0

completion_tokens_extract_event_info=0
prompt_tokens_extract_event_info=0
total_tokens_extract_event_info=0

completion_tokens_extract_malfunction_consequences_info=0
prompt_tokens_extract_malfunction_consequences_info=0
total_tokens_extract_malfunction_consequences_info=0

#endregion
########################################################################################################################

#region HELPER FUNCTIONS
def set_report_id(id):
    global report_id
    report_id = id
def get_report_id():
    return report_id

def get_raw_output():
    return raw_output

def save_log(raw_output, tokens, fingerprint):
    report_id = get_report_id()
    with open("Output/save_log.csv", "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([report_id, tokens, fingerprint, raw_output])

# Auto Eval
def llm_CALL_prompt_eng(taxonomy,instruction,report, report_id):
    global print_output
    print_output = True
    set_report_id(report_id)
    response = API_CALL_prompt_eng(taxonomy, instruction, report, report_id)
    return response

def llm_CALL_one_shot(prompt, report_id):
    global print_output
    print_output = True
    set_report_id(report_id)
    response = API_CALL_one_shot(prompt, report_id)
    return response

def llm_CALL_function_call(report, report_id, pydantic_model):
    global print_output
    print_output = True
    set_report_id(report_id)
    response = OPEN_AI_API_call_function(report, report_id, pydantic_model)
    return response

def save_token_usage(token_usage, name):
    global completion_tokens_extract_pilot_info, prompt_tokens_extract_pilot_info, total_tokens_etract_pilot_info
    global completion_tokens_extract_equipment_info, prompt_tokens_extract_equipment_info, total_tokens_extract_equipment_info
    global completion_tokens_extract_weather_info, prompt_tokens_extract_weather_info, total_tokens_extract_weather_info
    global completion_tokens_extract_event_info, prompt_tokens_extract_event_info, total_tokens_extract_event_info
    global completion_tokens_extract_malfunction_consequences_info, prompt_tokens_extract_malfunction_consequences_info, total_tokens_extract_malfunction_consequences_info

    if name == "Extract_pilot_info":
        completion_tokens_extract_pilot_info = token_usage.completion_tokens
        prompt_tokens_extract_pilot_info = token_usage.prompt_tokens
        total_tokens_etract_pilot_info = token_usage.total_tokens

    if name == "Extract_equipment_info":
        completion_tokens_extract_equipment_info = token_usage.completion_tokens
        prompt_tokens_extract_equipment_info = token_usage.prompt_tokens
        total_tokens_extract_equipment_info = token_usage.total_tokens

    if name == "Extract_weather_info":
        completion_tokens_extract_weather_info = token_usage.completion_tokens
        prompt_tokens_extract_weather_info = token_usage.prompt_tokens
        total_tokens_extract_weather_info = token_usage.total_tokens

    if name == "Extract_event_info":
        completion_tokens_extract_event_info = token_usage.completion_tokens
        prompt_tokens_extract_event_info = token_usage.prompt_tokens
        total_tokens_extract_event_info = token_usage.total_tokens

    if name == "Extract_malfunction_consequences_info":
        completion_tokens_extract_malfunction_consequences_info = token_usage.completion_tokens
        prompt_tokens_extract_malfunction_consequences_info = token_usage.prompt_tokens
        total_tokens_extract_malfunction_consequences_info = token_usage.total_tokens

    return


def get_token_usage():
    sum_completion_tokens = completion_tokens_extract_pilot_info + completion_tokens_extract_equipment_info + completion_tokens_extract_weather_info + completion_tokens_extract_event_info + completion_tokens_extract_malfunction_consequences_info
    sum_prompt_tokens = prompt_tokens_extract_pilot_info + prompt_tokens_extract_equipment_info + prompt_tokens_extract_weather_info + prompt_tokens_extract_event_info + prompt_tokens_extract_malfunction_consequences_info
    sum_total_tokens = total_tokens_etract_pilot_info + total_tokens_extract_equipment_info + total_tokens_extract_weather_info + total_tokens_extract_event_info + total_tokens_extract_malfunction_consequences_info

    return sum_completion_tokens, sum_prompt_tokens, sum_total_tokens

def get_model_parameters():
    return openai_model, seed, temperature, max_tokens, top_p

#endregion
########################################################################################################################

#region TESTING
def llm_analysis(report, report_id):
    instruction = ("You are a paraglider safety expert. "
                   "You want to classify accident reports according to a classification schema. "
                   "The classification schema holds attributes like (pilot_error, flight_type, etc.) and a list of possible values (e.g.[pilot, authority, other])"
                   "Follow these steps VERY carefully:"
                   "1. Choose all attributes that are directly or indirectly given in the accident report"
                   "2. Classify each attribute you have chosen with one value from the schema."
                   "3. Respond with your result in a JSON schema. "
                   "Here is the classification schema: \n")

    taxonomy = json.load(open("Taxonomy/JSON/taxonomy_annotated_list.json", "r", encoding="utf-8"))
    set_report_id(report_id)
    response = API_CALL_prompt_eng(taxonomy, instruction, report, report_id)
    return response

def llm_test1(report_id):
    taxonomy = json.load(open("Taxonomy/JSON/taxonomy.json", "r", encoding="utf-8"))
    instruction = ("Extract all information from the accident report."
                   "Respond in JSON Format given a predefined classification schema:\n")
    report = connection.get_accident_report_auto_eval(report_id)
    set_report_id(report_id)
    response = API_CALL_prompt_eng(taxonomy, instruction, report, report_id)
    return response

def llm_test2(report_id):
    instruction = ("You are a renowned paragliding safety expert. "
                   "You must search an accident report for information about the harness."
                   "You may only classify the information according to a predefined scheme. "
                   "Answer in JSON format. Use only the BEST fitting value in a category. "
                   "Only Output Categories, that are known: ")

    taxonomy = json.load(open("Taxonomy/JSON/taxonomy_categories/harness.json", "r", encoding="utf-8"))
    set_report_id(report_id)
    report = connection.get_accident_report_auto_eval(report_id)

    response = API_CALL_prompt_eng(taxonomy, instruction, report, report_id)




def llm_test3_function_calling(report, report_id):
    instruction = ("You are a paraglider safety expert. "
                   "You want to classify accident reports only with the provided function: extract_accident_info. "
                   "The function holds a classification schema."
                   "It holds attributes like (pilot_error, flight_type, etc.) and a list of possible values (e.g.[pilot, authority, other])"
                   "Follow these steps VERY carefully:"
                   "1. Choose all attributes that are directly or indirectly given in the accident report"
                   "2. Classify each attribute you have chosen with one value from the schema."
                   "3. Respond with your result in a JSON schema. ")

    taxonomy = json.load(open("Taxonomy/JSON/taxonomy_function_call_noType.json", "r", encoding="utf-8"))
    set_report_id(report_id)
    response = OPEN_AI_API_call_function(taxonomy, instruction, report, report_id)

    return response

#endregion
########################################################################################################################

#region API CALLS
# def API_CALL_prompt_eng(taxonomy, instruction, report, report_id):
#     global raw_output   # save the raw_output for log in auto_eval_preprocessing.py
#     # Initialize the validator (pydantic object)
#     reports = validator.reports
#     reports.report_id = report_id   # save in the validator (for error_log)
#
#     if print_output:
#         print("#################################### All Inputs befor the call: ########################################")
#         print(f"instruction: {instruction}{taxonomy}")
#         print(f"taxonomy: {taxonomy}")
#         print(f"report: {report}")
#         print(f"report_id: {report_id}")
#         print("######################################### End of Inputs :###############################################\n")
#         print(f"seed: {seed}, temperature: {temperature}, max_tokens: {max_tokens}, top_p: {top_p}, frequency_penalty: {frequency_penalty}, presence_penalty: {presence_penalty}\n")
#
#     # Create the client
#     client = instructor.patch(OpenAI())
#     # noinspection PyArgumentList
#     classified_report = client.chat.completions.create(
#         model=openai_model,
#         response_model=reports,
#         response_format={"type": "json_object"},
#         messages=[
#             {"role": "system",
#              "content": f"{instruction}{taxonomy}"
#              },
#             {
#                 "role": "user",
#                 "content": f"{report}"
#             }
#         ],
#         seed=seed,
#         temperature=temperature,
#         max_tokens=max_tokens,
#         top_p=top_p,
#         frequency_penalty=frequency_penalty,
#         presence_penalty=presence_penalty,
#         max_retries=1,
#     )
#     raw_output = classified_report      # save the raw_output for log in auto_eval_preprocessing.py
#
#     raw_response = raw_output.model_dump(exclude_unset=True)
#     token_usage = raw_output._raw_response.usage
#     completion_tokens = token_usage.completion_tokens
#     prompt_tokens = token_usage.prompt_tokens
#     total_tokens = token_usage.total_tokens
#     fingerprint = raw_output._raw_response.system_fingerprint
#     if print_output:
#         print("#################################### All Outputs after the call: ########################################\n")
#         print(f"Completion Tokens: {completion_tokens}, Prompt Tokens: {prompt_tokens}, Total Tokens: {total_tokens}")
#         print(f"Fingerprint: {classified_report._raw_response.system_fingerprint}")
#         print("Response with model.dump (exclude_unset=True):")
#         print(raw_response)
#
#     # Save relevant information in save_log.csv (report_id, tokens, fingerprint, raw_message)
#     save_log(raw_response, raw_output._raw_response.usage, raw_output._raw_response.system_fingerprint)
#
#     # Filter for relevant key value pairs; Exclude null, none, etc.
#     output_dict = {key: value for key, value in raw_response.items() if value not in ("null", None, "unknown", "<null>")}
#
#     if print_output:
#         print("Response filtered for (null, None, unknown, <null>):")
#         print(output_dict)
#
#     return output_dict


def API_CALL_prompt_eng(taxonomy, instruction, report, report_id):
    global raw_output   # save the raw_output for log in auto_eval_preprocessing.py
    # Initialize the validator (pydantic object)
    reports = validator.extract_accident_info_literals
    reports.report_id = report_id   # save in the validator (for error_log)

    if print_output:
        print("#################################### All Inputs befor the call: ########################################")
        print(f"instruction: {instruction}{taxonomy}")
        print(f"taxonomy: {taxonomy}")
        print(f"report: {report}")
        print(f"report_id: {report_id}")
        print("######################################### End of Inputs :###############################################\n")
        print(f"seed: {seed}, temperature: {temperature}, max_tokens: {max_tokens}, top_p: {top_p}, frequency_penalty: {frequency_penalty}, presence_penalty: {presence_penalty}\n")

    # Create the client
    client = instructor.patch(OpenAI())
    # noinspection PyArgumentList
    try:
        classified_report = client.chat.completions.create(
            model=openai_model,
            response_model=reports,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system",
                 "content": f"{instruction}{taxonomy}"
                 },
                {
                    "role": "user",
                    "content": f"{report}"
                }
            ],
            seed=seed,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            max_retries=1,
        )
        raw_output = classified_report      # save the raw_output for log in auto_eval_preprocessing.py

        raw_response = raw_output.model_dump(exclude_unset=True)
        token_usage = raw_output._raw_response.usage
        completion_tokens = token_usage.completion_tokens
        prompt_tokens = token_usage.prompt_tokens
        total_tokens = token_usage.total_tokens
        fingerprint = raw_output._raw_response.system_fingerprint
        if print_output:
            print("#################################### All Outputs after the call: ########################################\n")
            print(f"Completion Tokens: {completion_tokens}, Prompt Tokens: {prompt_tokens}, Total Tokens: {total_tokens}")
            print(f"Fingerprint: {classified_report._raw_response.system_fingerprint}")
            print("Response with model.dump (exclude_unset=True):")
            print(raw_response)

        # Save relevant information in save_log.csv (report_id, tokens, fingerprint, raw_message)
        save_log(raw_response, raw_output._raw_response.usage, raw_output._raw_response.system_fingerprint)

        # Filter for relevant key value pairs; Exclude null, none, etc.
        output_dict = {key: value for key, value in raw_response.items() if value not in ("null", None, "unknown", "<null>")}

        if print_output:
            print("Response filtered for (null, None, unknown, <null>):")
            print(output_dict)

    except ValidationError as e:
        print("Error: ", e)
        # Save relevant information in save_log.csv (report_id, tokens, fingerprint, raw_message)
        save_log(e, "Error", "Error")
        output_dict = None

    return output_dict


def API_CALL_one_shot(prompt, report_id):
    global raw_output   # save the raw_output for log in auto_eval_preprocessing.py
    # Initialize the validator (pydantic object)
    reports = validator.extract_accident_info_literals
    reports.report_id = report_id   # save in the validator (for error_log)

    if print_output:
        print("#################################### All Inputs befor the call: ########################################")
        print(f"prompt: {prompt}")
        print(f"report_id: {report_id}")
        print("######################################### End of Inputs :###############################################\n")
        print(f"seed: {seed}, temperature: {temperature}, max_tokens: {max_tokens}, top_p: {top_p}, frequency_penalty: {frequency_penalty}, presence_penalty: {presence_penalty}\n")

    # Create the client
    client = instructor.patch(OpenAI())
    # noinspection PyArgumentList
    try:
        classified_report = client.chat.completions.create(
            model=openai_model,
            response_model=reports,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system",
                 "content": f"{prompt}"
                 }
            ],
            seed=seed,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            max_retries=1,
        )
        raw_output = classified_report      # save the raw_output for log in auto_eval_preprocessing.py

        raw_response = raw_output.model_dump(exclude_unset=True)
        token_usage = raw_output._raw_response.usage
        completion_tokens = token_usage.completion_tokens
        prompt_tokens = token_usage.prompt_tokens
        total_tokens = token_usage.total_tokens
        fingerprint = raw_output._raw_response.system_fingerprint
        if print_output:
            print("#################################### All Outputs after the call: ########################################\n")
            print(f"Completion Tokens: {completion_tokens}, Prompt Tokens: {prompt_tokens}, Total Tokens: {total_tokens}")
            print(f"Fingerprint: {classified_report._raw_response.system_fingerprint}")
            print("Response with model.dump (exclude_unset=True):")
            print(raw_response)

        # Save relevant information in save_log.csv (report_id, tokens, fingerprint, raw_message)
        save_log(raw_response, raw_output._raw_response.usage, raw_output._raw_response.system_fingerprint)

        # Filter for relevant key value pairs; Exclude null, none, etc.
        output_dict = {key: value for key, value in raw_response.items() if value not in ("null", None, "unknown", "<null>")}

        if print_output:
            print("Response filtered for (null, None, unknown, <null>):")
            print(output_dict)

    except ValidationError as e:
        print("Error: ", e)
        # Save relevant information in save_log.csv (report_id, tokens, fingerprint, raw_message)
        save_log(e, "Error", "Error")
        output_dict = None

    return output_dict


def OPEN_AI_API_call_function(report, report_id, pydantic_model):
    global raw_output   # save the raw_output for log in auto_eval_preprocessing.py

    #reports = validator.reports_new
    reports = getattr(validator, pydantic_model)      # getattr because the model name is transferred as a string
    reports.report_id = report_id                       # save the report_id in the validator (for error_log)
    #TODO: reports.report_pydanctic_model einabuen und im save_log speichern

    if print_output:
        print("#################################### All Inputs befor the call: ########################################")
        print(f"pydantic_model: {pydantic_model}")
        print(f"report_id: {report_id}")
        print("######################################### End of Inputs :###############################################\n")
        print(f"seed: {seed}, temperature: {temperature}, max_tokens: {max_tokens}, top_p: {top_p}, frequency_penalty: {frequency_penalty}, presence_penalty: {presence_penalty}\n")

    # Create the client
    client = instructor.patch(OpenAI(), mode=instructor.Mode.FUNCTIONS)
    # noinspection PyArgumentList

    try:
        classified_report = client.chat.completions.create(
            model=openai_model,
            response_model=reports,
            messages=[
                {"role": "system",
                 "content": "Only extract values that are known!"
                 },
                {
                    "role": "user",
                    "content": f"{report}"
                }
            ],
            seed=seed,
            temperature=temperature,
            max_tokens=max_tokens,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            max_retries=2,
        )

        raw_output = classified_report      # save the raw_output for log in auto_eval_preprocessing.py

        raw_response = raw_output.model_dump(exclude_unset=True)
        token_usage = raw_output._raw_response.usage
        completion_tokens = token_usage.completion_tokens
        prompt_tokens = token_usage.prompt_tokens
        total_tokens = token_usage.total_tokens
        fingerprint = raw_output._raw_response.system_fingerprint

        json_llm_response = comperator.convert_dict_to_json(raw_response)

        if print_output:
            print("#################################### All Outputs after the call: ########################################\n")
            print(f"Completion Tokens: {completion_tokens}, Prompt Tokens: {prompt_tokens}, Total Tokens: {total_tokens}")
            print(f"Fingerprint: {fingerprint}")
            print("Response with model.dump (exclude_unset=True):")
            print(json_llm_response)

        # Save relevant information in save_log.csv (report_id, tokens, fingerprint, raw_message)
        save_log(json_llm_response, raw_output._raw_response.usage, raw_output._raw_response.system_fingerprint)

        # Save token usage
        save_token_usage(token_usage, pydantic_model)


        # Filter for relevant key value pairs; Exclude null, none, etc.
        output_dict = {key: value for key, value in raw_response.items() if value not in ("null", None, "unknown", "<null>")}

        output_dict = comperator.convert_dict_to_json(output_dict)
        output_dict = {key: value for key, value in output_dict.items() if value != 'unknown'}

        # if print_output:
        #     print("Response filtered for (null, None, unknown, <null>):")
        #     print(output_dict)

    except ValidationError as e:
        print("Error: ", e)
        # Save relevant information in save_log.csv (report_id, tokens, fingerprint, raw_message)
        save_log(e, "Error", "Error")
        output_dict = None

    return output_dict

#endregion
########################################################################################################################

if __name__ == '__main__':
    print_output = True

    llm_test1(18506)
    # #Test
    # accident_report = open("accident_reports/18506.txt", "r", encoding="utf-8").read()
    #
    # # simple accident report, complex taxonomy (complete take off taxonomy)
    # complex_taxonomy_analysis = llm_analysis(accident_report, 18506)


    #llm_test2(18506)
    # accident_report = connection.get_accident_report_auto_eval(18506)
    #
    #
    # llm_test3_function_calling(accident_report, 18506)
