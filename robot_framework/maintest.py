"""Test hele eller dele af robotprocessen"""
import os
# import json
from OpenOrchestrator.orchestrator_connection.connection import OrchestratorConnection
# from robot_framework import config

# ###TEST TEST TEST####
connection_string = os.environ.get("OpenOrchestratorConnString")
crypto_key = os.environ.get("OpenOrchestratorKey")
orchestrator_connection = OrchestratorConnection(process_name="000_00_Eksempel", connection_string=connection_string, crypto_key=crypto_key, process_arguments="none")
# ###TEST TEST TEST####

gemt_credential = orchestrator_connection.get_credential("000_Eksempel")
# login

print("Stop her")
