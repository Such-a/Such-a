Kubernetes Hands-On DevOps Project Overview
This project contains practical Kubernetes tasks covering storage, networking, security, resource management, and workload deployment. It demonstrates real-world DevOps and Kubernetes administration skills through hands-on exercises.

🚀 Technologies Used
Kubernetes

Docker

Linux

YAML Manifests

PersistentVolumes & PersistentVolumeClaims

ConfigMaps & Secrets

Deployments, Pods, DaemonSets

Services & Ingress

Resource Requests & Limits

ServiceAccounts

🛠 Tasks
Task 10 – Persistent Storage
Objectives

Create a file on node sk8s-node-0: /opt/KDSP00101/data/index.html

Content: Acct=Finance

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

Mount PVC at: /usr/share/nginx/html

Validation

Bash

kubectl get pv,pvc
kubectl get pods
cat /opt/KDSP00101/data/index.html
Task 11 – Resource Requests & ServiceAccount
Objectives

Create Deployment neptune-10ab

Namespace: neptune

Replicas: 3

Image: httpd:2.4-alpine

Container name: neptune-pod-10ab

Memory request: 20Mi

Validation

Bash

kubectl get pods -n neptune
kubectl get sa -n neptune
Task 12 – Secrets & Environment Variables
Objectives

Create Secret app-secret: key3=value1

Create Pod nginx-secret

Consume secret as environment variable BEST_VARIABLE

Validation

Bash

kubectl get secret
kubectl get pods
kubectl get pod nginx-secret -o yaml
Task 13 – Pod Resource Requests
Objectives

Pod name: nginx-resources

Image: nginx:stable

CPU request: 300m

Memory request: 1Gi

Validation

Bash

kubectl get pods
kubectl get pod nginx-resources -o yaml
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

Validation

Bash

kubectl get namespace
kubectl get deployment -n btu-final
kubectl get deployment nginx-deployment -o yaml -n btu-final
Task 15 – ConfigMap Volume Mount
Objectives

Create ConfigMap another-config: key4=value3

Create Pod nginx-configmap

Mount ConfigMap at /also/a/path

Validation

Bash

kubectl get cm -n btu-final
kubectl get pod nginx-configmap -o yaml -n btu-final
Task 16 – Docker Image Build & Export
Objectives

Create Dockerfile:

Base image: bash

Command: ping killercoda.com

Build image: pinger:3.0

Export image: /root/pinger3.0.tar

Validation

Bash

docker images
ls /root/
Task 17 – Pod Scheduling with Resources
Objectives

Pod name: nginx-resources

Namespace: btu-final

Image: nginx

CPU request: 200m

Memory request: 1Gi

Validation

Bash

kubectl get pods -n btu-final
kubectl get pod nginx-resources -o yaml -n btu-final
Task 18 – Deployment with Limits & ServiceAccount
Objectives

Deployment name: neptune-10ab

Namespace: btu-final

Replicas: 3

Memory:

Request: 20Mi

Limit: 50Mi

ServiceAccount: neptune-sa-v2

Validation

Bash

kubectl get pods -n btu-final
kubectl get sa -n btu-final
Task 19 – DaemonSet for Node Configuration
Objectives

Namespace: configurator

DaemonSet name: configurator

Image: bash

Mount hostPath: /configurator

Write file: /configurator/config

Keep container running: sleep 1d

Validation

Bash

kubectl get daemonset -n configurator -o yaml
Task 20 – Pod, Service & Port Forward
Objectives

Namespace: httpd-app

Pod:

Name: app-pod

Image: httpd:latest

Service:

Name: app-svc

Type: ClusterIP

Port: 80

Access app via port-forward and curl

Validation

Bash

kubectl get pod -n httpd-app -o yaml
kubectl get service app-svc -n httpd-app -o yaml
Task 21 – Redis ConfigMap
Objectives

Create ConfigMap redis-config:

maxmemory=2mb

maxmemory-policy=allkeys-lru

Validation

Bash

kubectl get cm redis-config -o yaml
Task 22 – Minimal Ingress
Objectives

Ingress name: minimal-ingress

Domain: hello.com

Backend service: apache-svc:80

Validation

Bash

kubectl get ingress minimal-ingress -o yaml
📝 Summary
This project demonstrates practical Kubernetes and DevOps skills, including:

Persistent storage management

Resource requests and limits

Secure configuration with Secrets & ConfigMaps

Deployments, Services, Ingress, and DaemonSets

ServiceAccounts and namespace isolation

Docker image building and exporting

Node-level configuration and pod scheduling
