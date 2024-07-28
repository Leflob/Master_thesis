import mariadb
import sys
import json


#region VARIABLES and MARIA DB CONNECTION

db_password = open("API_keys/db_password.txt", "r", encoding="utf-8").read()
try:
    conn = mariadb.connect(
        user = "root",
        password = f"{db_password}",
        host = "localhost",
        port = 3306,
        database = "dhvdump"
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

cur = conn.cursor()

# Variables
weather_info_bool = None
injured_body_parts_info_bool = None
user_input = None

#endregion
########################################################################################################################

#region HELPER FUNCTIONS
def get_suppl_info():
    return user_input, weather_info_bool, injured_body_parts_info_bool

#endregion
########################################################################################################################

#region AUTO EVAL

def get_json_database_auto_eval(id):
    with open(f"Input/{id}.json", "r", encoding="utf-8") as file:
        x = json.load(file)
    # print("\n###### json database ######")
    # print(f"{x}\n")
    return x

def get_accident_report_auto_eval(id):
    json_database = get_json_database_auto_eval(id)

    combined_info = create_info_string(json_database)

    return combined_info


def create_info_string(data):
    # store info about what is included in the prompt
    global weather_info_bool, injured_body_parts_info_bool, user_input

    info_string = ""
    if 'additional_information' in data and data['additional_information']:
        info_string += data['additional_information'] + "\n"


    if 'weather_further_information' in data and data['weather_further_information']:
        weather_info_bool = True
        info_string += data['weather_further_information'] + "\n"
    else:
        weather_info_bool = False

    if 'injured_body_parts_sup_info_pilot' in data and data['injured_body_parts_sup_info_pilot']:
        injured_body_parts_info_bool = True
        info_string += data['injured_body_parts_sup_info_pilot'] + "\n"
    else:
        injured_body_parts_info_bool = False

    user_input = info_string.strip()
    # print(f"weather_further_information: {weather_info_bool} \n injured_body_parts_sup_info_pilot: {injured_body_parts_info_bool}")
    return user_input


def get_ground_truth_auto_eval(id):
    json_data = get_json_database_auto_eval(id)
    # Liste der unerwünschten Attribute
    unwanted_attributes = ['additional_information', 'word_counter', 'id', 'weather_further_information',
                           'injured_body_parts_sup_info_pilot']

    # Kopie des JSON erstellen, um das Original nicht zu verändern
    cleaned_json = json_data.copy()

    # Unerwünschte Attribute entfernen
    for attr in unwanted_attributes:
        cleaned_json.pop(attr, None)

    return cleaned_json

#endregion
########################################################################################################################

#region STREAMLIT

def get_accident_report(id):    # additional_information + weather + sup_info_injuries
    # store info about what is included in the prompt
    global weather_info_bool, injured_body_parts_info_bool, user_input

    cur.execute(
        f"SELECT JSON_UNQUOTE(JSON_EXTRACT(content, '$.description_and_additional_information')) AS description_and_additional_information, "
        f"JSON_UNQUOTE(JSON_EXTRACT(content, '$.weather_further_information')) AS weather_further_information, "
        f"JSON_UNQUOTE(JSON_EXTRACT(content, '$.injured_body_parts_sup_info_pilot')) AS injured_body_parts_sup_info_pilot "
        f"FROM incidents "
        f"WHERE id = {id};")
    result_tuple = cur.fetchone()
    if result_tuple:
        description = result_tuple[0] if result_tuple[0] else ""
        if result_tuple[1]:
            weather_info = result_tuple[1]
            weather_info_bool = True
        else:
            weather_info = ""
            weather_info_bool = False

        if result_tuple[2]:
            injured_body_parts_info = result_tuple[2]
            injured_body_parts_info_bool = True
        else:
            injured_body_parts_info = ""
            injured_body_parts_info_bool = False

        combined_info = f"{description} \n{weather_info} \n{injured_body_parts_info}"
        user_input = combined_info.strip()

        return user_input  # Trim leading/trailing whitespaces
    else:
        return None


def get_json_database(id):      # Extract relevant keys Select content from incidents
    # Liste der gewünschten Attribute
    desired_attributes = ["report_as", "flight_equipment", "date", "time", "airfield", "location",
                          "country", "flight_type",

                          "age", "starting_weight", "gender", "nationality",
                          "type_of_flight_license", "flies_since", "total_nof", "total_nof_six_months",
                          "nof_accident_equipment", "safety_training",

                          "aircraft_manufacturer", "aircraft_model", "aircraft_size", "aircraft_classification",
                          "aircraft_last_check",

                          "reserve_parachute_manufacturer", "reserve_parachute_model", "reserve_parachute_size",
                          "reserve_parachute_controllable", "reserve_parachute_last_repack",

                          "harness_manufacturer", "harness_model", "harness_rescue_equipment_container",
                          "harness_back_protection", "harness_impact",

                          "accessories_helmet", "accessories_helmet_ce_966_tested", "accessories_ankle_high_shoes",

                          "weather_wind", "weather_turbulences", "weather_thermic", "weather_special_conditions",


                          "flight_phase", "start_type", "landing", "rescue_tool",
                          "event_sequence_triggered_at_m_agl_gnd", "rescue_equipment_opening",

                          "collision", "paraglider_flight_behavior_f_e_f_c",
                          "paraglider_flight_behavior_triggered", "paraglider_flight_behavior_follow_up",

                          "pilot_error", "equipment_malfunction",

                          "injuries_pilot", "injured_body_parts_pilot",

                          "please_specify_here",

                          "description_and_additional_information", "weather_further_information",
                          "injured_body_parts_sup_info_pilot"
                          ]

    query = f"SELECT content FROM incidents WHERE id = {id};"
    cur.execute(query)
    result_tuple = cur.fetchone()

    if result_tuple:
        json_string = result_tuple[0]

        # JSON in ein Python Dictionary umwandeln
        data = json.loads(json_string)

        # Dictionary nur mit den gewünschten Attributen erstellen
        specific_attributes = {attr: data[attr] for attr in desired_attributes if attr in data}

        return specific_attributes if specific_attributes else None
    else:
        return None

#endregion
########################################################################################################################


if __name__ == '__main__':
    # x = get_json_database(26746)
    # print(x)
    # print(type(x))
    # print(get_accident_report(21322))

    print(get_accident_report_auto_eval("test"))


    print("#### JSON Database ####")
    print(get_json_database_auto_eval("test"))
    print("#### Ground Truth ####")
    print(get_ground_truth_auto_eval("test"))
