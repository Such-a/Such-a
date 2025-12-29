Here is the README.md content using your exact text, organized with professional Markdown formatting to make it clean and readable for GitHub.

Kubernetes Hands-On DevOps Project Overview
This project contains practical Kubernetes tasks covering storage, networking, security, resource management, and workload deployment. It demonstrates real-world DevOps and Kubernetes administration skills through hands-on exercises.

🛠 Technologies Used
Orchestration: Kubernetes

Containerization: Docker

Operating System: Linux

Configuration: YAML Manifests

Storage: PersistentVolumes & PersistentVolumeClaims

Configuration Management: ConfigMaps & Secrets

Workloads: Deployments, Pods, DaemonSets

Networking: Services & Ingress

Resource Management: Resource Requests & Limits

Identity: ServiceAccounts

📝 Tasks
Task 10 – Persistent Storage
Objectives

Create a file on node sk8s-node-0: /opt/KDSP00101/data/index.html (Content: Acct=Finance)

Create a PersistentVolume:

Name: task-pv-volume

Type: hostPath

Path: /opt/KDSP00101/data

Capacity: 1Gi

Access Mode: ReadWriteOnce

StorageClass: exam

Create a PersistentVolumeClaim:

Name: task-pv-claim

Request: 100Mi

Create a Pod:

Name: my-storage-app

Mount PVC at /usr/share/nginx/html

Task 11 – Resource Requests & ServiceAccount
Objectives

Create Deployment neptune-10ab

Namespace: neptune

Replicas: 3

Image: httpd:2.4-alpine

Container name: neptune-pod-10ab

Memory request: 20Mi

Task 12 – Secrets & Environment Variables
Objectives

Create Secret app-secret (key3=value1)

Create Pod nginx-secret

Consume secret as environment variable BEST_VARIABLE

Task 13 – Pod Resource Requests
Objectives

Pod name: nginx-resources

Image: nginx:stable

CPU request: 300m

Memory request: 1Gi

Task 14 – Deployment, Service & Ingress
Objectives

Namespace: btu-final

Deployment:

Name: nginx-deployment

Replicas: 2

Image: nginx:1.14.2

Container port: 80

Environment variable: NGINX__PORT=8080

Expose Deployment via:

Service type: ClusterIP

Create Ingress:

Name: nginx-deployment

Host: nginx.final.eu

Backend: nginx-deployment:80

Task 15 – ConfigMap Volume Mount
Objectives

Create ConfigMap another-config (key4=value3)

Create Pod nginx-configmap

Mount ConfigMap at /also/a/path

Task 16 – Docker Image Build & Export
Objectives

Create Dockerfile:

Base image: bash

Command: ping killercoda.com

Build image: pinger:3.0

Export image: /root/pinger3.0.tar

Task 17 – Pod Scheduling with Resources
Objectives

Pod name: nginx-resources

Namespace: btu-final

Image: nginx

CPU request: 200m

Memory request: 1Gi

Task 18 – Deployment with Limits & ServiceAccount
Objectives

Deployment name: neptune-10ab

Namespace: btu-final

Replicas: 3

Memory: Request 20Mi / Limit 50Mi

ServiceAccount: neptune-sa-v2

Task 19 – DaemonSet for Node Configuration
Objectives

Namespace: configurator

DaemonSet name: configurator

Image: bash

Mount hostPath: /configurator

Write file: /configurator/config

Keep container running: sleep 1d

Task 20 – Pod, Service & Port Forward
Objectives

Namespace: httpd-app

Pod: app-pod (Image: httpd:latest)

Service: app-svc (Type: ClusterIP, Port: 80)

Access app via port-forward and curl

Task 21 – Redis ConfigMap
Objectives

Create ConfigMap redis-config

maxmemory=2mb

maxmemory-policy=allkeys-lru

Task 22 – Minimal Ingress
Objectives

Ingress name: minimal-ingress

Domain: hello.com

Backend service: apache-svc:80

📊 Summary
This project demonstrates practical Kubernetes and DevOps skills, including:

Persistent storage management

Resource requests and limits

Secure configuration with Secrets & ConfigMaps

Deployments, Services, Ingress, and DaemonSets

ServiceAccounts and namespace isolation

Docker image building and exporting

Node-level configuration and pod scheduling
