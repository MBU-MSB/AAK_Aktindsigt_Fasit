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

attachment_ids = get_journalnotes_for_citizenid('6791B45D-EA2D-E611-80F6-00155D177806', bearer_token, '2015-01-01', '2024-01-01')
for attachment_id in attachment_ids:
    get_attached_file('6791B45D-EA2D-E611-80F6-00155D177806', attachment_id, bearer_token)

print("Stop her")
