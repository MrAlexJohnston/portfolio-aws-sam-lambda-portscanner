# Portfolio Port Scanner Lambda - AWS SAM

This project deploys a port scanner Lambda function using AWS SAM (Serverless Application Model). The Lambda function scans a specified target (domain or IP address) for open ports and returns the results. Additionally, the project includes Application Insights for enhanced monitoring and troubleshooting of the Lambda function's execution.

## Project Overview

- **Lambda Function**: The `PortScannerFunction` performs a concurrent scan of all ports (0-65535) on the specified target using Python's `ThreadPoolExecutor`.
- **AWS Resources**: 
  - **Application Insights Monitoring**: AWS Application Insights is configured to monitor the Lambda function, providing insights into the performance and potential issues.
  - **Resource Group**: An Application Resource Group is created to manage monitoring of resources related to the port scanning functionality.
  
## Project Structure

- **port_scanner/**: Contains the Lambda function's source code.
  - `app.py`: Main entry point for the Lambda function.
  - `__init__.py`: Standard Python package initialization file.
  
- **tests/**: Contains unit tests for the Lambda function.
  - `__init__.py`: Test package initialization file.
  
- **template.yaml**: AWS SAM template defining the Lambda function, monitoring, and resource group.

## SAM Template Overview

### Resources Defined

- **PortScannerFunction**:  
  - **Handler**: `app.lambda_handler`
  - **Runtime**: Python 3.9
  - **Architecture**: x86_64
  - **Timeout**: 900 seconds (15 minutes)
  - **Memory Size**: 2048 MB
  - **Environment Variables**:
    - `MAX_WORKERS`: Maximum number of concurrent workers (set to 900 by default).
  
- **ApplicationResourceGroup**:  
  A resource group created to track and manage related resources using CloudFormation stack-based queries.

- **ApplicationInsightsMonitoring**:  
  Configures AWS Application Insights for monitoring and automated issue detection. Application Insights helps track performance and error rates for the Lambda function.

### Globals Configuration

The `Globals` section defines default settings for all functions in the SAM template:

- **Timeout**: 3 seconds (overridden by specific function settings).
- **MemorySize**: 128 MB (overridden by specific function settings).
- **LoggingConfig**: Uses JSON format for Lambda logs.

## Deployment Instructions

### Prerequisites

- AWS CLI configured with appropriate permissions.
- AWS SAM CLI installed (`npm install -g aws-sam-cli`).
- Python 3.9 installed locally.

### Deployment Steps

1. **Build and Package the Application**  
   Use SAM CLI to build and package the application for deployment:

   ```bash
   sam build
