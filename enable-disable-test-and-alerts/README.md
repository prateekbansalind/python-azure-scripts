# README for Python Scripts: Manage Alerts and Availability Tests

## Overview
This repository contains two Python scripts to manage Azure metric alerts and availability tests based on wildcard patterns. The scripts can enable or disable these resources based on wildcard names specified in a text file.

- **`manage_alerts.py`**: This script enables or disables Azure metric alerts based on wildcards specified in a file.
- **`manage_availability_tests.py`**: This script enables or disables Azure Application Insights availability tests based on wildcards specified in a file.

## Prerequisites

1. **Python 3.x**: Ensure Python is installed on your system.
2. **Azure CLI**: Ensure you have the Azure CLI installed and authenticated with your subscription.
3. **PIP (Python Package Manager)**: Ensure `pip` is installed to install necessary Python modules.
4. **Azure Subscription**: You need an Azure subscription and appropriate permissions to manage resources.

## Installation

### Step 1: Install required Python modules
The scripts use the Azure SDK for Python, so you'll need to install the following modules.

```bash
pip install azure-identity
pip install azure-mgmt-monitor
pip install azure-mgmt-applicationinsights
```

### Step 2: Set environment variables
Make sure to set your `AZURE_SUBSCRIPTION_ID` environment variable.

```bash
export AZURE_SUBSCRIPTION_ID="your-subscription-id"
```

Alternatively, you can modify the `SUBSCRIPTION_ID` variable directly in the scripts to set your subscription ID.

## Usage

### **1. Manage Azure Metric Alerts (`manage_alerts.py`)**
This script enables or disables Azure metric alerts based on the patterns provided in a wildcard file.

#### Command to use:
```bash
python manage_alerts.py <action> <wildcard_file> <resource_group>
```

#### Example:
```bash
python manage_alerts.py enable wildcard.txt rg-poc-ol
```

#### Wildcard File Format:
Create a `wildcard.txt` file with each wildcard on a new line (case-insensitive matching):
```
google
facebook
```

#### Parameters:
- `<action>`: The action you want to perform: `enable` or `disable`.
- `<wildcard_file>`: The file containing wildcard patterns to match alert names.
- `<resource_group>`: The Azure resource group where alerts are located.

### **2. Manage Availability Tests (`manage_availability_tests.py`)**
This script enables or disables Azure Application Insights availability tests based on the patterns provided in a wildcard file.

#### Command to use:
```bash
python manage_availability_tests.py <action> <wildcard_file> <resource_group>
```

#### Example:
```bash
python manage_availability_tests.py disable wildcard.txt rg-poc-ol
```

#### Wildcard File Format:
Create a `wildcard.txt` file with each wildcard on a new line (case-insensitive matching):
```
google
azure
```

#### Parameters:
- `<action>`: The action you want to perform: `enable` or `disable`.
- `<wildcard_file>`: The file containing wildcard patterns to match availability test names.
- `<resource_group>`: The Azure resource group where availability tests are located.

## Error Handling

Both scripts include error handling for:
1. Missing or unreadable wildcard files.
2. Invalid resource group names.
3. Azure API errors while fetching or updating alerts/tests.
4. Case-insensitive wildcard matching for resource names.

### Example Wildcard File:
`wildcard.txt`
```txt
google
azure
```

### Example Execution:
```bash
python manage_alerts.py disable wildcard.txt rg-poc-ol
python manage_availability_tests.py disable wildcard.txt rg-poc-ol
```
![Availability Test Disabled](screenshot\disableAVT.png)
![Availability Test Disabled](screenshot\availabilityTest.png)
![Metric Alert Disabled](screenshot\disableAlert.png)
![Metric Alert Disabled](screenshot\disabledAlert2.png)



## Conclusion

These scripts help in bulk enabling or disabling Azure metric alerts and availability tests using wildcard patterns. You can use these scripts to automate the management of these resources across multiple projects and environments.

---