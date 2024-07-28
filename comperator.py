
import json
from deepdiff import DeepDiff
import pandas as pd
from enum import Enum

# eigene Module
import call
import connection


#region HELPER FUNCTIONS
def count_attributes(json_llm):
    return len(json_llm.keys())

def find_values_for_keys(input_dict, keys):
    values = []
    for key in keys:
        values.append(input_dict[key])
    return values
#endregion
########################################################################################################################

#region AUTO EVAL
def get_json_database_auto_eval(report_id):
    x = connection.get_json_database_auto_eval(report_id)
    if x:
        return x
    else:
        return None

def compare_json_auto_eval(report_id, json_llm):
    # read json tuples from ground truth
    json_database = get_json_database_auto_eval(report_id)
    changes = DeepDiff(json_database, json_llm, ignore_order=True)
    changedData, addedData = output_to_dataframe_auto_eval(changes, json_llm)

    return changedData, addedData

def output_to_dataframe_auto_eval(changes, json_llm):
    values_changed = changes.get("values_changed", {})
    dictionary_item_added = changes.get("dictionary_item_added", {})
    # Daten für DataFrame vorbereiten
    changedData = {
        'values_changed': [v.split("['")[1][:-2] for v in values_changed.keys()],
        'old_value': [v['old_value'] for v in values_changed.values()],
        'new_value': [v['new_value'] for v in values_changed.values()],
    }

    added_keys = [v.split("['")[1][:-2] for v in dictionary_item_added]

    # values zu den Keys aus added Data herausfinden:
    added_values = find_values_for_keys(json_llm, added_keys)

    addedData = pd.DataFrame({
        'added_key': added_keys,
        'added_value': added_values,
    })

    # DataFrames erstellen
    changedData = pd.DataFrame(changedData)
    addedData = pd.DataFrame(addedData)

    return changedData, addedData

def dataframes_to_json_changes(changed_data, added_data):
    changed_json = {}
    added_json = {}

    if not changed_data.empty:
        # Füge geänderte Werte hinzu
        for index, row in changed_data.iterrows():
            changed_json[row['values_changed']] = row['new_value']

    if not added_data.empty:
        # Füge hinzugefügte Werte hinzu
        for index, row in added_data.iterrows():
            added_json[row['added_key']] = row['added_value']

    # Konvertiere in JSON-Strings
    changed_json_str = json.dumps(changed_json, indent=4)
    added_json_str = json.dumps(added_json, indent=4)

    return changed_json_str, added_json_str

def convert_dict_to_json(input_dict):
    json_data = {}
    for key, value in input_dict.items():
        if isinstance(value, Enum):
            json_data[key] = value.value
        else:
            json_data[key] = value
    return json_data
#endregion
########################################################################################################################

#region Streamlit

def get_json_database(report_id):
    # Hier solltest du deine eigene Implementierung der SQL-Verbindung einsetzen
    x = connection.get_json_database(report_id)
    if x:
        return x
    else:
        return None

def get_json_llm(report_id):
    report = connection.get_accident_report(report_id)
    JSON_LLM = call.llm_analysis(report, report_id)

    return JSON_LLM


def compare_json_streamlit(report_id):
    json_database = get_json_database(report_id)
    json_llm = get_json_llm(report_id)
    changes = DeepDiff(json_database, json_llm, ignore_order=True)
    changedData, addedData = output_to_dataframe_streamlit(changes, json_llm)
    count_changed = len(changedData.index)
    count_added = len(addedData.index)
    return changedData, addedData, count_changed, count_added


def output_to_dataframe_streamlit(changes, json_llm):
    values_changed = changes.get("values_changed", {})
    dictionary_item_added = changes.get("dictionary_item_added", {})
    print("Values changed:\n")
    print(changes)
    # Daten für DataFrame vorbereiten
    changedData = {
        'values_changed': [v.split("['")[1][:-2] for v in values_changed.keys()],
        'old_value': [v['old_value'] for v in values_changed.values()],
        'new_value': [v['new_value'] for v in values_changed.values()],
    }

    added_keys = [v.split("['")[1][:-2] for v in dictionary_item_added]
    print("added Keys:\n")
    print(added_keys)

    # values zu den Keys aus added Data herausfinden:
    added_values = find_values_for_keys(json_llm, added_keys)
    print("added Values:\n")
    print(added_values)

    addedData = pd.DataFrame({
        'added_key': added_keys,
        'added_value': added_values,
    })

    # DataFrames erstellen
    changedData = pd.DataFrame(changedData)
    addedData = pd.DataFrame(addedData)


    # Prepare Data for streamlit
    changedData = add_bool_accept(changedData)
    changedData = add_bool_wrong(changedData)
    addedData = add_bool_accept(addedData)
    addedData = add_bool_wrong(addedData)
    # Streamlit needs a boolean colum to use the checkbox functionality

    return changedData, addedData

def add_bool_accept(input):
    input["accept"] = False
    return input
def add_bool_wrong(input):
    input["wrong_value"] = False
    return input

#endregion
########################################################################################################################

if __name__ == '__main__':
    # Streamlit
    # print(get_json_llm(21322))
    # changedData, addedData = compare_json(15618)
    # print(changedData)
    # print("######\n")
    # print(addedData)

    # AutoEval
    # compare_json_auto_eval(24058)

    compare_json_auto_eval(14858, )
    def compare_json_auto_eval(report_id, json_llm):
        # read json tuples from ground truth
        json_database = get_json_database_auto_eval(report_id)
        changes = DeepDiff(json_database, json_llm, ignore_order=True)
        changedData, addedData = output_to_dataframe_auto_eval(changes, json_llm)

        return changedData, addedData
