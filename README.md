# Webhook for RHACS Audit Logging

## Introduction

Red Hat Advanced Cluster Security for Kubernetes (RHACS) provides audit logging to track changes, capturing PUT and POST events. You can use this data for auditing, troubleshooting, record-keeping, and monitoring gaining insights into both normal and abnormal events.

When you enable audit logging, every time there is a modification, RHACS sends an HTTP POST message (JSON f) to a Webhook you provide. This is a Python Webhook container that you can use to check the log events in the container STDOUT.

![diagram](/images/diagram.png)
## Prerequisites

* Python 3.11.
* Podman or the container engine of your choice.
* Access to an OpenShift cluster for deployment. (I recommend [CRC](https://github.com/crc-org/crc) if you want to test it in your local)
* Basic understanding of Red Hat Advanced Cluster Security for Kubernetes.

## Building the Container image

Clone this repository to your local machine. Navigate to the cloned directory and build the Container:

```bash
$ podman build -t mywebhook .
```

Push the built image to a container registry:

```bash
$ podman tag mywebhook [YOUR_REGISTRY]/mywebhook
$ podman push [YOUR_REGISTRY]/mywebhook
```

## Deploying on OpenShift

Log in to your OpenShift cluster using the oc CLI. Deploy the webhook service using the image from your registry:

```bash
$ oc create -f mywebook.yaml
```


## Enabling Audit Logging in ACS:

* Log in to the RHACS Central portal.
* Navigate to Platform Configuration -> Integrations -> Generic Webhook.
* Check ✅ "Enable audit logging".

Get the route url and Fill in the Create Integration form:

```bash
$ oc get route mywebhook
NAME        HOST/PORT                                PATH   SERVICES    PORT       TERMINATION   WILDCARD
mywebhook   mywebhook-acsauditlog.apps-crc.testing          mywebhook   8080-tcp                 None
```


![Generic WebHook Configuration in ACS](/images/genericwebhook.png)

## Viewing Audit Logs

The Webhook will display the log messages in the container STDOUT. In the example below I have cloned the Policy "30-Day Scan Age".

Use the **$oc logs -f[pod-name]** command to check the container output:

```bash
$ oc logs -f mywebhook-pod
```
```json
 "request": {
            "endpoint": "/v1/policies/dryrunjob",
            "method": "POST",
            "payload": {
                "@type": "storage.Policy",
                "name": "30-Day Scan Age (CLONE)",
                "description": "Alert on deployments with images that haven't been scanned in 30 days",
                "rationale": "Out-of-date scans may not identify the most recent CVEs.",
                "remediation": "Integrate a scanner with the StackRox Kubernetes Security Platform to trigger scans automatically.",
                "categories": [
                    "Security Best Practices"
                ],
                "lifecycleStages": [
                    "DEPLOY"
                ],
                "severity": "MEDIUM_SEVERITY",
                "SORTName": "30-Day Scan Age",
                "SORTLifecycleStage": "DEPLOY",
                "policyVersion": "1.1",
                "policySections": [
                    {
                        "policyGroups": [
                            {
                                "fieldName": "Image Scan Age",
                                "values": [
                                    {
                                        "value": "30"
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            "sourceHeaders": {
                "requestAddr": "10.217.0.1:46496"
            },
            "sourceIp": "10.217.0.1:46496"
        },
        "method": "UI",
        "interaction": "CREATE"
```

## Future Work: Centralized Log Management with Loki and Grafana

I am working to implement a centralized solution for viewing and analyzing Red Hat Advanced Cluster Security (RHACS) audit logs using Loki and Grafana in the OpenShift Logging stack. Contributions are welcome. 

## Contributing 

Whether it's reporting a bug, proposing a feature, or submitting a pull request, every bit of help is appreciated. Feel free to dive in and raise issues or contribute through pull requests. 
