# Webhook Service for ACS Audit Logging

## Introduction

This project contains a Python Flask-based webhook service designed to demonstrate the audit logging integration of Red Hat Advanced Cluster Security for Kubernetes (ACS). ACS provides audit logging to monitor changes made within the system, capturing important PUT and POST events through generic webhook. This webhook service is configured to receive and display these audit log messages, facilitating the monitoring and troubleshooting of ACS.

## Prerequisites

    * Python 3.8 or higher.
    * Docker or Podman for containerization.
    * Access to an OpenShift cluster for deployment. (I recommend [CRC](https://github.com/crc-org/crc) if you want to test it in your local)
    * Basic understanding of Red Hat Advanced Cluster Security for Kubernetes, including permissions to configure audit logging integration.

## Installation

### Building the Container

Clone this repository to your local machine. Navigate to the cloned directory and build the Docker container:

```bash
$ podman build -t webhook-service .
```

Push the built image to a container registry:

```bash
$ podman tag webhook-service [YOUR_REGISTRY]/webhook-service
$ podman push [YOUR_REGISTRY]/webhook-service
```

### Deploying on OpenShift
Log in to your OpenShift cluster using the oc CLI. Deploy the webhook service using the image from your registry:

```bash
$ oc new-project auditlogs
$ oc new-app [YOUR_REGISTRY]/webhook-service
$ oc expose svc/webhook-service
```

Note the exposed service URL, which will be used as the webhook endpoint in ACS.

### Usage
Enabling Audit Logging in ACS:

* Log in to the RHACS portal.
* Navigate to Platform Configuration → Integrations.
* In the Notifier Integrations section, select Generic Webhook or Splunk.
* Fill in the required information, including the URL of the deployed webhook service.
* Enable Audit Logging.

### Viewing Audit Logs

Once enabled, ACS will send HTTP POST messages to the configured webhook URL whenever a modification occurs. The webhook service will display these messages, allowing you to monitor ACS activities and audit logs. You can save the Json objects in a PersistentVolume if you want. 

The audit log messages are in JSON format, providing comprehensive details about each event, including the type of interaction (e.g., CREATE), the method used (e.g., UI), and the source IP address. A sample audit log message is provided in the container.

To check your audit logs you can simulate the creationg of a SecurityPolicy in ACS and check the container logs as below:

```bash
$ oc logs mywebhook-7768c5ffcb-rfnt8
 * Serving Flask app 'main'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8080
 * Running on http://10.217.0.205:8080
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 570-989-203
10.217.0.1 - - [10/Jan/2024 15:06:15] "POST /webhook HTTP/1.1" 200 -
10.217.0.1 - - [10/Jan/2024 15:07:35] "POST /webhook HTTP/1.1" 200 -
10.217.0.1 - - [10/Jan/2024 15:08:11] "POST /webhook HTTP/1.1" 200 -
Received a POST request:
{'key': 'value'}
Received a POST request:
{'audit': {'time': '2024-01-10T15:07:35.614205079Z', 'status': 'REQUEST_SUCCEEDED', 'user': {'friendlyName': 'kubeadmin', 'permissions': {'resourceToAccess': {'Access': 'READ_WRITE_ACCESS', 'Administration': 'READ_WRITE_ACCESS', 'Alert': 'READ_WRITE_ACCESS', 'CVE': 'READ_WRITE_ACCESS', 'Cluster': 'READ_WRITE_ACCESS', 'Compliance': 'READ_WRITE_ACCESS', 'Deployment': 'READ_WRITE_ACCESS', 'DeploymentExtension': 'READ_WRITE_ACCESS', 'Detection': 'READ_WRITE_ACCESS', 'Image': 'READ_WRITE_ACCESS', 'Integration': 'READ_WRITE_ACCESS', 'K8sRole': 'READ_WRITE_ACCESS', 'K8sRoleBinding': 'READ_WRITE_ACCESS', 'K8sSubject': 'READ_WRITE_ACCESS', 'Namespace': 'READ_WRITE_ACCESS', 'NetworkGraph': 'READ_WRITE_ACCESS', 'NetworkPolicy': 'READ_WRITE_ACCESS', 'Node': 'READ_WRITE_ACCESS', 'Secret': 'READ_WRITE_ACCESS', 'ServiceAccount': 'READ_WRITE_ACCESS', 'VulnerabilityManagementApprovals': 'READ_WRITE_ACCESS', 'VulnerabilityManagementRequests': 'READ_WRITE_ACCESS', 'WatchedImage': 'READ_WRITE_ACCESS', 'WorkflowAdministration': 'READ_WRITE_ACCESS'}}, 'roles': [{'name': 'Admin', 'resourceToAccess': {'Access': 'READ_WRITE_ACCESS', 'Administration': 'READ_WRITE_ACCESS', 'Alert': 'READ_WRITE_ACCESS', 'CVE': 'READ_WRITE_ACCESS', 'Cluster': 'READ_WRITE_ACCESS', 'Compliance': 'READ_WRITE_ACCESS', 'Deployment': 'READ_WRITE_ACCESS', 'DeploymentExtension': 'READ_WRITE_ACCESS', 'Detection': 'READ_WRITE_ACCESS', 'Image': 'READ_WRITE_ACCESS', 'Integration': 'READ_WRITE_ACCESS', 'K8sRole': 'READ_WRITE_ACCESS', 'K8sRoleBinding': 'READ_WRITE_ACCESS', 'K8sSubject': 'READ_WRITE_ACCESS', 'Namespace': 'READ_WRITE_ACCESS', 'NetworkGraph': 'READ_WRITE_ACCESS', 'NetworkPolicy': 'READ_WRITE_ACCESS', 'Node': 'READ_WRITE_ACCESS', 'Secret': 'READ_WRITE_ACCESS', 'ServiceAccount': 'READ_WRITE_ACCESS', 'VulnerabilityManagementApprovals': 'READ_WRITE_ACCESS', 'VulnerabilityManagementRequests': 'READ_WRITE_ACCESS', 'WatchedImage': 'READ_WRITE_ACCESS', 'WorkflowAdministration': 'READ_WRITE_ACCESS'}}]}, 'request': {'endpoint': '/v1/notifiers', 'method': 'POST', 'payload': {'@type': 'storage.Notifier', 'id': '13e19570-a5d3-4869-9a9d-1c4048063b6a', 'name': 'MyAuditLog', 'type': 'generic', 'uiEndpoint': 'https://central-stackrox.apps-crc.testing', 'generic': {'endpoint': 'http://mywebhook-acsauditlog.apps-crc.testing/webhook', 'skipTLSVerify': True, 'auditLoggingEnabled': True}}, 'sourceHeaders': {'requestAddr': '10.217.0.1:49318'}, 'sourceIp': '10.217.0.1:49318'}, 'method': 'UI', 'interaction': 'CREATE'}}
Received a POST request:
{'audit': {'time': '2024-01-10T15:08:11.645646845Z', 'status': 'REQUEST_SUCCEEDED', 'user': {'friendlyName': 'kubeadmin', 'permissions': {'resourceToAccess': {'Access': 'READ_WRITE_ACCESS', 'Administration': 'READ_WRITE_ACCESS', 'Alert': 'READ_WRITE_ACCESS', 'CVE': 'READ_WRITE_ACCESS', 'Cluster': 'READ_WRITE_ACCESS', 'Compliance': 'READ_WRITE_ACCESS', 'Deployment': 'READ_WRITE_ACCESS', 'DeploymentExtension': 'READ_WRITE_ACCESS', 'Detection': 'READ_WRITE_ACCESS', 'Image': 'READ_WRITE_ACCESS', 'Integration': 'READ_WRITE_ACCESS', 'K8sRole': 'READ_WRITE_ACCESS', 'K8sRoleBinding': 'READ_WRITE_ACCESS', 'K8sSubject': 'READ_WRITE_ACCESS', 'Namespace': 'READ_WRITE_ACCESS', 'NetworkGraph': 'READ_WRITE_ACCESS', 'NetworkPolicy': 'READ_WRITE_ACCESS', 'Node': 'READ_WRITE_ACCESS', 'Secret': 'READ_WRITE_ACCESS', 'ServiceAccount': 'READ_WRITE_ACCESS', 'VulnerabilityManagementApprovals': 'READ_WRITE_ACCESS', 'VulnerabilityManagementRequests': 'READ_WRITE_ACCESS', 'WatchedImage': 'READ_WRITE_ACCESS', 'WorkflowAdministration': 'READ_WRITE_ACCESS'}}, 'roles': [{'name': 'Admin', 'resourceToAccess': {'Access': 'READ_WRITE_ACCESS', 'Administration': 'READ_WRITE_ACCESS', 'Alert': 'READ_WRITE_ACCESS', 'CVE': 'READ_WRITE_ACCESS', 'Cluster': 'READ_WRITE_ACCESS', 'Compliance': 'READ_WRITE_ACCESS', 'Deployment': 'READ_WRITE_ACCESS', 'DeploymentExtension': 'READ_WRITE_ACCESS', 'Detection': 'READ_WRITE_ACCESS', 'Image': 'READ_WRITE_ACCESS', 'Integration': 'READ_WRITE_ACCESS', 'K8sRole': 'READ_WRITE_ACCESS', 'K8sRoleBinding': 'READ_WRITE_ACCESS', 'K8sSubject': 'READ_WRITE_ACCESS', 'Namespace': 'READ_WRITE_ACCESS', 'NetworkGraph': 'READ_WRITE_ACCESS', 'NetworkPolicy': 'READ_WRITE_ACCESS', 'Node': 'READ_WRITE_ACCESS', 'Secret': 'READ_WRITE_ACCESS', 'ServiceAccount': 'READ_WRITE_ACCESS', 'VulnerabilityManagementApprovals': 'READ_WRITE_ACCESS', 'VulnerabilityManagementRequests': 'READ_WRITE_ACCESS', 'WatchedImage': 'READ_WRITE_ACCESS', 'WorkflowAdministration': 'READ_WRITE_ACCESS'}}]}, 'request': {'endpoint': '/v1/policies/dryrunjob', 'method': 'POST', 'payload': {'@type': 'storage.Policy', 'name': '30-Day Scan Age (COPY)', 'description': "Alert on deployments with images that haven't been scanned in 30 days", 'rationale': 'Out-of-date scans may not identify the most recent CVEs.', 'remediation': 'Integrate a scanner with the StackRox Kubernetes Security Platform to trigger scans automatically.', 'categories': ['Security Best Practices'], 'lifecycleStages': ['DEPLOY'], 'severity': 'MEDIUM_SEVERITY', 'SORTName': '30-Day Scan Age', 'SORTLifecycleStage': 'DEPLOY', 'policyVersion': '1.1', 'policySections': [{'policyGroups': [{'fieldName': 'Image Scan Age', 'values': [{'value': '30'}]}]}]}, 'sourceHeaders': {'requestAddr': '10.217.0.1:49318'}, 'sourceIp': '10.217.0.1:49318'}, 'method': 'UI', 'interaction': 'CREATE'}}
Received a POST request:
```


## Contributing 

Whether it's reporting a bug, proposing a feature, or submitting a pull request, every bit of help is appreciated. Feel free to dive in and raise issues or contribute through pull requests. 