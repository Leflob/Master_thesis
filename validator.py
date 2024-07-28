from pydantic import BaseModel, field_validator
from typing import Optional
import csv
import json

# my imports
import call

#for new version
from pydantic import BaseModel, field_validator, Field, AfterValidator, ValidationError
from enum import Enum
from typing import Literal
from typing import ClassVar
from typing import Union
from typing_extensions import Annotated
import datetime

# global variables
null_dict = ["null", None, "unknown"]


def count_csv_lines():
    with open("Output/AutoEval/Backup/save_log.csv", 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        line_count = 0
        for row in csvreader:
            line_count += 1
        return line_count


#region FIELD VALIDATORS (V1)   - class reports(BaseModel)

# class reports(BaseModel):
#     report_as: Optional[str] = Field(None, description="USE only one of the following: pilot, flight_school_flight_instructor, witness or unknown")
#     flight_equipment: Optional[str] = Field(None, description="USE only one of the following: paraglider, hang_glider, fixed_wing, speedflyer_miniwing_foot_launch or unknown")
#     flight_type: Optional[str] = Field(None, description="USE only one of the following: cross_country_flight, local_flight, training_flight, assisted_flying_flight_travel_training, competition_flight, passenger_flight, acro_flight, safety_training_flight or unknown")
#     age: Optional[int]
#     starting_weight: Optional[int]
#     gender: Optional[str]
#
#     type_of_flight_license: Optional[str]
#     flies_since: Optional[int]
#     total_nof: Optional[int]
#     total_nof_six_months: Optional[int]
#     nof_accident_equipment: Optional[int]
#     safety_training: Optional[str] = Field(None, description="USE only one of the following: not_completed, graduated_with_different_pattern, graduated_with_accident_pattern or unknown")
#
#     aircraft_manufacturer: Optional[str]
#     aircraft_model: Optional[str]
#     aircraft_size: Optional[str]
#     aircraft_last_check: Optional[str]
#
#     reserve_parachute_manufacturer: Optional[str]
#     reserve_parachute_model: Optional[str]
#     reserve_parachute_size: Optional[str]
#     reserve_parachute_controllable: Optional[str]
#     reserve_parachute_last_repack: Optional[str]
#
#     harness_manufacturer: Optional[str]
#     harness_model: Optional[str]
#     harness_rescue_equipment_container: Optional[str]
#     harness_back_protection: Optional[str]
#     harness_impact: Optional[str]
#
#     accessories_helmet: Optional[str]
#     accessories_helmet_ce_966_tested: Optional[str]
#     accessories_ankle_high_shoes: Optional[str]
#
#     weather_wind: Optional[str] = Field(None, description="USE only one of the following: 0_5_kmh, 5_10_kmh, 10_15_kmh, 15_20_kmh, 20_25_kmh, 25_30_kmh, 30_35_kmh, 35_40_kmh, 40_45_kmh, more_45_kmh or unknown")
#     weather_turbulences: Optional[str] = Field(None, description="USE only one of the following: non_turbulent, slightly_turbulent, moderately_turbulent, strong_turbulent, very_strong_turbulent or unknown")
#     weather_thermic: Optional[str] = Field(None, description="USE only one of the following: slightly_1_ms, moderately_3_ms, strong_5_ms, very_strong_more_5_ms or unknown")
#     weather_special_conditions: Optional[str] = Field(None, description="USE only one of the following: flight_in_clouds_fog, foehn, front_influence, leeside, rain_snow, thundery or unknown")
#     flight_phase: Optional[str] = Field(None, description="USE only one of the following: departure, extreme_flight_acro_safety_training, glide, groundhandling, landing, soaring, start_run, thermal_flight or unknown")
#     start_type: Optional[str] = Field(None, description="USE only one of the following: slope_start, ul_towing, winch_tow_launch or unknown")
#     landing: Optional[str] = Field(None, description="USE only one of the following: building, normal_landing, off_field_landing, other, power_line_ropeway_cable, top_landing, tree_landing, water_landing or unknown")
#
#     rescue_tool: Optional[str] = Field(None, description="USE only one of the following: intentionally_triggered, not_triggered, unintentionally_triggered or unknown")
#     event_sequence_triggered_at_m_agl_gnd: Optional[str] = Field(None, description="USE only one of the following: less_20, 20_50, 50_70, 70_100, 100_250, 250_500, more_500 or unknown")
#     rescue_equipment_opening: Optional[str] = Field(None, description="USE only one of the following: not_successful_entanglement_with_umbrella_cap, not_successful_other_reasons, not_successful_too_little_height, successful or unknown")
#     collision: Optional[str] = Field(None, description="USE only one of the following: collision_with_another_vehicle, collision_with_obstacle, collision_with_paraglider_or_hang_glider or unknown")
#     paraglider_flight_behavior_f_e_f_c: Optional[str] = Field(None, description="USE only one of the following: unilateral_collapse, spin, not_specified_frontal_collapse, fullstall, frontal_collapse, got_caught, stalled_flight, steep_spiral, lines_unclear or unknown")
#     paraglider_flight_behavior_triggered: Optional[str] = Field(None, description="USE only one of the following: less_5, 5_10, 10_20, 20_50, 50_70, 70_100, 100_250, 250_500, more_500 or unknown")
#     paraglider_flight_behavior_follow_up: Optional[str] = Field(None, description="USE only one of the following: fullstall, frontal_collapse, got_caught, one_sided_collapse, spiral_got_caught, spin, stable_frontal_collapse, stable_stalled_flight, stable_steep_spiral, stalled_flight, steep_spiral, twist or unknown")
#
#     pilot_error: Optional[str] = Field(None, description="USE only one of the following: affected, control_error, disregard_of_flight_rules, exuberance, inadequate_airspace_observation, inattention, inexperience, miscalculation_weather, miscalculation_wind_terrain, preflight_check_takeoff_check, risk_taking, spatial_misjudgement, traffic_density, unsuitable_takeoff_landing_site or unknown")
#     equipment_malfunction: Optional[str] = Field(None, description="USE only one of the following: aircraft, harness, rescue_tool, winch_towing_equipment or unknown")
#
#     injuries_pilot: Optional[str] = Field(None, description="USE only one of the following: deadly_injured, seriously_injured, slightly_injured, unharmed or unknown")
#     injured_body_parts_pilot: Optional[str] = Field(None, description="USE only one of the following: basin, chest, cervical_spine, feet_legs, hands_arms_shoulder, head, lumbar_spine, thoracic_spine, internal_organs or unknown")


class reports(BaseModel):
    report_as: Optional[str]
    flight_equipment: Optional[str]
    flight_type: Optional[str]
    age: Optional[int]
    starting_weight: Optional[int]
    gender: Optional[str]

    type_of_flight_license: Optional[str]
    flies_since: Optional[int]
    total_nof: Optional[int]
    total_nof_six_months: Optional[int]
    nof_accident_equipment: Optional[int]
    safety_training: Optional[str]

    aircraft_manufacturer: Optional[str]
    aircraft_model: Optional[str]
    aircraft_size: Optional[str]
    aircraft_last_check: Optional[str]

    reserve_parachute_manufacturer: Optional[str]
    reserve_parachute_model: Optional[str]
    reserve_parachute_size: Optional[str]
    reserve_parachute_controllable: Optional[str]
    reserve_parachute_last_repack: Optional[str]

    harness_manufacturer: Optional[str]
    harness_model: Optional[str]
    harness_rescue_equipment_container: Optional[str]
    harness_back_protection: Optional[str]
    harness_impact: Optional[str]

    accessories_helmet: Optional[str]
    accessories_helmet_ce_966_tested: Optional[str]
    accessories_ankle_high_shoes: Optional[str]

    weather_wind: Optional[str]
    weather_turbulences: Optional[str]
    weather_thermic: Optional[str]
    weather_special_conditions: Optional[str]
    flight_phase: Optional[str]
    start_type: Optional[str]
    landing: Optional[str]

    rescue_tool: Optional[str]
    event_sequence_triggered_at_m_agl_gnd: Optional[str]
    rescue_equipment_opening: Optional[str]
    collision: Optional[str]
    paraglider_flight_behavior_f_e_f_c: Optional[str]
    paraglider_flight_behavior_triggered: Optional[str]
    paraglider_flight_behavior_follow_up: Optional[str]

    pilot_error: Optional[str]
    equipment_malfunction: Optional[str]

    injuries_pilot: Optional[str]
    injured_body_parts_pilot: Optional[str]

    @field_validator("report_as")
    def validate_report_as(cls, v):
        if v in null_dict:
            v = "null"
        if v not in ["pilot", "flight_school_flight_instructor", "witness", "null", "unknown"]:
            cls.save_error("report_as", v)
        #     raise ValueError("For report_as you can only choose one of those values: "
        #                      "pilot, flight_school_flight_instructor, other, authority, witness, passenger, null")
        return v

    @field_validator("flight_equipment")
    def validate_flight_equipment(cls, v):
        if v in null_dict:
            v = "null"
        if v not in ["paraglider", "hang_glider", "fixed_wing", "speedflyer_miniwing_foot_launch",
                     "other", "null", "unknown"]:
            cls.save_error("flight_equipment", v)
            # raise ValueError(f"LLM suggested {v}, but it is not a valid value")
        return v

    @field_validator("flight_type")
    def validate_flight_type(cls, v):
        if v in null_dict:
            v = "null"
        if v not in ["cross_country_flight", "local_flight", "training_flight",
                     "assisted_flying_flight_travel_training", "competition_flight",
                     "passenger_flight", "acro_flight", "safety_training_flight", "null", "unknown"]:
            cls.save_error("flight_type", v)
            # raise ValueError(f"LLM suggested {v}, but it is not a valid value")
        return v

    @field_validator("gender")
    def validate_gender(cls, v):
        if v in null_dict:
            v = "null"
        if v not in ["m", "w", "d", "null", "unknown"]:
            cls.save_error("gender", v)
            # raise ValueError(f"LLM suggested {v}, but it is not a valid value")
        return v

    @field_validator("safety_training")
    def validate_safety_training(cls, v):
        if v in null_dict:
            v = "null"
        if v not in ["not_completed", "graduated_with_different_pattern",
                     "graduated_with_accident_pattern", "null", "unknown"]:
            cls.save_error("safety_training", v)
            # raise ValueError(f"LLM suggested {v}, but it is not a valid value")
        return v

    @field_validator("reserve_parachute_controllable")
    def validate_reserve_parachute_controllable(cls, v):
        if v in null_dict:
            v = "null"
        if v not in ["yes", "no", "null", "unknown"]:
            cls.save_error("reserve_parachute_controllable", v)
            # raise ValueError(f"LLM suggested {v}, but it is not a valid value")
        return v

    @field_validator("harness_rescue_equipment_container")
    def validate_harness_rescue_equipment_container(cls, v):
        if v in null_dict:
            v = "null"
        if v not in ["bottom", "site", "front", "back", "null", "unknown"]:
            cls.save_error("harness_rescue_equipment_container", v)
            # raise ValueError(f"LLM suggested {v}, but it is not a valid value")
        return v

    @field_validator("harness_back_protection")
    def validate_harness_back_protection(cls, v):
        if v in null_dict:
            v = "null"
        if v not in ["airbag", "foam_more_10", "foam_less_10", "foam_airbag", "none",
                     "null", "unknown"]:
            cls.save_error("harness_back_protection", v)
            # raise ValueError(f"LLM suggested {v}, but it is not a valid value")
        return v

    @field_validator("harness_impact")
    def validate_harness_impact(cls, v):
        if v in null_dict:
            v = "null"
        if v not in ["feet_ahead", "vertical", "lateral", "frontal", "back_ahead",
                     "null", "unknown"]:
            cls.save_error("harness_impact", v)
            # raise ValueError(f"LLM suggested {v}, but it is not a valid value")
        return v

    @field_validator("accessories_helmet")
    def validate_accessories_helmet(cls, v):
        if v in null_dict:
            v = "null"
        if v not in ["half_shelf_helmet", "integral_helmet", "null", "unknown"]:
            cls.save_error("accessories_helmet", v)
            # raise ValueError(f"LLM suggested {v}, but it is not a valid value")
        return v

    @field_validator("accessories_helmet_ce_966_tested")
    def validate_accessories_helmet_ce_966_tested(cls, v):
        if v in null_dict:
            v = "null"
        if v not in ["yes", "unknown", "no", "null", "unknown"]:
            cls.save_error("accessories_helmet_ce_966_tested", v)
            # raise ValueError(f"LLM suggested {v}, but it is not a valid value")
        return v

    @field_validator("accessories_ankle_high_shoes")
    def validate_accessories_ankle_high_shoes(cls, v):
        if v in null_dict:
            v = "null"
        if v not in ["yes", "unknown", "no", "null", "unknown"]:
            cls.save_error("accessories_ankle_high_shoes", v)
            # raise ValueError(f"LLM suggested {v}, but it is not a valid value")
        return v

    @field_validator("weather_wind")
    def validate_weather_wind(cls, v):
        if v in null_dict:
            v = "null"
        if v not in ["0_5_kmh", "5_10_kmh", "10_15_kmh", "15_20_kmh", "20_25_kmh", "25_30_kmh",
                     "30_35_kmh", "35_40_kmh", "40_45_kmh", "more_45_kmh", "null", "unknown"]:
            cls.save_error("weather_wind", v)
            # raise ValueError(f"LLM suggested {v}, but it is not a valid value")
        return v

    @field_validator("weather_turbulences")
    def validate_weather_turbulences(cls, v):
        if v in null_dict:
            return v
        if v not in ["non_turbulent", "slightly_turbulent", "moderately_turbulent", "strong_turbulent",
                     "very_strong_turbulent", "null", "unknown"]:
            cls.save_error("weather_turbulences", v)
            # raise ValueError(f"LLM suggested {v}, but it is not a valid value")
        return v

    @field_validator("weather_thermic")
    def validate_weather_thermic(cls, v):
        if v in null_dict:
            v = "null"
        if v not in ["slightly_1_ms", "moderately_3_ms", "strong_5_ms", "very_strong_more_5_ms",
                     "null", "unknown"]:
            cls.save_error("weather_thermic", v)
            # raise ValueError(f"LLM suggested {v}, but it is not a valid value")
        return v

    @field_validator("weather_special_conditions")
    def validate_weather_special_conditions(cls, v):
        if v in null_dict:
            v = "null"
        if v not in ["flight_in_clouds_fog", "foehn", "front_influence", "leeside", "rain_snow",
                     "thundery", "null", "unknown"]:
            cls.save_error("weather_special_conditions", v)
            # raise ValueError(f"LLM suggested {v}, but it is not a valid value")
        return v

    @field_validator("flight_phase")
    def validate_flight_phase(cls, v):
        if v in null_dict:
            v = "null"
        if v not in ["departure", "extreme_flight_acro_safety_training", "glide", "groundhandling",
                     "landing", "soaring", "start_run", "thermal_flight", "null", "unknown"]:
            cls.save_error("flight_phase", v)
            # raise ValueError(f"LLM suggested {v}, but it is not a valid value")
        return v

    @field_validator("start_type")
    def validate_start_type(cls, v):
        if v in null_dict:
            v = "null"
        if v not in ["slope_start", "ul_towing", "winch_tow_launch", "null", "unknown"]:
            cls.save_error("start_type", v)
            # raise ValueError(f"LLM suggested {v}, but it is not a valid value")
        return v

    @field_validator("landing")
    def validate_landing(cls, v):
        if v in null_dict:
            v = "null"
        if v not in ["building", "normal_landing", "off_field_landing", "other",
                     "power_line_ropeway_cable",
                     "top_landing", "tree_landing", "water_landing", "null", "unknown"]:
            cls.save_error("landing", v)
            # raise ValueError(f"LLM suggested {v}, but it is not a valid value")
        return v

    @field_validator("rescue_tool")
    def validate_rescue_tool(cls, v):
        if v in null_dict:
            v = "null"
        if v not in ["intentionally_triggered", "not_triggered", "unintentionally_triggered",
                     "null", "unknown"]:
            cls.save_error("rescue_tool", v)
            # raise ValueError(f"LLM suggested {v}, but it is not a valid value")
        return v

    @field_validator("event_sequence_triggered_at_m_agl_gnd")
    def validate_event_sequence_triggered_at_m_agl_gnd(cls, v):
        if v in null_dict:
            v = "null"
            return v
        if v not in ["less_20", "20_50", "50_70", "70_100", "100_250", "250_500", "more_500",
                     "null", "unknown"]:
            cls.save_error("event_sequence_triggered_at_m_agl_gnd", v)
            # raise ValueError(f"LLM suggested {v}, but it is not a valid value")
        return v

    @field_validator("rescue_equipment_opening")
    def validate_rescue_equipment_opening(cls, v):
        if v in null_dict:
            v = "null"
            return v
        if v not in ["not_successful_entanglement_with_umbrella_cap", "not_successful_other_reasons",
                     "not_successful_too_little_height", "successful", "null", "unknown"]:
            cls.save_error("rescue_equipment_opening", v)
            # raise ValueError(f"LLM suggested {v}, but it is not a valid value")
        return v

    @field_validator("collision")
    def validate_collision(cls, v):
        if v in null_dict:
            v = "null"
            return v
        if v not in ["collision_with_another_vehicle", "collision_with_obstacle",
                     "collision_with_paraglider_or_hang_glider", "null", "unknown"]:
            cls.save_error("collision", v)
            # raise ValueError(f"LLM suggested {v}, but it is not a valid value")
        return v

    @field_validator("paraglider_flight_behavior_f_e_f_c")
    def validate_paraglider_flight_behavior_f_e_f_c(cls, v):
        if v in null_dict:
            v = "null"
            return v
        if v not in ["unilateral_collapse", "spin", "not_specified_frontal_collapse", "fullstall",
                     "frontal_collapse", "got_caught", "stalled_flight", "steep_spiral",
                     "lines_unclear", "null", "unknown"]:
            cls.save_error("paraglider_flight_behavior_f_e_f_c", v)
            # raise ValueError(f"LLM suggested {v}, but it is not a valid value")
        return v

    @field_validator("paraglider_flight_behavior_triggered")
    def validate_paraglider_flight_behavior_triggered(cls, v):
        if v in null_dict:
            v = "null"
            return v
        if v not in ["less_5", "5_10", "10_20", "20_50", "50_70", "70_100", "100_250",
                     "250_500", "more_500", "null", "unknown"]:
            cls.save_error("paraglider_flight_behavior_triggered", v)
            # raise ValueError(f"LLM suggested {v}, but it is not a valid value")
        return v

    @field_validator("paraglider_flight_behavior_follow_up")
    @classmethod
    def validate_paraglider_flight_behavior_follow_up(cls, v):
        if v in null_dict:
            v = "null"
            return v
        if v not in ["fullstall", "frontal_collapse", "got_caught", "one_sided_collapse",
                     "spiral_got_caught", "spin", "stable_frontal_collapse", "stable_stalled_flight",
                     "stable_steep_spiral", "stalled_flight", "steep_spiral", "twist",
                     "null", "unknown"]:
            cls.save_error("paraglider_flight_behavior_follow_up", v)
            # raise ValueError(f"LLM suggested {v}, but it is not a valid value")
        return v

    @field_validator("pilot_error")
    def validate_pilot_error(cls, v):
        if v in null_dict:
            v = "null"
            return v
        if v not in ["affected", "control_error", "disregard_of_flight_rules", "exuberance",
                     "inadequate_airspace_observation", "inattention", "inexperience",
                     "miscalculation_weather", "miscalculation_wind_terrain",
                     "preflight_check_takeoff_check", "risk_taking", "spatial_misjudgement",
                     "traffic_density", "unsuitable_takeoff_landing_site", "null", "unknown"]:
            cls.save_error("pilot_error", v)
            # raise ValueError(f"LLM suggested {v}, but it is not a valid value")
        return v

    @field_validator("equipment_malfunction")
    def validate_equipment_malfunction(cls, v):
        if v in null_dict:
            v = "null"
            return v
        if v not in ["aircraft", "harness", "rescue_tool", "winch_towing_equipment",
                     "null", "unknown"]:
            cls.save_error("equipment_malfunction", v)
            # raise ValueError(f"LLM suggested {v}, but it is not a valid value")
        return v

    @field_validator("injuries_pilot")
    def validate_injuries_pilot(cls, v):
        if v in null_dict:
            v = "null"
            return v
        if v not in ["deadly_injured", "seriously_injured", "slightly_injured", "unharmed",
                     "null", "unknown"]:
            cls.save_error("injuries_pilot", v)
            # raise ValueError(f"LLM suggested {v}, but it is not a valid value")
        return v

    @field_validator("injured_body_parts_pilot")
    def validate_injured_body_parts_pilot(cls, v):
        if v in null_dict:
            v = "null"
            return v
        if v not in ["basin", "chest", "cervical_spine", "feet_legs", "hands_arms_shoulder",
                     "head", "lumbar_spine", "thoracic_spine", "internal_organs",
                     "null", "unknown"]:
            cls.save_error("injured_body_parts_pilot", v)
            # raise ValueError(f"LLM suggested {v}, but it is not a valid value")
        # if v != type(str):                                                                # Das hier funktioniert nicht. der input ist nie vom type string
        #     cls.save_error("injured_body_parts_pilot", v)
        #     # raise ValueError(f"LLM suggested {v}, but it is not a valid value")
        return v

    @classmethod
    def save_error(cls, field_name, value):
        counter = count_csv_lines()
        report_id = call.get_report_id()
        #report_id = get_report_id()
        with open("Output/AutoEval/error_log.csv", "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([counter, report_id, field_name, value])


    class Config:
        arbitrary_types_allowed = True
        # Manchmal kam ein fehler bei nen attributen mit nof in der Kennung.
        # Attribut wurde nicht als int erkannt.
        # Diese Konfiguration erlaubt es, arbiträre Werte zu akzeptieren.

#endregion  #
########################################################################################################################

#region ANNOTADED - with Enums (V2)

#region Allgemeine Informationen
class Report_as(Enum):
    pilot = "pilot"
    flight_school_flight_instructor = "flight_school_flight_instructor"
    witness = "witness"
    authority = "authority"
    passenger = "passenger"
    other = "other"
    unknown = "unknown"
    # not_given = "not_given"

class Flight_equipment(Enum):
    paraglider = "paraglider"
    hang_glider = "hang_glider"
    fixed_wing = "fixed_wing"
    speedflyer_miniwing_foot_launch = "speedflyer_miniwing_foot_launch"
    other = "other"
    unknown = "unknown"
    # not_given = "not_given"
class Flight_type(Enum):
    cross_country_flight = "cross_country_flight"
    local_flight = "local_flight"
    training_flight = "training_flight"
    assisted_flying_flight_travel_training = "assisted_flying_flight_travel_training"
    competition_flight = "competition_flight"
    passenger_flight = "passenger_flight"
    acro_flight = "acro_flight"
    safety_training_flight = "safety_training_flight"
    unknown = "unknown"
    # not_given = "not_given"

#endregion

#region Pilot
class Gender(Enum):
    m = "m"
    w = "w"
    d = "d"
    unknown = "unknown"
    # not_given = "not_given"

class Safety_training(Enum):
    not_completed = "not_completed"
    graduated_with_different_pattern = "graduated_with_different_pattern"
    graduated_with_accident_pattern = "graduated_with_accident_pattern"
    unknown = "unknown"
    # not_given = "not_given"

#endregion

#region Fluggerät
class Aircraft_classification(Enum):
    en_b = "en_b"
    en_a = "en_a"
    en_c = "en_c"
    unknown = "unknown"

class Reserve_parachute_controllable(Enum):
    yes = "yes"
    no = "no"
    unknown = "unknown"
    # not_given = "not_given"

#endregion

#region Gurtzeug
class Harness_rescue_equipment_container(Enum):
    bottom = "bottom"
    site = "site"
    front = "front"
    back = "back"
    unknown = "unknown"
    # not_given = "not_given"

class Harness_back_protection(Enum):
    airbag = "airbag"
    foam_more_10 = "foam_more_10"
    foam_less_10 = "foam_less_10"
    foam_airbag = "foam_airbag"
    none = "none"
    unknown = "unknown"
    # not_given = "not_given"

class Harness_impact(Enum):
    feet_ahead = "feet_ahead"
    vertical = "vertical"
    lateral = "lateral"
    frontal = "frontal"
    back_ahead = "back_ahead"
    unknown = "unknown"
    # not_given = "not_given"

#endregion

#region Zubehör
class Accessories_helmet(Enum):
    half_shelf_helmet = "half_shelf_helmet"
    integral_helmet = "integral_helmet"
    unknown = "unknown"
    # not_given = "not_given"

class Accessories_helmet_ce_966_tested(Enum):
    yes = "yes"
    no = "no"
    unknown = "unknown"
    # not_given = "not_given"

class Accessories_ankle_high_shoes(Enum):
    yes = "yes"
    no = "no"
    unknown = "unknown"
    # not_given = "not_given"

#endregion

#region Wetter

class Weather_wind(Enum):
    #Attribute dürfen wohl nicht mit Zahlen beginnen, daher immer ein m davor
    m0_5_kmh = "0_5_kmh"
    m5_10_kmh = "5_10_kmh"
    m10_15_kmh = "10_15_kmh"
    m15_20_kmh = "15_20_kmh"
    m20_25_kmh = "20_25_kmh"
    m25_30_kmh = "25_30_kmh"
    m30_35_kmh = "30_35_kmh"
    m35_40_kmh = "35_40_kmh"
    m40_45_kmh = "40_45_kmh"
    more_45_kmh = "more_45_kmh"
    unknown = "unknown"
    # not_given = "not_given"

class Weather_turbulences(Enum):
    non_turbulent = "non_turbulent"
    slightly_turbulent = "slightly_turbulent"
    moderately_turbulent = "moderately_turbulent"
    strong_turbulent = "strong_turbulent"
    very_strong_turbulent = "very_strong_turbulent"
    unknown = "unknown"
    # not_given = "not_given"

class Weather_thermic(Enum):
    slightly_1_ms = "slightly_1_ms"
    moderately_3_ms = "moderately_3_ms"
    strong_5_ms = "strong_5_ms"
    very_strong_more_5_ms = "very_strong_more_5_ms"
    unknown = "unknown"
    # not_given = "not_given"

class Weather_special_conditions(Enum):
    flight_in_clouds_fog = "flight_in_clouds_fog"
    foehn = "foehn"
    front_influence = "front_influence"
    leeside = "leeside"
    rain_snow = "rain_snow"
    thundery = "thundery"
    unknown = "unknown"
    # not_given = "not_given"

#endregion

#region Ereignisablauf

class Flight_phase(Enum):
    departure = "departure"
    extreme_flight_acro_safety_training = "extreme_flight_acro_safety_training"
    glide = "glide"
    groundhandling = "groundhandling"
    landing = "landing"
    soaring = "soaring"
    start_run = "start_run"
    thermal_flight = "thermal_flight"
    unknown = "unknown"
    # not_given = "not_given"

class Start_type(Enum):
    slope_start = "slope_start"
    ul_towing = "ul_towing"
    winch_tow_launch = "winch_tow_launch"
    unknown = "unknown"
    # not_given = "not_given"

class Landing(Enum):
    building = "building"
    normal_landing = "normal_landing"
    off_field_landing = "off_field_landing"
    other = "other"
    power_line_ropeway_cable = "power_line_ropeway_cable"
    top_landing = "top_landing"
    tree_landing = "tree_landing"
    water_landing = "water_landing"
    unknown = "unknown"
    # not_given = "not_given"

class Rescue_tool(Enum):
    intentionally_triggered = "intentionally_triggered"
    not_triggered = "not_triggered"
    unintentionally_triggered = "unintentionally_triggered"
    unknown = "unknown"
    # not_given = "not_given"

class Event_sequence_triggered_at_m_agl_gnd(Enum):
    less_20 = "less_20"
    m20_50 = "20_50"
    m50_70 = "50_70"
    m70_100 = "70_100"
    m100_250 = "100_250"
    m250_500 = "250_500"
    more_500 = "more_500"
    unknown = "unknown"
    # not_given = "not_given"

class Rescue_equipment_opening(Enum):
    not_successful_entanglement_with_umbrella_cap = "not_successful_entanglement_with_umbrella_cap"
    not_successful_other_reasons = "not_successful_other_reasons"
    not_successful_too_little_height = "not_successful_too_little_height"
    successful = "successful"
    unknown = "unknown"
    # not_given = "not_given"

class Collision(Enum):
    collision_with_another_vehicle = "collision_with_another_vehicle"
    collision_with_obstacle = "collision_with_obstacle"
    collision_with_paraglider_or_hang_glider = "collision_with_paraglider_or_hang_glider"
    unknown = "unknown"
    # not_given = "not_given"

#endregion

#region Gleitschirm Flugverhalten
class Paraglider_flight_behavior_f_e_f_c(Enum):
    unilateral_collapse = "unilateral_collapse"
    spin = "spin"
    not_specified_frontal_collapse = "not_specified_frontal_collapse"
    fullstall = "fullstall"
    frontal_collapse = "frontal_collapse"
    got_caught = "got_caught"
    stalled_flight = "stalled_flight"
    steep_spiral = "steep_spiral"
    lines_unclear = "lines_unclear"
    unknown = "unknown"
    # not_given = "not_given"

class Paraglider_flight_behavior_triggered(Enum):
    less_5 = "less_5"
    m5_10 = "5_10"
    m10_20 = "10_20"
    m20_50 = "20_50"
    m50_70 = "50_70"
    m70_100 = "70_100"
    m100_250 = "100_250"
    m250_500 = "250_500"
    more_500 = "more_500"
    unknown = "unknown"
    # not_given = "not_given"

class Paraglider_flight_behavior_follow_up(Enum):
    fullstall = "fullstall"
    frontal_collapse = "frontal_collapse"
    got_caught = "got_caught"
    one_sided_collapse = "one_sided_collapse"
    spiral_got_caught = "spiral_got_caught"
    spin = "spin"
    stable_frontal_collapse = "stable_frontal_collapse"
    stable_stalled_flight = "stable_stalled_flight"
    stable_steep_spiral = "stable_steep_spiral"
    stalled_flight = "stalled_flight"
    steep_spiral = "steep_spiral"
    twist = "twist"
    unknown = "unknown"
    # not_given = "not_given"

#endregion

#region Fehlfunktion
class Pilot_error(Enum):
    affected = "affected"
    control_error = "control_error"
    disregard_of_flight_rules = "disregard_of_flight_rules"
    exuberance = "exuberance"
    inadequate_airspace_observation = "inadequate_airspace_observation"
    inattention = "inattention"
    inexperience = "inexperience"
    miscalculation_weather = "miscalculation_weather"
    miscalculation_wind_terrain = "miscalculation_wind_terrain"
    preflight_check_takeoff_check = "preflight_check_takeoff_check"
    risk_taking = "risk_taking"
    spatial_misjudgement = "spatial_misjudgement"
    traffic_density = "traffic_density"
    unsuitable_takeoff_landing_site = "unsuitable_takeoff_landing_site"
class Equipment_malfunction(Enum):
    aircraft = "aircraft"
    harness = "harness"
    rescue_tool = "rescue_tool"
    winch_towing_equipment = "winch_towing_equipment"
    unknown = "unknown"
    # not_given = "not_given"

#endregion

#region Verletzungen
class Injuries_pilot(Enum):
    deadly_injured = "deadly_injured"
    seriously_injured = "seriously_injured"
    slightly_injured = "slightly_injured"
    unharmed = "unharmed"
    unknown = "unknown"
    # not_given = "not_given"

class Injured_body_parts_pilot(Enum):
    basin = "basin"
    chest = "chest"
    cervical_spine = "cervical_spine"
    feet_legs = "feet_legs"
    hands_arms_shoulder = "hands_arms_shoulder"
    head = "head"
    lumbar_spine = "lumbar_spine"
    thoracic_spine = "thoracic_spine"
    internal_organs = "internal_organs"
    unknown = "unknown"
    # not_given = "not_given"

#endregion


class extract_accident_info(BaseModel):

    report_as: Optional[Report_as] = Field(default= None, description="Who is reporting the incident?")
    flight_equipment: Optional[Flight_equipment] = Field(default= None)
    flight_type: Optional[Flight_type] = Field(default= None)
    age: Optional[int] = Field(default= None)
    starting_weight: Optional[int]= Field(default= None)
    gender: Optional[Gender] = Field(default= None)

    type_of_flight_license: Optional[str]= Field(default= None)
    flies_since: Optional[int]= Field(default= None, description="Year when pilot had first flight")                 # YYYY
    total_nof: Optional[int]= Field(default= None, description="Total number of flights")
    total_nof_six_months: Optional[int]= Field(default= None, description="Total number of flight hours in the last six months")
    nof_accident_equipment: Optional[int]= Field(default= None, description="Number of flights with the accident equipment")
    safety_training: Optional[Safety_training] = Field(default= None, description="Status of safety training")

    aircraft_manufacturer: Optional[str]= Field(default= None, description="Manufacturer of the paraglider")
    aircraft_model: Optional[str]= Field(default= None, description="Model of the paraglider")
    aircraft_size: Optional[str]= Field(default= None, description="Size of the paraglider")
    aircraft_classification: Optional[Aircraft_classification] = Field(default= None)
    aircraft_last_check: Optional[str]= Field(default= None)        # MM/YYYY #TODO: Das ist ein Datum, wie kann ich das hier angeben?

    harness_manufacturer: Optional[str]= Field(default= None)
    harness_model: Optional[str]= Field(default= None)
    harness_rescue_equipment_container: Optional[Harness_rescue_equipment_container] = Field(default= None, description="Where is the rescue equipment stored?")
    harness_back_protection: Optional[Harness_back_protection] = Field(default= None, description="Type of safety protection")
    harness_impact: Optional[Harness_impact] = Field(default= None, description="Impact of the pilot")

    reserve_parachute_manufacturer: Optional[str]= Field(default= None)
    reserve_parachute_model: Optional[str]= Field(default= None)
    reserve_parachute_size: Optional[str]= Field(default= None)
    reserve_parachute_controllable: Optional[Reserve_parachute_controllable] = Field(default= None)
    reserve_parachute_last_repack: Optional[int]= Field(default= None, description="months since last repack")

    accessories_helmet: Optional[Accessories_helmet]= Field(default= None)
    accessories_helmet_ce_966_tested: Optional[Accessories_helmet_ce_966_tested]= Field(default= None)
    accessories_ankle_high_shoes: Optional[Accessories_ankle_high_shoes]= Field(default= None)

    weather_wind: Optional[Weather_wind]= Field(default= None)
    weather_turbulences: Optional[Weather_turbulences]= Field(default= None, description="Intensity of turbulence")
    weather_thermic: Optional[Weather_thermic]= Field(default= None, description="Thermic conditions (upforce and downforce)")
    weather_special_conditions: Optional[Weather_special_conditions]= Field(default= None)

    flight_phase: Optional[Flight_phase]= Field(default= None, description="Flight phase at the time of the incident")
    start_type: Optional[Start_type]= Field(default= None)
    landing: Optional[Landing]= Field(default= None)
    rescue_tool: Optional[Rescue_tool]= Field(default= None, description="Has the rescue equipment been triggered?")
    event_sequence_triggered_at_m_agl_gnd: Optional[Event_sequence_triggered_at_m_agl_gnd]= Field(default= None, description="The height at which the rescue equipment was opened")
    rescue_equipment_opening: Optional[Rescue_equipment_opening]= Field(default= None, description="Was the rescue equipment triggering successful?")
    collision: Optional[Collision]= Field(default= None)

    paraglider_flight_behavior_f_e_f_c: Optional[Paraglider_flight_behavior_f_e_f_c]= Field(default= None, description="First unusual flight condition")
    paraglider_flight_behavior_triggered: Optional[Paraglider_flight_behavior_triggered]= Field(default= None, description="Height of the first unusual flight condition")
    paraglider_flight_behavior_follow_up: Optional[Paraglider_flight_behavior_follow_up]= Field(default= None, description="Follow-up reaction of the paraglider")

    pilot_error: Optional[Pilot_error]= Field(default= None, description="What best describes the pilot's error?")
    equipment_malfunction: Optional[Equipment_malfunction]= Field(default= None, description="note: (aircraft = paraglider.)")

    injuries_pilot: Optional[Injuries_pilot]= Field(default= None)
    injured_body_parts_pilot: Optional[Injured_body_parts_pilot]= Field(default= None, description="If injured only choose the most severe injury.")

    errors: ClassVar[dict] = {}
# region_rules
    @classmethod
    def save_error(cls, field, value):
        if field not in cls.errors:
            cls.errors[field] = []
        cls.errors[field].append(value)
    @field_validator("report_as")
    def validate_report_as(cls, v):
        if v in null_dict:
            v = "null"
        if v not in ["pilot", "flight_school_flight_instructor", "witness", "null", "unknown"]:
            cls.save_error("report_as", v)
        #     raise ValueError("For report_as you can only choose one of those values: "
        #                      "pilot, flight_school_flight_instructor, other, authority, witness, passenger, null")
        return v

    @field_validator("flight_equipment")
    def validate_flight_equipment(cls, v):
        if v in null_dict:
            v = "null"
        if v not in ["paraglider", "hang_glider", "fixed_wing", "speedflyer_miniwing_foot_launch",
                     "other", "null", "unknown"]:
            cls.save_error("flight_equipment", v)
            # raise ValueError(f"LLM suggested {v}, but it is not a valid value")
        return v

    @field_validator("flight_type")
    def validate_flight_type(cls, v):
        if v in null_dict:
            v = "null"
        if v not in ["cross_country_flight", "local_flight", "training_flight",
                     "assisted_flying_flight_travel_training", "competition_flight",
                     "passenger_flight", "acro_flight", "safety_training_flight", "null", "unknown"]:
            cls.save_error("flight_type", v)
            # raise ValueError(f"LLM suggested {v}, but it is not a valid value")
        return v

    @field_validator("gender")
    def validate_gender(cls, v):
        if v in null_dict:
            v = "null"
        if v not in ["m", "w", "d", "null", "unknown"]:
            cls.save_error("gender", v)
            # raise ValueError(f"LLM suggested {v}, but it is not a valid value")
        return v

    @field_validator("safety_training")
    def validate_safety_training(cls, v):
        if v in null_dict:
            v = "null"
        if v not in ["not_completed", "graduated_with_different_pattern",
                     "graduated_with_accident_pattern", "null", "unknown"]:
            cls.save_error("safety_training", v)
            # raise ValueError(f"LLM suggested {v}, but it is not a valid value")
        return v

    @field_validator("reserve_parachute_controllable")
    def validate_reserve_parachute_controllable(cls, v):
        if v in null_dict:
            v = "null"
        if v not in ["yes", "no", "null", "unknown"]:
            cls.save_error("reserve_parachute_controllable", v)
            # raise ValueError(f"LLM suggested {v}, but it is not a valid value")
        return v

    @field_validator("harness_rescue_equipment_container")
    def validate_harness_rescue_equipment_container(cls, v):
        if v in null_dict:
            v = "null"
        if v not in ["bottom", "site", "front", "back", "null", "unknown"]:
            cls.save_error("harness_rescue_equipment_container", v)
            # raise ValueError(f"LLM suggested {v}, but it is not a valid value")
        return v

    @field_validator("harness_back_protection")
    def validate_harness_back_protection(cls, v):
        if v in null_dict:
            v = "null"
        if v not in ["airbag", "foam_more_10", "foam_less_10", "foam_airbag", "none",
                     "null", "unknown"]:
            cls.save_error("harness_back_protection", v)
            # raise ValueError(f"LLM suggested {v}, but it is not a valid value")
        return v

    @field_validator("harness_impact")
    def validate_harness_impact(cls, v):
        if v in null_dict:
            v = "null"
        if v not in ["feet_ahead", "vertical", "lateral", "frontal", "back_ahead",
                     "null", "unknown"]:
            cls.save_error("harness_impact", v)
            # raise ValueError(f"LLM suggested {v}, but it is not a valid value")
        return v

    @field_validator("accessories_helmet")
    def validate_accessories_helmet(cls, v):
        if v in null_dict:
            v = "null"
        if v not in ["half_shelf_helmet", "integral_helmet", "null", "unknown"]:
            cls.save_error("accessories_helmet", v)
            # raise ValueError(f"LLM suggested {v}, but it is not a valid value")
        return v

    @field_validator("accessories_helmet_ce_966_tested")
    def validate_accessories_helmet_ce_966_tested(cls, v):
        if v in null_dict:
            v = "null"
        if v not in ["yes", "unknown", "no", "null", "unknown"]:
            cls.save_error("accessories_helmet_ce_966_tested", v)
            # raise ValueError(f"LLM suggested {v}, but it is not a valid value")
        return v

    @field_validator("accessories_ankle_high_shoes")
    def validate_accessories_ankle_high_shoes(cls, v):
        if v in null_dict:
            v = "null"
        if v not in ["yes", "unknown", "no", "null", "unknown"]:
            cls.save_error("accessories_ankle_high_shoes", v)
            # raise ValueError(f"LLM suggested {v}, but it is not a valid value")
        return v

    @field_validator("weather_wind")
    def validate_weather_wind(cls, v):
        if v in null_dict:
            v = "null"
        if v not in ["0_5_kmh", "5_10_kmh", "10_15_kmh", "15_20_kmh", "20_25_kmh", "25_30_kmh",
                     "30_35_kmh", "35_40_kmh", "40_45_kmh", "more_45_kmh", "null", "unknown"]:
            cls.save_error("weather_wind", v)
            # raise ValueError(f"LLM suggested {v}, but it is not a valid value")
        return v

    @field_validator("weather_turbulences")
    def validate_weather_turbulences(cls, v):
        if v in null_dict:
            return v
        if v not in ["non_turbulent", "slightly_turbulent", "moderately_turbulent", "strong_turbulent",
                     "very_strong_turbulent", "null", "unknown"]:
            cls.save_error("weather_turbulences", v)
            # raise ValueError(f"LLM suggested {v}, but it is not a valid value")
        return v

    @field_validator("weather_thermic")
    def validate_weather_thermic(cls, v):
        if v in null_dict:
            v = "null"
        if v not in ["slightly_1_ms", "moderately_3_ms", "strong_5_ms", "very_strong_more_5_ms",
                     "null", "unknown"]:
            cls.save_error("weather_thermic", v)
            # raise ValueError(f"LLM suggested {v}, but it is not a valid value")
        return v

    @field_validator("weather_special_conditions")
    def validate_weather_special_conditions(cls, v):
        if v in null_dict:
            v = "null"
        if v not in ["flight_in_clouds_fog", "foehn", "front_influence", "leeside", "rain_snow",
                     "thundery", "null", "unknown"]:
            cls.save_error("weather_special_conditions", v)
            # raise ValueError(f"LLM suggested {v}, but it is not a valid value")
        return v

    @field_validator("flight_phase")
    def validate_flight_phase(cls, v):
        if v in null_dict:
            v = "null"
        if v not in ["departure", "extreme_flight_acro_safety_training", "glide", "groundhandling",
                     "landing", "soaring", "start_run", "thermal_flight", "null", "unknown"]:
            cls.save_error("flight_phase", v)
            # raise ValueError(f"LLM suggested {v}, but it is not a valid value")
        return v

    @field_validator("start_type")
    def validate_start_type(cls, v):
        if v in null_dict:
            v = "null"
        if v not in ["slope_start", "ul_towing", "winch_tow_launch", "null", "unknown"]:
            cls.save_error("start_type", v)
            # raise ValueError(f"LLM suggested {v}, but it is not a valid value")
        return v

    @field_validator("landing")
    def validate_landing(cls, v):
        if v in null_dict:
            v = "null"
        if v not in ["building", "normal_landing", "off_field_landing", "other",
                     "power_line_ropeway_cable",
                     "top_landing", "tree_landing", "water_landing", "null", "unknown"]:
            cls.save_error("landing", v)
            # raise ValueError(f"LLM suggested {v}, but it is not a valid value")
        return v

    @field_validator("rescue_tool")
    def validate_rescue_tool(cls, v):
        if v in null_dict:
            v = "null"
        if v not in ["intentionally_triggered", "not_triggered", "unintentionally_triggered",
                     "null", "unknown"]:
            cls.save_error("rescue_tool", v)
            # raise ValueError(f"LLM suggested {v}, but it is not a valid value")
        return v

    @field_validator("event_sequence_triggered_at_m_agl_gnd")
    def validate_event_sequence_triggered_at_m_agl_gnd(cls, v):
        if v in null_dict:
            v = "null"
            return v
        if v not in ["less_20", "20_50", "50_70", "70_100", "100_250", "250_500", "more_500",
                     "null", "unknown"]:
            cls.save_error("event_sequence_triggered_at_m_agl_gnd", v)
            # raise ValueError(f"LLM suggested {v}, but it is not a valid value")
        return v

    @field_validator("rescue_equipment_opening")
    def validate_rescue_equipment_opening(cls, v):
        if v in null_dict:
            v = "null"
            return v
        if v not in ["not_successful_entanglement_with_umbrella_cap", "not_successful_other_reasons",
                     "not_successful_too_little_height", "successful", "null", "unknown"]:
            cls.save_error("rescue_equipment_opening", v)
            # raise ValueError(f"LLM suggested {v}, but it is not a valid value")
        return v

    @field_validator("collision")
    def validate_collision(cls, v):
        if v in null_dict:
            v = "null"
            return v
        if v not in ["collision_with_another_vehicle", "collision_with_obstacle",
                     "collision_with_paraglider_or_hang_glider", "null", "unknown"]:
            cls.save_error("collision", v)
            # raise ValueError(f"LLM suggested {v}, but it is not a valid value")
        return v

    @field_validator("paraglider_flight_behavior_f_e_f_c")
    def validate_paraglider_flight_behavior_f_e_f_c(cls, v):
        if v in null_dict:
            v = "null"
            return v
        if v not in ["unilateral_collapse", "spin", "not_specified_frontal_collapse", "fullstall",
                     "frontal_collapse", "got_caught", "stalled_flight", "steep_spiral",
                     "lines_unclear", "null", "unknown"]:
            cls.save_error("paraglider_flight_behavior_f_e_f_c", v)
            # raise ValueError(f"LLM suggested {v}, but it is not a valid value")
        return v

    @field_validator("paraglider_flight_behavior_triggered")
    def validate_paraglider_flight_behavior_triggered(cls, v):
        if v in null_dict:
            v = "null"
            return v
        if v not in ["less_5", "5_10", "10_20", "20_50", "50_70", "70_100", "100_250",
                     "250_500", "more_500", "null", "unknown"]:
            cls.save_error("paraglider_flight_behavior_triggered", v)
            # raise ValueError(f"LLM suggested {v}, but it is not a valid value")
        return v

    @field_validator("paraglider_flight_behavior_follow_up")
    @classmethod
    def validate_paraglider_flight_behavior_follow_up(cls, v):
        if v in null_dict:
            v = "null"
            return v
        if v not in ["fullstall", "frontal_collapse", "got_caught", "one_sided_collapse",
                     "spiral_got_caught", "spin", "stable_frontal_collapse", "stable_stalled_flight",
                     "stable_steep_spiral", "stalled_flight", "steep_spiral", "twist",
                     "null", "unknown"]:
            cls.save_error("paraglider_flight_behavior_follow_up", v)
            # raise ValueError(f"LLM suggested {v}, but it is not a valid value")
        return v

    @field_validator("pilot_error")
    def validate_pilot_error(cls, v):
        if v in null_dict:
            v = "null"
            return v
        if v not in ["affected", "control_error", "disregard_of_flight_rules", "exuberance",
                     "inadequate_airspace_observation", "inattention", "inexperience",
                     "miscalculation_weather", "miscalculation_wind_terrain",
                     "preflight_check_takeoff_check", "risk_taking", "spatial_misjudgement",
                     "traffic_density", "unsuitable_takeoff_landing_site", "null", "unknown"]:
            cls.save_error("pilot_error", v)
            # raise ValueError(f"LLM suggested {v}, but it is not a valid value")
        return v

    @field_validator("equipment_malfunction")
    def validate_equipment_malfunction(cls, v):
        if v in null_dict:
            v = "null"
            return v
        if v not in ["aircraft", "harness", "rescue_tool", "winch_towing_equipment",
                     "null", "unknown"]:
            cls.save_error("equipment_malfunction", v)
            # raise ValueError(f"LLM suggested {v}, but it is not a valid value")
        return v

    @field_validator("injuries_pilot")
    def validate_injuries_pilot(cls, v):
        if v in null_dict:
            v = "null"
            return v
        if v not in ["deadly_injured", "seriously_injured", "slightly_injured", "unharmed",
                     "null", "unknown"]:
            cls.save_error("injuries_pilot", v)
            # raise ValueError(f"LLM suggested {v}, but it is not a valid value")
        return v

    @field_validator("injured_body_parts_pilot")
    def validate_injured_body_parts_pilot(cls, v):
        if v in null_dict:
            v = "null"
            return v
        if v not in ["basin", "chest", "cervical_spine", "feet_legs", "hands_arms_shoulder",
                     "head", "lumbar_spine", "thoracic_spine", "internal_organs",
                     "null", "unknown"]:
            cls.save_error("injured_body_parts_pilot", v)
            # raise ValueError(f"LLM suggested {v}, but it is not a valid value")
        # if v != type(str):                                                                # Das hier funktioniert nicht. der input ist nie vom type string
        #     cls.save_error("injured_body_parts_pilot", v)
        #     # raise ValueError(f"LLM suggested {v}, but it is not a valid value")
        return v

# endregion

    class Config:
        arbitrary_types_allowed = True
        # Manchmal kam ein fehler bei nen attributen mit nof in der Kennung.
        # Attribut wurde nicht als int erkannt.
        # Diese Konfiguration erlaubt es, arbiträre Werte zu akzeptieren.

# def map_to_extract_accident_info(data: dict) -> extract_accident_info:
#     return extract_accident_info(**data)

#endregion
########################################################################################################################

#region ANNOTADED - with Literals (V3)
# Jason Liu sagt Lietarls tendenziell besser als Enums : https://www.wandb.courses/courses/take/steering-language-models/lessons/51843240-tip-2-arbitrary-properties

class extract_accident_info_literals(BaseModel):
    report_as: Optional[Literal["pilot", "flight_school_flight_instructor", "witness", "authority", "passenger", "other", "unknown"]] = Field(default= None, description="Who is reporting the incident?, e.g. I was doing .... = report_as: pilot")
    flight_equipment: Optional[Literal["paraglider", "hang_glider", "fixed_wing", "speedflyer_miniwing_foot_launch", "other", "unknown"]] = Field(default= None)
    flight_type: Optional[Literal["cross_country_flight", "local_flight", "training_flight", "assisted_flying_flight_travel_training", "competition_flight", "passenger_flight", "acro_flight", "safety_training_flight", "unknown"]] = Field(default= None)
    date: Optional[Union[str, int]] = None # DD/MM/YYYY or integer
    time: Optional[Union[str, int]] = None # HH:MM or integer
    location: Optional[str] = Field(default= None)
    country: Optional[str] = Field(default= None, description="Only Coutry code e.g. Chile = CL")

    gender: Optional[Literal["m", "w", "d", "unknown"]]= Field(default= None)

    type_of_flight_license: Optional[str]= Field(default= None)
    flies_since: Optional[int]= Field(default= None, description="Year when pilot had first flight")                 # YYYY
    total_nof: Optional[int]= Field(default= None, description="Total number of flights")
    total_nof_six_months: Optional[int]= Field(default= None, description="Total number of flight hours in the last six months")
    nof_accident_equipment: Optional[int]= Field(default= None, description="Number of flights with the accident equipment")
    safety_training: Optional[Literal["not_completed", "graduated_with_different_pattern", "graduated_with_accident_pattern", "unknown"]] = Field(default= None, description="Status of safety training")

    aircraft_manufacturer: Optional[str]= Field(default= None, description="Manufacturer of the paraglider")
    aircraft_model: Optional[str]= Field(default= None, description="Model of the paraglider")
    aircraft_size: Optional[str]= Field(default= None, description="Size of the paraglider")
    aircraft_classification: Optional[Literal["en_b", "en_a", "en_c", "unknown"]] = Field(default= None)
    aircraft_last_check: Optional[Union[str, int]] = None

    harness_manufacturer: Optional[str]= Field(default= None)
    harness_model: Optional[str]= Field(default= None)
    harness_rescue_equipment_container: Optional[Literal["bottom", "site", "front", "back", "unknown"]] = Field(default= None, description="Where is the rescue equipment stored?")
    harness_back_protection: Optional[Literal["airbag", "foam_more_10", "foam_less_10", "foam_airbag", "none", "unknown"]] = Field(default= None, description="Type of safety protection")
    harness_impact: Optional[Literal["feet_ahead", "vertical", "lateral", "frontal", "back_ahead", "unknown"]] = Field(default= None, description="If the pilot crashed, which part of the body crashed first?")

    reserve_parachute_manufacturer: Optional[str]= Field(default= None)
    reserve_parachute_model: Optional[str]= Field(default= None)
    reserve_parachute_size: Optional[str]= Field(default= None)
    reserve_parachute_controllable: Optional[Literal["yes", "no","unknown"]] = Field(default= None, description="Is the reserve parachute controllable?")
    reserve_parachute_last_repack: Optional[int]= Field(default= None, description="months since last repack")

    accessories_helmet: Optional[Literal["half_shelf_helmet", "integral_helmet", "unknown"]] = Field(default= None)
    accessories_helmet_ce_966_tested: Optional[Literal["yes", "no", "unknown"]] = Field(default= None)
    accessories_ankle_high_shoes: Optional[Literal["yes", "no", "unknown"]] = Field(default= None)

    weather_wind: Optional[Literal["0_5_kmh", "5_10_kmh", "10_15_kmh", "15_20_kmh", "20_25_kmh", "25_30_kmh", "30_35_kmh", "35_40_kmh", "40_45_kmh", "more_45_kmh", "unknown"]] = Field(default= None)
    weather_turbulences: Optional[Literal["non_turbulent", "slightly_turbulent", "moderately_turbulent", "strong_turbulent", "very_strong_turbulent", "unknown"]] = Field(default= None, description="Intensity of turbulence")
    weather_thermic: Optional[Literal["slightly_1_ms", "moderately_3_ms", "strong_5_ms", "very_strong_more_5_ms", "unknown"]] = Field(default= None, description="Thermic conditions (upforce and downforce)")
    weather_special_conditions: Optional[Literal["flight_in_clouds_fog", "foehn", "front_influence", "leeside", "rain_snow", "thundery", "unknown"]] = Field(default= None)

    flight_phase: Optional[Literal["departure", "extreme_flight_acro_safety_training", "glide", "groundhandling", "landing", "soaring", "start_run", "thermal_flight", "unknown"]] = Field(default= None, description="Flight phase at the time of the incident")
    start_type: Optional[Literal["slope_start", "ul_towing", "winch_tow_launch", "unknown"]] = Field(default= None)
    landing: Optional[Literal[ "other", "tree_landing","normal_landing", "building", "off_field_landing", "power_line_ropeway_cable", "top_landing", "water_landing", "unknown"]] = Field(default= None)
    rescue_tool: Optional[Literal["intentionally_triggered", "not_triggered", "unintentionally_triggered", "unknown"]] = Field(default= None, description="Has the rescue equipment been triggered?")
    event_sequence_triggered_at_m_agl_gnd: Optional[Literal["less_20", "20_50", "50_70", "70_100", "100_250", "250_500", "more_500", "unknown"]] = Field(default= None, description="The height at which the rescue equipment was opened")
    rescue_equipment_opening: Optional[Literal["not_successful_entanglement_with_umbrella_cap", "not_successful_other_reasons", "not_successful_too_little_height", "successful", "unknown"]] = Field(default= None, description="Was the rescue equipment triggering successful?")
    collision: Optional[Literal["collision_with_another_vehicle", "collision_with_obstacle", "collision_with_paraglider_or_hang_glider", "unknown"]] = Field(default= None)

    paraglider_flight_behavior_f_e_f_c: Optional[Literal["unilateral_collapse", "spin", "not_specified_frontal_collapse", "fullstall", "frontal_collapse", "got_caught", "stalled_flight", "steep_spiral", "lines_unclear", "unknown"]] = Field(default= None, description="First unusual flight condition")
    paraglider_flight_behavior_triggered: Optional[Literal["less_5", "5_10", "10_20", "20_50", "50_70", "70_100", "100_250", "250_500", "more_500", "unknown"]] = Field(default= None, description="Height of the first unusual flight condition")
    paraglider_flight_behavior_follow_up: Optional[Literal["fullstall", "frontal_collapse", "got_caught", "one_sided_collapse", "spiral_got_caught", "spin", "stable_frontal_collapse", "stable_stalled_flight", "stable_steep_spiral", "stalled_flight", "steep_spiral", "twist", "unknown"]] = Field(default= None, description="Follow-up reaction of the paraglider")

    pilot_error: Optional[Literal["affected", "control_error", "disregard_of_flight_rules", "exuberance", "inadequate_airspace_observation", "inattention", "inexperience", "miscalculation_weather", "miscalculation_wind_terrain", "preflight_check_takeoff_check", "risk_taking", "spatial_misjudgement", "traffic_density", "unsuitable_takeoff_landing_site", "unknown"]] = Field(default= None, description="What best describes the pilot's error?")
    equipment_malfunction: Optional[Literal["aircraft", "harness", "rescue_tool", "winch_towing_equipment", "unknown"]] = Field(default= None, description="This is only true if the cause of the accident was a malfunctioning paraglider(aircraft = paraglider.)")

    injuries_pilot: Optional[Literal["deadly_injured", "seriously_injured", "slightly_injured", "unharmed", "unknown"]] = Field(default= None)
    injured_body_parts_pilot: Optional[Literal["basin", "chest", "cervical_spine", "feet_legs", "hands_arms_shoulder", "head", "lumbar_spine", "thoracic_spine", "internal_organs", "unknown"]] = Field(default= None, description="If injured only choose the most severe injury.")

def map_to_extract_accident_info(data: dict) -> extract_accident_info_literals:
    return extract_accident_info_literals(**data)


#endregion
########################################################################################################################

#region Multi-Function-Call (V4)

class Extract_pilot_info(BaseModel):
    report_as: Optional[Report_as] = Field(default= None, description="Who is reporting the incident?, e.g. I was doing .... = report_as: pilot")
    flight_equipment: Optional[Flight_equipment] = Field(default= None)
    flight_type: Optional[Flight_type] = Field(default= None)
    age: Optional[int] = Field(default= None)
    starting_weight: Optional[int]= Field(default= None)
    gender: Optional[Gender] = Field(default= None)
    type_of_flight_license: Optional[str] = Field(default=None)
    flies_since: Optional[int] = Field(default=None, description="Year when pilot had first flight")  # YYYY
    total_nof: Optional[int] = Field(default=None, description="Total number of flights")
    total_nof_six_months: Optional[int] = Field(default=None,
                                                description="Total number of flight hours in the last six months")
    nof_accident_equipment: Optional[int] = Field(default=None,
                                                  description="Number of flights with the accident equipment")
    safety_training: Optional[Safety_training] = Field(default=None, description="Status of safety training")

class Extract_equipment_info(BaseModel):
    aircraft_manufacturer: Optional[str]= Field(default= None, description="Manufacturer of the paraglider")
    aircraft_model: Optional[str]= Field(default= None, description="Model of the paraglider")
    aircraft_size: Optional[str]= Field(default= None, description="Size of the paraglider")
    aircraft_classification: Optional[Aircraft_classification] = Field(default= None)
    aircraft_last_check: Optional[str]= Field(default= None)        # MM/YYYY

    harness_manufacturer: Optional[str]= Field(default= None)
    harness_model: Optional[str]= Field(default= None)
    harness_rescue_equipment_container: Optional[Harness_rescue_equipment_container] = Field(default= None, description="Where is the rescue equipment stored?")
    harness_back_protection: Optional[Harness_back_protection] = Field(default= None, description="Type of safety protection")
    harness_impact: Optional[Harness_impact] = Field(default= None, description="Impact of the pilot")

    reserve_parachute_manufacturer: Optional[str]= Field(default= None)
    reserve_parachute_model: Optional[str]= Field(default= None)
    reserve_parachute_size: Optional[str]= Field(default= None)
    reserve_parachute_controllable: Optional[Reserve_parachute_controllable] = Field(default= None)
    reserve_parachute_last_repack: Optional[int]= Field(default= None, description="months since last repack")

    accessories_helmet: Optional[Accessories_helmet]= Field(default= None)
    accessories_helmet_ce_966_tested: Optional[Accessories_helmet_ce_966_tested]= Field(default= None)
    accessories_ankle_high_shoes: Optional[Accessories_ankle_high_shoes]= Field(default= None)

class Extract_weather_info(BaseModel):
    weather_wind: Optional[Weather_wind]= Field(default= None)
    weather_turbulences: Optional[Weather_turbulences]= Field(default= None, description="Intensity of turbulence")
    weather_thermic: Optional[Weather_thermic]= Field(default= None, description="Thermic conditions (upforce and downforce)")
    weather_special_conditions: Optional[Weather_special_conditions]= Field(default= None)

class Extract_event_info(BaseModel):
    flight_phase: Optional[Flight_phase]= Field(default= None, description="Flight phase at the time of the incident")
    start_type: Optional[Start_type]= Field(default= None)
    landing: Optional[Landing]= Field(default= None)
    rescue_tool: Optional[Rescue_tool]= Field(default= None, description="Has the rescue equipment been triggered?")
    event_sequence_triggered_at_m_agl_gnd: Optional[Event_sequence_triggered_at_m_agl_gnd]= Field(default= None, description="If the rescue equipment was opened at which height?")
    rescue_equipment_opening: Optional[Rescue_equipment_opening]= Field(default= None, description="If the rescue equipment was opened, was it successful?")
    collision: Optional[Collision]= Field(default= None)

    paraglider_flight_behavior_f_e_f_c: Optional[Paraglider_flight_behavior_f_e_f_c]= Field(default= None, description="If given, what was the first unusual flight condition.")
    paraglider_flight_behavior_triggered: Optional[Paraglider_flight_behavior_triggered]= Field(default= None, description="If given, what was the height of the first unusual flight condition")
    paraglider_flight_behavior_follow_up: Optional[Paraglider_flight_behavior_follow_up]= Field(default= None, description="If given, what was the follow-up reaction of the paraglider after the first unusual flight condition?")

class Extract_malfunction_consequences_info(BaseModel):
    pilot_error: Optional[Pilot_error]= Field(default= None, description="What best describes the pilot's error?")
    equipment_malfunction: Optional[Equipment_malfunction]= Field(default= None, description="note: (aircraft = paraglider.)")

    injuries_pilot: Optional[Injuries_pilot]= Field(default= None)
    injured_body_parts_pilot: Optional[Injured_body_parts_pilot]= Field(default= None, description="If injured only choose the most severe injury.")

#endregion
#########################################################################################################################

# region Multi-Function-Call with literals (V5)
# class Extract_pilot_info(BaseModel):
#     report_as: Optional[
#         Literal["pilot", "flight_school_flight_instructor", "witness", "authority", "passenger", "other"]] = Field(
#         default=None, description="Who is reporting the incident?, e.g. I was doing .... = report_as: pilot")
#     flight_equipment: Optional[
#         Literal["paraglider", "hang_glider", "fixed_wing", "speedflyer_miniwing_foot_launch", "other"]] = Field(
#         default=None)
#     flight_type: Optional[Literal[
#         "cross_country_flight", "local_flight", "training_flight", "assisted_flying_flight_travel_training", "competition_flight", "passenger_flight", "acro_flight", "safety_training_flight"]] = Field(
#         default=None)
#     date: Optional[Union[str, int]] = None  # DD/MM/YYYY or integer
#     time: Optional[Union[str, int]] = None  # HH:MM or integer
#     location: Optional[str] = Field(default=None)
#     country: Optional[str] = Field(default=None, description="Only Coutry code e.g. Chile = CL")
#
#     gender: Optional[Literal["m", "w", "d"]] = Field(default=None)
#
#     type_of_flight_license: Optional[str] = Field(default=None)
#     flies_since: Optional[int] = Field(default=None, description="Year when pilot had first flight")  # YYYY
#     total_nof: Optional[int] = Field(default=None, description="Total number of flights")
#     total_nof_six_months: Optional[int] = Field(default=None,
#                                                 description="Total number of flight hours in the last six months")
#     nof_accident_equipment: Optional[int] = Field(default=None,
#                                                   description="Number of flights with the accident equipment")
#     safety_training: Optional[
#         Literal["not_completed", "graduated_with_different_pattern", "graduated_with_accident_pattern"]] = Field(
#         default=None, description="Status of safety training")
#
#
# class Extract_equipment_info(BaseModel):
#     aircraft_manufacturer: Optional[str]= Field(default= None, description="Manufacturer of the paraglider")
#     aircraft_model: Optional[str]= Field(default= None, description="Model of the paraglider")
#     aircraft_size: Optional[str]= Field(default= None, description="Size of the paraglider")
#     aircraft_classification: Optional[Literal["en_b", "en_a", "en_c"]] = Field(default= None)
#     aircraft_last_check: Optional[Union[str, int]] = None
#
#     harness_manufacturer: Optional[str]= Field(default= None)
#     harness_model: Optional[str]= Field(default= None)
#     harness_rescue_equipment_container: Optional[Literal["bottom", "site", "front", "back"]] = Field(default= None, description="Where is the rescue equipment stored?")
#     harness_back_protection: Optional[Literal["airbag", "foam_more_10", "foam_less_10", "foam_airbag", "none"]] = Field(default= None, description="Type of safety protection")
#     harness_impact: Optional[Literal["feet_ahead", "vertical", "lateral", "frontal", "back_ahead"]] = Field(default= None, description="If the pilot crashed, which part of the body crashed first?")
#
#     reserve_parachute_manufacturer: Optional[str]= Field(default= None)
#     reserve_parachute_model: Optional[str]= Field(default= None)
#     reserve_parachute_size: Optional[str]= Field(default= None)
#     reserve_parachute_controllable: Optional[Literal["yes", "no"]] = Field(default= None, description="Is the reserve parachute controllable?")
#     reserve_parachute_last_repack: Optional[int]= Field(default= None, description="months since last repack")
#
#     accessories_helmet: Optional[Literal["half_shelf_helmet", "integral_helmet"]] = Field(default= None)
#     accessories_helmet_ce_966_tested: Optional[Literal["yes", "no"]] = Field(default= None)
#     accessories_ankle_high_shoes: Optional[Literal["yes", "no"]] = Field(default= None)
#
# class Extract_weather_info(BaseModel):
#     weather_wind: Optional[Literal["0_5_kmh", "5_10_kmh", "10_15_kmh", "15_20_kmh", "20_25_kmh", "25_30_kmh", "30_35_kmh", "35_40_kmh", "40_45_kmh", "more_45_kmh"]] = Field(default= None)
#     weather_turbulences: Optional[Literal["non_turbulent", "slightly_turbulent", "moderately_turbulent", "strong_turbulent", "very_strong_turbulent"]] = Field(default= None, description="Intensity of turbulence")
#     weather_thermic: Optional[Literal["slightly_1_ms", "moderately_3_ms", "strong_5_ms", "very_strong_more_5_ms"]] = Field(default= None, description="Thermic conditions (upforce and downforce)")
#     weather_special_conditions: Optional[Literal["flight_in_clouds_fog", "foehn", "front_influence", "leeside", "rain_snow", "thundery"]] = Field(default= None)
#
# class Extract_event_info(BaseModel):
#     flight_phase: Optional[Literal["departure", "extreme_flight_acro_safety_training", "glide", "groundhandling", "landing", "soaring", "start_run", "thermal_flight"]] = Field(default= None, description="Flight phase at the time of the incident")
#     start_type: Optional[Literal["slope_start", "ul_towing", "winch_tow_launch"]] = Field(default= None)
#     landing: Optional[Literal[ "other", "tree_landing","normal_landing", "building", "off_field_landing", "power_line_ropeway_cable", "top_landing", "water_landing"]] = Field(default= None)
#     rescue_tool: Optional[Literal["intentionally_triggered", "not_triggered", "unintentionally_triggered"]] = Field(default= None, description="Has the rescue equipment been triggered?")
#     event_sequence_triggered_at_m_agl_gnd: Optional[Literal["less_20", "20_50", "50_70", "70_100", "100_250", "250_500", "more_500"]] = Field(default= None, description="The height at which the rescue equipment was opened")
#     rescue_equipment_opening: Optional[Literal["not_successful_entanglement_with_umbrella_cap", "not_successful_other_reasons", "not_successful_too_little_height", "successful"]] = Field(default= None, description="Was the rescue equipment triggering successful?")
#     collision: Optional[Literal["collision_with_another_vehicle", "collision_with_obstacle", "collision_with_paraglider_or_hang_glider"]] = Field(default= None)
#
#     paraglider_flight_behavior_f_e_f_c: Optional[Literal["unilateral_collapse", "spin", "not_specified_frontal_collapse", "fullstall", "frontal_collapse", "got_caught", "stalled_flight", "steep_spiral", "lines_unclear"]] = Field(default= None, description="First unusual flight condition")
#     paraglider_flight_behavior_triggered: Optional[Literal["less_5", "5_10", "10_20", "20_50", "50_70", "70_100", "100_250", "250_500", "more_500"]] = Field(default= None, description="Height of the first unusual flight condition")
#     paraglider_flight_behavior_follow_up: Optional[Literal["fullstall", "frontal_collapse", "got_caught", "one_sided_collapse", "spiral_got_caught", "spin", "stable_frontal_collapse", "stable_stalled_flight", "stable_steep_spiral", "stalled_flight", "steep_spiral", "twist"]] = Field(default= None, description="Follow-up reaction of the paraglider")
#
# class Extract_malfunction_consequences_info(BaseModel):
#     pilot_error: Optional[Literal["affected", "control_error", "disregard_of_flight_rules", "exuberance", "inadequate_airspace_observation", "inattention", "inexperience", "miscalculation_weather", "miscalculation_wind_terrain", "preflight_check_takeoff_check", "risk_taking", "spatial_misjudgement", "traffic_density", "unsuitable_takeoff_landing_site"]] = Field(default= None, description="What best describes the pilot's error?")
#     equipment_malfunction: Optional[Literal["aircraft", "harness", "rescue_tool", "winch_towing_equipment"]] = Field(default= None, description="This is only true if the cause of the accident was a malfunctioning paraglider(aircraft = paraglider.)")
#
#     injuries_pilot: Optional[Literal["deadly_injured", "seriously_injured", "slightly_injured", "unharmed"]] = Field(default= None)
#     injured_body_parts_pilot: Optional[Literal["basin", "chest", "cervical_spine", "feet_legs", "hands_arms_shoulder", "head", "lumbar_spine", "thoracic_spine", "internal_organs"]] = Field(default= None, description="If injured only choose the most severe injury.")
#endregion
########################################################################################################################

if __name__ == "__main__":
    # try:
    #     extract_accident_info(report_as="witness", pilot_error="Json")
    # except Exception as e:
    #     print(e)


    try:
        print("erster Try: ")
        extract_accident_info(report_as="pilot", pilot_error="test")
        print("zweiter Try: ")
        extract_accident_info(report_as="pilot", pilot_error="affected")
        print("zweiter Try wurde ausgeführt und die Fehler aus 1 dokumentiert ")
    except Exception as e:
        print("kacke der Text sollte nicht angezeigt werden")


    #print(json.dumps(reports_new.model_json_schema(), indent=2))