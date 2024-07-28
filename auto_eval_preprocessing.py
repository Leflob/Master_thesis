# General Imports
import json
import csv
import datetime

# Batching
import asyncio

# My Modules
import comperator
import call
import connection
import validator

#region VARIABLES
print_output = False



#endregion
########################################################################################################################

#region HELPER FUNCTIONS

def new_run(name):
    if name == "function_calling_multi":
        col_desc_eval = ["report_id", "timestamp", "completion_tokens", "prompt_tokens", "total_tokens", "fingerprint",
                         "count_database", "count_llm", "count_changed", "count_added",
                         "changedData", "addedData",
                         "weather_bool", "injuries_bool",
                         "ground_truth", "cleaned_llm_response", "raw_user_input", "model_used", "temp", "top_p", "seed"]

        with open(f'Output/AutoEval/{name}.csv', 'w', newline="") as eval:
            writer = csv.writer(eval)
            writer.writerow(col_desc_eval)
    else:
        col_desc_eval = ["report_id", "timestamp", "completion_tokens", "prompt_tokens", "total_tokens", "fingerprint",
                         "count_database", "count_llm", "count_changed","count_added",
                         "changedData", "addedData",
                         "weather_bool", "injuries_bool",
                         "ground_truth", "cleaned_llm_response", "raw_user_input", "model_used", "temp", "top_p", "seed", "raw_llm_response"]

        with open(f'Output/AutoEval/{name}.csv', 'w',newline="") as eval:
            writer = csv.writer(eval)
            writer.writerow(col_desc_eval)

