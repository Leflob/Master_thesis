import time
import streamlit as st
import csv

# eigene Module
import connection
import comperator


# Extact additional information to display
def get_accident_report(id):
    # Hier solltest du deine eigene Implementierung der SQL-Verbindung einsetzen
    x = connection.get_accident_report(id)
    if x:
        return x
    else:
        return None

# Initialisieren des Session State
def init_session_state():
    return {"selected_id": None, "analysis_result": None, "switch_state": False, "accident_report": None,
            "llm_result_df": ''}


def count_answers(data):
    accept_count = 0
    wrong_value_count = 0

    edited_rows = st.session_state[f"{data}"]["edited_rows"]

    for row in edited_rows.values():
        if "accept" in row and row["accept"]:
            accept_count += 1
        if "wrong_value" in row and row["wrong_value"]:
            wrong_value_count += 1

    return accept_count, wrong_value_count

# Überprüfen, ob Session State bereits initialisiert wurde
if "session_state" not in st.session_state:
    st.session_state.session_state = init_session_state()


# Debugging
# "session_state: ", st.session_state

st.set_page_config(layout="wide")
# Streamlit App
st.title("Unfallbericht Analyse")

# Sidebar für ID-Eingabe und Suche
st.sidebar.header("Unfallbericht suchen")
selected_id = st.sidebar.number_input("Bitte ID eingeben:", min_value=1, step=1)
if st.sidebar.button("Suchen"):
    st.session_state.session_state["selected_id"] = selected_id


# Hauptbereich mit Informationen und Toggle-Button
if st.session_state.session_state.get("selected_id") is not None:

    # 1. Abrufen der Zusatzinformationen um diese für den Nutzer anzuzeigen
    report_id = st.session_state.session_state.get("selected_id")
    st.session_state.session_state["accident_report"] = get_accident_report(report_id)

    # 2. Wenn Unfallbericht zur ID existiert, dann zeige die Zusatzinformationen an
    if st.session_state.session_state["accident_report"] is not None:
        st.markdown(f"<span style=\"font-size:1.5em;\">Zusatzinformationen für Unfallbericht *{report_id}*</span>",
                    unsafe_allow_html=True)
        st.write(st.session_state.session_state["accident_report"])

        # Analyse-Button nur anzeigen, wenn ein gültiger Unfallbericht vorhanden ist
        analyse = st.button("Analyse")
        if "analyse" not in st.session_state.session_state:
            st.session_state.session_state["analyse"] = False

        # Wenn Analyse-Button gedrückt wurde, oder im laufenden run schoneinmal gedrückt wurde
        if analyse or st.session_state.session_state["analyse"]:

            # Wenn bisher KEIN API Call gemacht wurde:
            if "llm_result" not in st.session_state.session_state and st.session_state.session_state["switch_state"] == False:
                # Wenn nein, dann führe den Api-Call und die JSON-comparison aus
                changedData, addedData, count_changed, count_added = comperator.compare_json_streamlit(selected_id)

                # Speichere beide Tabellen im globalen Session State
                st.session_state["llm_result_changedData"] = changedData
                st.session_state["llm_result_addedData"] = addedData

                # Speichere die Anzahl der geänderten und hinzugefügten Einträge
                st.session_state["count_changed"] = count_changed
                st.session_state["count_added"] = count_added


                # Setze den switch_state auf True, damit der Api-Call nicht nochmal ausgeführt wird
                st.session_state.session_state["analyse"] = True
                st.session_state.session_state["switch_state"] = True


            # Wenn EIN API Call gemacht wurde:
            if "llm_result_df" in st.session_state.session_state and st.session_state.session_state["switch_state"] == True:

                #Zeige die Egebnisse in einem DataFrame an
                st.write('# Vorgeschlagenen Änderungen des LLM:')



                # Kleiner header für die erste Tabelle
                st.markdown(f"*Änderungsvorschläge für bestehende Datenbank-Einträge:*")
                st.data_editor(
                    st.session_state["llm_result_changedData"], key="changedData",
                    column_config={
                        "accept": st.column_config.CheckboxColumn(     #Checkboxen direkt ins Dataframe integriert
                            "accept new value?",
                            help="Check if you want to accept the new value",
                            default=False
                        ),
                        "wrong_value": st.column_config.CheckboxColumn(
                            "wrong value?",
                            help="Check if the suggested value is wrong (in terms of content)",
                            default=False
                        )

                    },
                    hide_index=True,
                )

                # Kleiner header für die zweite Tabelle
                st.markdown(f"*Noch nicht strukturiert erfasste Attribute:*")
                st.data_editor(
                    st.session_state["llm_result_addedData"], key="addedData",
                    column_config={
                        "accept": st.column_config.CheckboxColumn(     #Checkboxen direkt ins Dataframe integriert
                            "accept new entry?",
                            help="Check if you want to accept the new value",
                            default=False
                        ),
                        "wrong_value": st.column_config.CheckboxColumn(
                            "wrong value?",
                            help="Check if the suggested value is wrong (in terms of content)",
                            default=False
                        )
                    },
                    hide_index=True,
                )

                # API-Call wurde gemacht, daher wird auch Button zum Speichern angezeigt
                save_and_exit = st.button("Save Changes")


                if save_and_exit:
                    # Speichere statistiken in CSV
                    user_accept, user_wrong_value = count_answers("changedData")
                    user_accept_added, user_wrong_value_added = count_answers("addedData")

                    with open('Output/eval.csv', 'a', newline="") as data:
                        writer = csv.writer(data)
                        writer.writerow([report_id, st.session_state["count_changed"],
                                         user_accept, user_wrong_value, st.session_state["count_added"],
                                        user_accept_added, user_wrong_value_added])
            # report_id, change_suggestions, changes_accepted, classified_wrong_value,
            # add_suggestions, add_acceptance, add_wrong_value


                # Lösche alle Session States, damit die App neu geladen wird
                    for key in st.session_state.keys():
                        del st.session_state[key]

                    st.balloons()
                    time.sleep(1)
                    # Lade die Anwendung neu
                    st.rerun()

    # Hier noch das else, falls kein Unfallbericht zur ID gefunden wurde
    else:
        st.markdown(f" Der Unfall mit der :red[**ID {report_id}**] existiert nicht oder hat keine zusätzlichen "
                     f"Informationen in der Datenbank.")

# End of code