import os
import argparse
import fnmatch
from azure.identity import DefaultAzureCredential
from azure.mgmt.monitor import MonitorManagementClient

# Function to toggle the alert (enable/disable based on the action parameter)
def toggle_metric_alert(monitor_client, resource_group, alert_name, action):
    try:
        # Fetch the current alert details
        alert = monitor_client.metric_alerts.get(resource_group, alert_name)
        
        if action == 'enable':
            # Enable the alert if it's currently disabled
            if not alert.enabled:
                alert.enabled = True
                monitor_client.metric_alerts.create_or_update(resource_group, alert_name, alert)
                print(f"Metric alert '{alert_name}' has been successfully enabled.")
            else:
                print(f"Metric alert '{alert_name}' is already enabled.")
        elif action == 'disable':
            # Disable the alert if it's currently enabled
            if alert.enabled:
                alert.enabled = False
                monitor_client.metric_alerts.create_or_update(resource_group, alert_name, alert)
                print(f"Metric alert '{alert_name}' has been successfully disabled.")
            else:
                print(f"Metric alert '{alert_name}' is already disabled.")
    except Exception as e:
        print(f"Error processing metric alert '{alert_name}': {e}")

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Enable or disable metric alerts based on wildcards.")
    parser.add_argument('action', choices=['enable', 'disable'], help="Action to perform: 'enable' or 'disable'")
    parser.add_argument('wildcard_file', help="File containing wildcard patterns (one per line) to match alert names.")
    parser.add_argument('resource_group', help="The resource group to search for metric alerts.")
    
    args = parser.parse_args()

    # Read wildcard patterns from the file
    try:
        with open(args.wildcard_file, 'r') as file:
            wildcards = [line.strip().lower() for line in file.readlines()]
    except Exception as e:
        print(f"Error reading wildcard file: {e}")
        return

    # Set your Azure subscription ID
    SUBSCRIPTION_ID = "171af07e-2ca7-472d-bc77-e33c8d720c4b"  # Example valid subscription ID

    # Authenticate using DefaultAzureCredential
    credentials = DefaultAzureCredential()
    monitor_client = MonitorManagementClient(credentials, SUBSCRIPTION_ID)

    # List all metric alerts in the resource group
    metric_alerts = monitor_client.metric_alerts.list_by_resource_group(args.resource_group)
    
    # Iterate over each alert and check if the name matches any of the wildcards
    for alert in metric_alerts:
        for wildcard in wildcards:
            if fnmatch.fnmatchcase(alert.name.lower(), f"*{wildcard}*"):  # Case-insensitive wildcard match
                print(f"Processing metric alert: {alert.name} (matched wildcard: {wildcard})")
                toggle_metric_alert(monitor_client, args.resource_group, alert.name, args.action)

if __name__ == '__main__':
    main()
