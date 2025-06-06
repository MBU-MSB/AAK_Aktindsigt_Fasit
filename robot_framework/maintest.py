"""Test hele eller dele af robotprocessen"""
import os
from OpenOrchestrator.orchestrator_connection.connection import OrchestratorConnection
from msb_rpa.logins import fasit_login
from msb_rpa.generelt import use_retry_logic
from robot_framework.Processer.fasit_api_calls import get_journalnotes_for_citizenid
from robot_framework.Processer.fasit_api_calls import get_attached_file

# ###TEST TEST TEST####
connection_string = os.environ.get("OpenOrchestratorConnString")
crypto_key = os.environ.get("OpenOrchestratorKey")
orchestrator_connection = OrchestratorConnection(process_name="000_00_Eksempel", connection_string=connection_string, crypto_key=crypto_key, process_arguments="none")
# ###TEST TEST TEST####

gemt_credential = orchestrator_connection.get_credential("021_Fleksjob_Sagshåndtering_Fasit")
bearer_token = use_retry_logic(fasit_login, username=gemt_credential.username, password=gemt_credential.password, drivertype='chrome_wire')

test_dict = {"CPR":"0209862158","Citizenid":"6AEA3742-D12D-E611-80F6-00155D177806","Startdato":"2015-01-01","Slutdato":"2025-06-01","Serial":"10"}

attachments = get_journalnotes_for_citizenid(test_dict["Citizenid"], bearer_token, test_dict["Startdato"], test_dict["Slutdato"])
for attachment in attachments:
    get_attached_file(test_dict, attachment, bearer_token)

print("Stop her")
