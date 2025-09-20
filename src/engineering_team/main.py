#!/usr/bin/env python
import sys
import warnings
import os
from datetime import datetime

from engineering_team.crew import EngineeringTeam

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Create output directory if it doesn't exist
os.makedirs('output', exist_ok=True)

# requirements = """
# A simple account management system for a trading simulation platform.
# The system should allow users to create an account, deposit funds, and withdraw funds.
# The system should allow users to record that they have bought or sold shares, providing a quantity.
# The system should calculate the total value of the user's portfolio, and the profit or loss from the initial deposit.
# The system should be able to report the holdings of the user at any point in time.
# The system should be able to report the profit or loss of the user at any point in time.
# The system should be able to list the transactions that the user has made over time.
# The system should prevent the user from withdrawing funds that would leave them with a negative balance, or
#  from buying more shares than they can afford, or selling shares that they don't have.
#  The system has access to a function get_share_price(symbol) which returns the current price of a share, and includes a test implementation that returns fixed prices for AAPL, TSLA, GOOGL.
# """
# module_name = "accounts.py"
# class_name = "Account"

requirements = """
A simple account management system for a trading simulation platform.
The system should allow users to create an account, deposit funds, and withdraw funds.
The system should allow users to record that they have bought or sold shares, providing a quantity.
The system should calculate the total value of the user's portfolio, and the profit or loss from the initial deposit.
The system should be able to report the holdings of the user at any point in time.
The system should be able to report the profit or loss of the user at any point in time.
The system should be able to list the transactions that the user has made over time.
The system should prevent the user from withdrawing funds that would leave them with a negative balance, or
 from buying more shares than they can afford, or selling shares that they don't have.
 The system has access to a function get_share_price(symbol) which returns the current price of a share, and includes a test implementation that returns fixed prices for AAPL, TSLA, GOOGL.
"""
module_name = "accounts.py"
class_name = "Account"

# A simple digital and voice channel based customer support management system, simulating a SaaS based Contact Center platform.
# The system should have 4 types of users: superadmins, admins, supervisors and agents.
# The system should allow choosing digital vs voice as the channel for the agents. And the agents can choose both if needed.

# superadmins requirements:
# The system should allow superadmins to create 1 or more accounts.
# The system should allow superadmins to add admins to the accounts.

# admins requirements:
# The system should allow admins to create teams and assign a supervisor to the team. 

# supervisors requirements:
# The system should allow supervisors to add agents to the teams.

# agent requirements:
# The system should allow agent to accept contact to support from digital or voice channel, or both, based on their settings.
# The system should allow agent to complete the support with the contact, which will remove the contact from the active supporting queue of the agent.
# The system should calculate the total number of active contact the agent is supporting.
# The system should not allow more than 3 active contact of type digital. 
# The system should not allow more than 1 active contact of type voice. 
# The system should be able to report the total time spent with a contact.
# The system should be able to list the contacts that the agent has supported over time.
# """
# module_name = "ccaas.py"
# class_name = "Ccaas"

def run():
    """
    Run the research crew.
    """
    inputs = {
        'requirements': requirements,
        'module_name': module_name,
        'class_name': class_name
    }

    # Create and run the crew
    result = EngineeringTeam().crew().kickoff(inputs=inputs)


if __name__ == "__main__":
    run()