def save_data_csv(name, report_id, llm_json_response, changedData, addedData):
    #Model Parameters
    model_used, seed, temperature, max_tokens, top_p = call.get_model_parameters()
    # Database
    json_database = connection.get_json_database_auto_eval(report_id)
    # Details about USER-INPUT
    user_input, weather_info_bool, injured_body_parts_info_bool = connection.get_suppl_info()

    ground_truth = connection.get_ground_truth_auto_eval(report_id)
    count_json_database = comperator.count_attributes(ground_truth)

    if changedData is None:
        current_time = datetime.datetime.now()
        with open(f"Output/AutoEval/{name}.csv", "a", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([report_id, current_time.strftime("%Y-%m-%d %H:%M:%S"),
                             0, 0, 0, "Validation Error",
                             count_json_database, 0, 0, 0, 0, 0,
                             weather_info_bool, injured_body_parts_info_bool,
                             connection.get_ground_truth_auto_eval(report_id), llm_json_response, user_input, model_used, temperature, top_p, seed])
        return
    # JSON COUNTS
    count_json_llm = comperator.count_attributes(llm_json_response)
    count_changed = len(changedData.index)
    count_added = len(addedData.index)

    changedData, addedData = comperator.dataframes_to_json_changes(changedData, addedData)

    current_time = datetime.datetime.now()

    if name == "function_calling_multi":
        # RAW OUTPUT + TOKENS
        completion_tokens, prompt_tokens, total_tokens = call.get_token_usage()
        last_output = call.get_raw_output()
        fingerprint = last_output._raw_response.system_fingerprint
        with open(f"Output/AutoEval/{name}.csv", "a", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([report_id, current_time.strftime("%Y-%m-%d %H:%M:%S"),
                             completion_tokens, prompt_tokens, total_tokens, fingerprint,
                             count_json_database, count_json_llm, count_changed, count_added,
                             changedData, addedData,
                             weather_info_bool, injured_body_parts_info_bool,
                             ground_truth, llm_json_response, user_input, model_used, temperature, top_p, seed])
    else:
        # RAW OUTPUT + TOKENS
        raw_output = call.get_raw_output()
        raw_response = raw_output.model_dump(exclude_unset=True)
        token_usage = raw_output._raw_response.usage
        completion_tokens = token_usage.completion_tokens
        prompt_tokens = token_usage.prompt_tokens
        total_tokens = token_usage.total_tokens
        fingerprint = raw_output._raw_response.system_fingerprint
        with open(f"Output/AutoEval/{name}.csv", "a", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([report_id, current_time.strftime("%Y-%m-%d %H:%M:%S"),
                             completion_tokens, prompt_tokens, total_tokens, fingerprint,
                             count_json_database, count_json_llm, count_changed, count_added,
                             changedData, addedData,
                             weather_info_bool, injured_body_parts_info_bool,
                             ground_truth, llm_json_response, user_input, model_used, temperature, top_p, seed, raw_response])


def construct_report(report_id):
    return connection.get_accident_report_auto_eval(report_id)

#endregion
########################################################################################################################

#region MAIN FUNCTIONS

#region Prompt Engineering

#region prompt_engineering_baseline
def prompt_engineering_baseline(report_id, name):
    instruction = ("Extract all information from the accident report."
                   "Respond in JSON Format given a predefined classification schema:\n")

    taxonomy = json.load(open("Taxonomy/JSON/taxonomy.json", "r", encoding="utf-8"))
    report = connection.get_accident_report_auto_eval(report_id)
    json_llm = call.llm_CALL_prompt_eng(taxonomy, instruction, report, report_id)
    if json_llm is None:
        print("Error in LLM-Vaidation")
        save_data_csv(name, report_id, json_llm, None, "Validation Error")
        return

    if print_output:
        print("###### Additional Infos given ######")
        user_input, weather_info_bool, injured_body_parts_info_bool = connection.get_suppl_info()
        print(f"weather_further_information: {weather_info_bool}\ninjured_body_parts_sup_info_pilot: {injured_body_parts_info_bool}")
        print("###### Ground Truth ######")
        print(connection.get_ground_truth_auto_eval(report_id))
        print("###### json llm ######")
        print(json_llm)

    # 2. JSON Comperator
    changedData, addedData = comperator.compare_json_auto_eval(report_id, json_llm)

    # 3. Save Data
    save_data_csv(name, report_id, json_llm, changedData, addedData)

#endregion

#region prompt_engineering_simple
def prompt_engineering_simple(report_id, name):
    instruction = ("You are a renowned paragliding safety expert. "
                   "You must search an accident report for information about the harness."  
                   "You may only classify the information according to a predefined scheme. "
                   "Answer in JSON format."
                   "Only Output Categories, that are known: ")

    taxonomy = json.load(open("Taxonomy/JSON/taxonomy_annotated_list.json", "r", encoding="utf-8"))
    report = connection.get_accident_report_auto_eval(report_id)
    json_llm = call.llm_CALL_prompt_eng(taxonomy, instruction, report, report_id)
    if json_llm is None:
        print("Error in LLM-Vaidation")
        save_data_csv(name, report_id, json_llm, None, "Validation Error")
        return

    if print_output:
        print("###### Additional Infos given ######")
        user_input, weather_info_bool, injured_body_parts_info_bool = connection.get_suppl_info()
        print(f"weather_further_information: {weather_info_bool}\ninjured_body_parts_sup_info_pilot: {injured_body_parts_info_bool}")
        print("###### Ground Truth ######")
        print(connection.get_ground_truth_auto_eval(report_id))
        print("###### json llm ######")
        print(json_llm)

    # 2. JSON Comperator
    changedData, addedData = comperator.compare_json_auto_eval(report_id, json_llm)

    # 3. Save Data
    save_data_csv(name, report_id, json_llm, changedData, addedData)

#endregion

#region prompt_engineering_advanced
def prompt_engineering_advanced(report_id, name):
    instruction = ("You are a paraglider safety expert. "
                   "You want to classify accident reports according to a classification schema. "
                   "The classification schema holds attributes like (pilot_error, flight_type, etc.) and a list of possible values (e.g.[pilot, authority, other])"
                   "Follow these steps VERY carefully:"
                   "1. Choose all attributes that are directly or indirectly given in the accident report"
                   "2. Classify each attribute you have chosen with one value from the schema."
                   "3. Respond with your result in a JSON schema. "
                   "Here is the classification schema: \n")

    taxonomy = json.load(open("Taxonomy/JSON/taxonomy_annotated_list.json", "r", encoding="utf-8"))
    report = connection.get_accident_report_auto_eval(report_id)
    json_llm = call.llm_CALL_prompt_eng(taxonomy, instruction, report, report_id)

    if json_llm is None:
        print("Error in LLM-Vaidation")
        save_data_csv(name, report_id, json_llm, None, "Validation Error")
        return

    if print_output:
        print("###### Additional Infos given ######")
        user_input, weather_info_bool, injured_body_parts_info_bool = connection.get_suppl_info()
        print(
            f"weather_further_information: {weather_info_bool}\ninjured_body_parts_sup_info_pilot: {injured_body_parts_info_bool}")
        print("###### Ground Truth ######")
        print(connection.get_ground_truth_auto_eval(report_id))
        print("###### json llm ######")
        print(json_llm)

    # 2. JSON Comperator
    changedData, addedData = comperator.compare_json_auto_eval(report_id, json_llm)

    # 3. Save Data
    save_data_csv(name, report_id, json_llm, changedData, addedData)

#endregion

#region prompt_engineering_one_shot
def prompt_engineering_one_shot(report_id, name):
    taxonomy = json.load(open("Taxonomy/JSON/taxonomy_annotated_list.json", "r", encoding="utf-8"))
    report = connection.get_accident_report_auto_eval(report_id)
    instruction = ("You are a paraglider safety expert. "
                   "You want to classify accident reports according to a classification schema. "
                   "The classification schema holds attributes like (pilot_error, flight_type, etc.) and a list of possible values (e.g.[pilot, authority, other])"
                   "Think step by step:"
                   "1. Choose all attributes that are directly or indirectly given in the accident report"
                   "2. Classify each attribute you have chosen with one value from the schema."
                   "3. Respond with your result in a JSON schema. "
                    "Here is the classification schema: \n"
                   f"{taxonomy}"

                   
                   "\n#### Example:\n"
                   "#### accident report: \n"
                   "Am 28.04.2022 startete ich gegen 11.45 Uhr am Westhang der Wasserkuppe zu einem Standortflug. Die Windrichtung zur Startzeit kam aus WNW und die Thermik begann sich zu entwickeln, so dass ich relativ schnell an Höhe gewann. Nachdem ich mich eine Weile über dem Startort halten konnte, änderte sich ständig die Windrichtung. Ich entschloss mich deshalb, den Landeanflug einzuleiten und oben auf der Wasserkuppe zu landen. Beim Endanflug, in Bodennähe, änderte sich wieder der Wind, so dass ich die Richtung des Endanfluges korrigieren musste. Andere Piloten hatten sich für den Start vorbereitet, konnten aber wegen dem ständigen Wechsel des Windes nicht starten. Ich bin dann mit den Füßen in den Gleitschirm des Geschädigten eingeflogen und habe diesen an der rechten Seite stark beschädigt. Ein Ausweichen war nicht mehr möglich."
                   "#### response: \n"
                    "{"
                    "\"report_as\": \"pilot\","
                    "\"flight_equipment\": \"paraglider\","
                    "\"date\": \"28.04.2022\","
                    "\"time\": \"11:45\","
                    "\"location\": \"Wasserkuppe / Westhang\","
                    "\"flight_type\": \"local_flight\","
                    "\"harness_impact\": \"feet_ahead\","
                    "\"weather_turbulences\": \"moderately_turbulent\","
                    "\"weather_thermic\": \"moderately_3_ms\","
                    "\"flight_phase\": \"landing\","
                    "\"start_type\": \"slope_start\","
                    "\"landing\": \"top_landing\","
                    "\"rescue_tool\": \"not_triggered\","
                    "\"collision\": \"collision_with_paraglider_or_hang_glider\","
                    "\"pilot_error\": \"miscalculation_wind_terrain\","
                    "\"please_specify_here\": \"third_party_damage\""
                    "}"
                    "\n #### accident report: \n"
                   f"{report}"
                    "#### response: \n")

    json_llm = call.llm_CALL_one_shot(instruction, report_id)

    if json_llm is None:
        print("Error in LLM-Vaidation")
        save_data_csv(name, report_id, json_llm, None, "Validation Error")
        return

    if print_output:
        print("###### Additional Infos given ######")
        user_input, weather_info_bool, injured_body_parts_info_bool = connection.get_suppl_info()
        print(
            f"weather_further_information: {weather_info_bool}\ninjured_body_parts_sup_info_pilot: {injured_body_parts_info_bool}")
        print("###### Ground Truth ######")
        print(connection.get_ground_truth_auto_eval(report_id))
        print("###### json llm ######")
        print(json_llm)

    # 2. JSON Comperator
    changedData, addedData = comperator.compare_json_auto_eval(report_id, json_llm)

    # 3. Save Data
    save_data_csv(name, report_id, json_llm, changedData, addedData)

#endregion

#region prompt_engineering_few_shot
def prompt_engineering_few_shot(report_id, name):
    taxonomy = json.load(open("Taxonomy/JSON/taxonomy_annotated_list.json", "r", encoding="utf-8"))
    report = connection.get_accident_report_auto_eval(report_id)
    instruction = ("You are a paraglider safety expert. "
                   "You want to classify accident reports according to a classification schema. "
                   "The classification schema holds attributes like (pilot_error, flight_type, etc.) and a list of possible values (e.g.[pilot, authority, other])"
                   "Think step by step:"
                   "1. Choose all attributes that are directly or indirectly given in the accident report"
                   "2. Classify each attribute you have chosen with one value from the schema."
                   "3. Respond with your result in a JSON schema. "
                    "Here is the classification schema: \n"
                   f"{taxonomy}"

                   "\n#### Example:\n"
                   "#### accident report: \n"
                   "Am 28.04.2022 startete ich gegen 11.45 Uhr am Westhang der Wasserkuppe zu einem Standortflug. Die Windrichtung zur Startzeit kam aus WNW und die Thermik begann sich zu entwickeln, so dass ich relativ schnell an Höhe gewann. Nachdem ich mich eine Weile über dem Startort halten konnte, änderte sich ständig die Windrichtung. Ich entschloss mich deshalb, den Landeanflug einzuleiten und oben auf der Wasserkuppe zu landen. Beim Endanflug, in Bodennähe, änderte sich wieder der Wind, so dass ich die Richtung des Endanfluges korrigieren musste. Andere Piloten hatten sich für den Start vorbereitet, konnten aber wegen dem ständigen Wechsel des Windes nicht starten. Ich bin dann mit den Füßen in den Gleitschirm des Geschädigten eingeflogen und habe diesen an der rechten Seite stark beschädigt. Ein Ausweichen war nicht mehr möglich."
                   "\n#### response: \n"
                    "{"
                    "\"report_as\": \"pilot\","
                    "\"flight_equipment\": \"paraglider\","
                    "\"date\": \"28.04.2022\","
                    "\"time\": \"11:45\","
                    "\"location\": \"Wasserkuppe / Westhang\","
                    "\"flight_type\": \"local_flight\","
                    "\"harness_impact\": \"feet_ahead\","
                    "\"weather_turbulences\": \"moderately_turbulent\","
                    "\"weather_thermic\": \"moderately_3_ms\","
                    "\"flight_phase\": \"landing\","
                    "\"start_type\": \"slope_start\","
                    "\"landing\": \"top_landing\","
                    "\"rescue_tool\": \"not_triggered\","
                    "\"collision\": \"collision_with_paraglider_or_hang_glider\","
                    "\"pilot_error\": \"miscalculation_wind_terrain\","
                    "\"please_specify_here\": \"third_party_damage\""
                    "}"
                   "\n#### Example 2: \n"
                   "#### accident report: \n"
                   "Beim Flugmanöver \"Schnelle Acht\" im Rahmen des B-Scheinkurses hatte der Pilot durch einen Steuerfehler einen einseitigen Strömungsabriss. Nach zweifacher Umdrehung öffnete der Schirm mit Verhänger und ist daraufhin in einen Verhängersat übergegangen. Der Pilot öffnete sofort das Rettungsgerät und ist unverletzt im Baum gelandet. Aufgrund der Baumlandung hat der Schirm zwei kleine Risse, das Rettungsgerät wurde zur Überprüfung an den Hersteller geschickt."
                   "\n#### response: \n"
                   "{"
                    "\"report_as\": \"other\","
                    "\"flight_equipment\": \"paraglider\","
                    "\"flight_type\": \"training_flight\","
                    "\"weather_turbulences\": \"moderately_turbulent\","
                    "\"landing\": \"tree_landing\","
                    "\"rescue_tool\": \"intentionally_triggered\","
                    "\"rescue_equipment_opening\": \"successful\","
                    "\"paraglider_flight_behavior_f_e_f_c\": \"spin\","
                    "\"paraglider_flight_behavior_follow_up\": \"got_caught\","
                    "\"pilot_error\": \"control_error\","
                    "\"injuries_pilot\": \"unharmed\","
                    "}"
                    "\n #### accident report: \n"
                   f"{report}"
                    "\n#### response: \n")

    json_llm = call.llm_CALL_one_shot(instruction, report_id)

    if json_llm is None:
        print("Error in LLM-Vaidation")
        save_data_csv(name, report_id, json_llm, None, "Validation Error")
        return

    if print_output:
        print("###### Additional Infos given ######")
        user_input, weather_info_bool, injured_body_parts_info_bool = connection.get_suppl_info()
        print(
            f"weather_further_information: {weather_info_bool}\ninjured_body_parts_sup_info_pilot: {injured_body_parts_info_bool}")
        print("###### Ground Truth ######")
        print(connection.get_ground_truth_auto_eval(report_id))
        print("###### json llm ######")
        print(json_llm)

    # 2. JSON Comperator
    changedData, addedData = comperator.compare_json_auto_eval(report_id, json_llm)

    # 3. Save Data
    save_data_csv(name, report_id, json_llm, changedData, addedData)

#endregion

#endregion


#region Function Calling with Instructor

#TODO: Implement to choose from different Pydantic classes
def function_calling(report_id, name, pydantic_model):
    #1. API-Call
    report = connection.get_accident_report_auto_eval(report_id)
    json_llm = call.llm_CALL_function_call(report,report_id, pydantic_model)
    if json_llm is None:
        print("Error in LLM-Vaidation")
        save_data_csv(name, report_id, json_llm, None, "Validation Error")
        return
    #2. JSON Comperator
    changedData, addedData= comperator.compare_json_auto_eval(report_id, json_llm)

    #3. Save Data
    save_data_csv(name, report_id, json_llm, changedData, addedData)


def function_calling_multi(report_id, name):
    # 1. Get Report
    report = connection.get_accident_report_auto_eval(report_id)

    async def extract_pilot_info(report_id: str) -> validator.Extract_pilot_info:
        print("Pilot_info_extraction function has been called")
        pydantic_model = "Extract_pilot_info"
        return await asyncio.to_thread(call.OPEN_AI_API_call_function, report, report_id, pydantic_model)

    async def extract_equipment_info(report_id: str) -> validator.Extract_equipment_info:
        print("Equipment_info_extraction function has been called")
        pydantic_model = "Extract_equipment_info"
        return await asyncio.to_thread(call.OPEN_AI_API_call_function, report, report_id, pydantic_model)

    async def extract_event_info(report_id: str) -> validator.Extract_event_info:
        print("Event_info_extraction function has been called")
        pydantic_model = "Extract_event_info"
        return await asyncio.to_thread(call.OPEN_AI_API_call_function, report, report_id, pydantic_model)

    async def extract_malfunction_consequences_info(report_id: str) -> validator.Extract_malfunction_consequences_info:
        print("Malfunction_consequences_info_extraction function has been called")
        pydantic_model = "Extract_malfunction_consequences_info"
        return await asyncio.to_thread(call.OPEN_AI_API_call_function, report, report_id, pydantic_model)
    async def extract_weather_info(report_id: str) -> validator.Extract_weather_info:
        print("Weather_info_extraction function has been called")
        pydantic_model = "Extract_weather_info"
        output = await asyncio.to_thread(call.OPEN_AI_API_call_function, report, report_id, pydantic_model)
        return output

    async def gather():
        tasks_get_report_details = [
            extract_pilot_info(report),
            extract_equipment_info(report),
            extract_weather_info(report),
            extract_event_info(report),
            extract_malfunction_consequences_info(report),
        ]
        all_details = await asyncio.gather(*tasks_get_report_details)
        print(all_details)

        # Zusammenführen der Responses zu einem Dict
        merged_data = {}
        for detail in all_details:
            if(detail is None):
                print("Für diese Kategorie wurde nichts gefunden")
                continue
            else:
                merged_data.update(detail)
        # Map das zusammengeführte Dict auf das Pydantic Model extract_accident_info
        accident_info = validator.map_to_extract_accident_info(merged_data)
        if print_output:
            print("########### Accident Info ###########")
            print(accident_info)
            print("########### Accident Info Filtered ###########")
            print(accident_info.model_dump(exclude_unset=True))

        return accident_info.model_dump(exclude_unset=True)

    json_llm = asyncio.run(gather())

    # 2. JSON Comperator
    changedData, addedData = comperator.compare_json_auto_eval(report_id, json_llm)

    # 3. Save Data
    save_data_csv(name, report_id, json_llm, changedData, addedData)

#endregion

#endregion
########################################################################################################################

#region Putting it ALL TOGETHER
def prompt_engineering_baseline_run(report_id, repetitions, new_document):
    name = "prompt_eng_baseline"
    if new_document:
        new_run(name)

    for i in range(repetitions):
        prompt_engineering_baseline(report_id, name)

def prompt_engineering_simple_run(report_id, repetitions, new_document):
    name = "prompt_eng_simple"
    if new_document:
        new_run(name)

    for i in range(repetitions):
        prompt_engineering_simple(report_id, name)

def prompt_engineering_advanced_run(report_id, repetitions, new_document):
    name = "prompt_eng_advanced"
    if new_document:
        new_run(name)

    for i in range(repetitions):
        prompt_engineering_advanced(report_id, name)

def prompt_engineering_one_shot_run(report_id, repetitions, new_document):
    name = "prompt_eng_one_shot"
    if new_document:
        new_run(name)

    for i in range(repetitions):
        prompt_engineering_one_shot(report_id, name)


def prompt_engineering_few_shot_run(report_id, repetitions, new_document):
    name = "prompt_eng_few_shot"
    if new_document:
        new_run(name)

    for i in range(repetitions):
        prompt_engineering_few_shot(report_id, name)



def function_calling_simple_run(report_id, repetitions, new_document):
    name = "function_calling_simple"
    pydantic_model = "reports"
    if new_document:
        new_run(name)

    for i in range(repetitions):
        function_calling(report_id, name, pydantic_model)

def function_calling_advanced_run(report_id, repetitions, new_document):
    name = "function_calling_advanced"
    pydantic_model = "extract_accident_info"
    if new_document:
        new_run(name)

    for i in range(repetitions):
        function_calling(report_id, name, pydantic_model)

def function_calling_advanced_literal_run(report_id, repetitions, new_document):
    name = "function_calling_advanced_literal"
    pydantic_model = "extract_accident_info_literals"
    if new_document:
        new_run(name)

    for i in range(repetitions):
        function_calling(report_id, name, pydantic_model)

def function_calling_multi_run(report_id, repetitions, new_document):
    name = "function_calling_multi"
    if new_document:
        new_run(name)

    for i in range(repetitions):
        function_calling_multi(report_id, name)


#endregion
########################################################################################################################

if __name__ == "__main__":
    print_output = False
    new_document = False
    repetitions = 5
    report_id = 18506               #18898, 18506
    # all_reports = [13982, 14858, 15086, 15522, 15890, 16594, 16614,
    #                18506, 18898, 20018, 20854, 20902, 21322, 22834,
    #                23394, 23702, 24058, 24074, 24258, 24266, 25570, 25818]

    # FÜr one_shot exkludiere 23702
    # für few_shot exkludiere 23702, 13982





    #region Prompt engineering

    # Baseline Testing
    prompt_engineering_baseline_run(
        report_id=16594,
        repetitions=1,
        new_document=new_document
    )
    # #iterate over all reports given in this array
    # report_array = [15086, 22834, 24058]
    # for report_id in report_array:
    #     prompt_engineering_baseline(report_id)

    # new_run("prompt_eng_baseline")
    # prompt_engineering_baseline_run(
    #     report_id=report_id,
    #     repetitions=repetitions,
    #     new_document=True
    # )

    # new_run("prompt_eng_baseline")
    # for report_id in all_reports:
    #     prompt_engineering_baseline_run(
    #         report_id=report_id,
    #         repetitions=repetitions,
    #         new_document=new_document
    #     )

    #
    # Simple Testing
    # new_run("prompt_eng_simple")
    #
    # for report_id in all_reports:
    #     prompt_engineering_simple_run(
    #         report_id=report_id,
    #         repetitions=repetitions,
    #         new_document=new_document
    #     )

    #
    # # Advanced Testing
    # new_run("prompt_eng_advanced")
    #
    # for report_id in all_reports:
    #     prompt_engineering_advanced_run(
    #         report_id=report_id,
    #         repetitions=repetitions,
    #         new_document=new_document
    #     )
    # # One Shot Testing
    # new_run("prompt_eng_one_shot")
    #
    # for report_id in all_reports:
    #     prompt_engineering_one_shot_run(
    #         report_id=report_id,
    #         repetitions=repetitions,
    #         new_document=new_document
    #     )
    # print("report_id: ", report_id)
    #
    #

    # Few Shot Testing
    # new_run("prompt_eng_few_shot")
    # for report_id in all_reports:
    #     prompt_engineering_few_shot_run(
    #         report_id=report_id,
    #         repetitions=repetitions,
    #         new_document=new_document
    #     )
    #     print("report_id: ", report_id)


    # #endregion


    # Function Call advanced


    # function_calling_advanced_run(
    #     report_id=14858,
    #     repetitions=1,
    #     new_document=new_document
    # )
    #
    # new_run("function_calling_advanced")
    # for report_id in all_reports:
    #     function_calling_advanced_run(
    #         report_id=report_id,
    #         repetitions=repetitions,
    #         new_document=new_document
    #     )
    #     print("report_id: ", report_id)
    # #
    # new_run("function_calling_advanced_literal")
    # function_calling_advanced_literal_run(
    #     report_id=report_id,
    #     repetitions=repetitions,
    #     new_document=new_document
    # )

    # function_calling_multi_run(
    #     report_id=18898,
    #     repetitions=1,
    #     new_document=new_document
    # )


    # Function Call multi
    # new_run("function_calling_multi")
    # function_calling_multi_run(
    #     report_id=25818,
    #     repetitions=5,
    #     new_document=new_document
    # )


    # function calling literals

    #new_run("function_calling_advanced_literal")
    # function_calling_advanced_literal_run(
    #     report_id=14858,
    #     repetitions=1,
    #     new_document=new_document
    # )
    #
    # function_calling_multi_run(
    #     report_id=14858,
    #     repetitions=2,
    #     new_document=new_document
    # )

    # function_calling_multi_functions_run(
    #     report_id=report_id,
    #     repetitions=5,
    #     new_document=new_document
    # )

    #endregion
