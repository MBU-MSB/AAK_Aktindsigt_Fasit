"""This module handles resetting the state of the computer so the robot can work with a clean slate."""
from OpenOrchestrator.orchestrator_connection.connection import OrchestratorConnection
from msb_rpa.generelt import use_retry_logic
from msb_rpa.logins import fasit_login


def reset(orchestrator_connection: OrchestratorConnection) -> None:
    """Clean up, close/kill all programs and start them again. """
    orchestrator_connection.log_trace("Resetting.")
    kill_all(orchestrator_connection)
    open_all(orchestrator_connection)


def kill_all(orchestrator_connection: OrchestratorConnection) -> None:
    """Forcefully close all applications used by the robot."""
    orchestrator_connection.log_trace("Killing all applications.")
    orchestrator_connection.log_trace("Killed all applications succesfully")


def open_all(orchestrator_connection: OrchestratorConnection) -> None:
    """Open all programs used by the robot."""
    orchestrator_connection.log_trace("Opening all applications.")
    # gemt_credential = orchestrator_connection.get_credential("000_Eksempel_Opus")
    # opus_login(username=gemt_credential.username,password=gemt_credential.password)
    orchestrator_connection.log_trace("Opened application succesfully")
