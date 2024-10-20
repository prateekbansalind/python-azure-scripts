import os
import argparse
import fnmatch
from azure.identity import DefaultAzureCredential
from azure.mgmt.applicationinsights import ApplicationInsightsManagementClient

# Function to toggle the availability test (enable/disable based on the action parameter)
def toggle_availability_test(appinsights_client, resource_group, test_name, action):
    try:
        # Fetch the current availability test details
        availability_test = appinsights_client.web_tests.get(resource_group, test_name)
        
        if action == 'enable':
            # Enable the availability test if it's currently disabled
            if not availability_test.enabled:
                availability_test.enabled = True
                appinsights_client.web_tests.create_or_update(resource_group, test_name, availability_test)
                print(f"Availability test '{test_name}' has been successfully enabled.")
            else:
                print(f"Availability test '{test_name}' is already enabled.")
        elif action == 'disable':
            # Disable the availability test if it's currently enabled
            if availability_test.enabled:
                availability_test.enabled = False
                appinsights_client.web_tests.create_or_update(resource_group, test_name, availability_test)
                print(f"Availability test '{test_name}' has been successfully disabled.")
            else:
                print(f"Availability test '{test_name}' is already disabled.")
    except Exception as e:
        print(f"Error processing availability test '{test_name}': {e}")

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Enable or disable availability tests based on wildcards.")
    parser.add_argument('action', choices=['enable', 'disable'], help="Action to perform: 'enable' or 'disable'")
    parser.add_argument('wildcard_file', help="File containing wildcard patterns (one per line) to match availability test names.")
    parser.add_argument('resource_group', help="The resource group to search for availability tests.")
    
    args = parser.parse_args()

    # Check if wildcard file exists and is not empty
    if not os.path.exists(args.wildcard_file):
        print(f"Error: Wildcard file '{args.wildcard_file}' does not exist.")
        return

    # Read wildcard patterns from the file
    try:
        with open(args.wildcard_file, 'r') as file:
            wildcards = [line.strip().lower() for line in file.readlines() if line.strip()]
    except Exception as e:
        print(f"Error reading wildcard file: {e}")
        return

    if not wildcards:
        print(f"Error: No valid wildcards found in '{args.wildcard_file}'.")
        return

    # Set your Azure subscription ID
    SUBSCRIPTION_ID = "171af07e-2ca7-472d-bc77-e33c8d720c4b"  # The provided subscription ID

    # Authenticate using DefaultAzureCredential
    credentials = DefaultAzureCredential()
    appinsights_client = ApplicationInsightsManagementClient(credentials, SUBSCRIPTION_ID)

    # List all availability tests in the resource group
    try:
        availability_tests = appinsights_client.web_tests.list_by_resource_group(args.resource_group)
    except Exception as e:
        print(f"Error fetching availability tests for resource group '{args.resource_group}': {e}")
        return
    
    # Iterate over each availability test and check if the name matches any of the wildcards
    for test in availability_tests:
        for wildcard in wildcards:
            if fnmatch.fnmatchcase(test.name.lower(), f"*{wildcard}*"):  # Case-insensitive wildcard match
                print(f"Processing availability test: {test.name} (matched wildcard: {wildcard})")
                toggle_availability_test(appinsights_client, args.resource_group, test.name, args.action)

if __name__ == '__main__':
    main()
