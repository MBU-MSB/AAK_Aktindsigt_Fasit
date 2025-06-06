"""This module contains the main process of the robot."""
import json
from msb_rpa.generelt import sql_insert_result
from OpenOrchestrator.orchestrator_connection.connection import OrchestratorConnection
from robot_framework import config
from robot_framework.Processer.fasit_api_calls import get_journalnotes_for_citizenid
from robot_framework.Processer.fasit_api_calls import get_attached_file


def process(orchestrator_connection: OrchestratorConnection, queue_element, bearer_token: str) -> None:
    """Do the primary process of the robot."""
    orchestrator_connection.log_trace("Running process.")
    # Gemmer data kolonnen som en dictionary, hvis du har behov for at hente data derfra.
    queue_data_string = queue_element.data
    rpa_id = str(queue_element.reference)
    executionid = str(queue_element.id)
    # Konverterer kun data kolonnen til dictionary, hvis den indeholder data.
    if queue_data_string:
        queue_dict = json.loads(queue_data_string)
    else:
        queue_dict = ''
    # Hent RPA_ID og ExecutionID fra køelementet

    sql_connection = orchestrator_connection.get_credential("sql_connection_string").password

    sql_insert_result(rpa_id, executionid, '1', "{}", sql_connection, config.RESULT_TABLE)

    orchestrator_connection.log_trace("Start: get_journalnotes_for_citizenid, to get journalfiles for the citizen")
    attachments = get_journalnotes_for_citizenid(queue_dict["Citizenid"], bearer_token, queue_dict["Startdato"], queue_dict["Slutdato"])
    orchestrator_connection.log_trace("Slut: get_journalnotes_for_citizenid")

    orchestrator_connection.log_trace("Start: get_attached_file, to get download the filecontent")
    for attachment in attachments:
        get_attached_file(queue_dict, attachment, bearer_token)
    orchestrator_connection.log_trace("Slut: get_attached_file")

    sql_insert_result(rpa_id, executionid, '2', "{}", sql_connection, config.RESULT_TABLE)
