### Hi there 👋

Kubernetes Hands-On DevOps Project

Overview
This repository documents a collection of practical Kubernetes tasks executed in a real cluster environment. The project focuses on persistent storage, pod scheduling, security, configuration management, networking, and containerization. All tasks were validated using kubectl commands and YAML manifests.

Technologies Used
Kubernetes
Docker
Linux
YAML manifests
Persistent Volumes and Claims
ConfigMaps and Secrets
Ingress
Deployments, Pods, DaemonSets
Resource Requests and Limits
ServiceAccounts

Task 10 – Persistent Storage (PV and PVC)

Created file on node sk8s-node-0 at /opt/KDSP00101/data/index.html

Created PersistentVolume named task-pv-volume
Capacity: 1Gi
Type: hostPath
Path: /opt/KDSP00101/data
AccessMode: ReadWriteOnce
StorageClass: exam

Created PersistentVolumeClaim task-pv-claim requesting 100Mi

Created a Pod with label app=my-storage-app

Mounted PVC to /usr/share/nginx/html

Validation commands
cat /opt/KDSP00101/data/index.html
kubectl get pv,pvc
kubectl get pods

Task 11 – Requests, Limits and ServiceAccount

Created Deployment neptune-10ab

Image: httpd:2.4-alpine

Replicas: 3

Container name: neptune-pod-10ab

Memory request: 20Mi

Namespace: neptune

Validation commands
kubectl get pods -n neptune
kubectl get sa -n neptune

Task 12 – Secrets and Environment Variables

Created Secret app-secret
key3=value1

Created Pod nginx-secret

Injected secret value as environment variable BEST_VARIABLE

Validation commands
kubectl get secret
kubectl get pods
kubectl get pod nginx-secret -o yaml

Task 13 – Pod Resource Requests

Created Pod nginx-resources

Image: nginx:stable

CPU request: 300m

Memory request: 1Gi

Validation commands
kubectl get pods
kubectl get pod nginx-resources -o yaml

Task 14 – Deployment, Service and Ingress

Created namespace btu-final

Created Deployment nginx-deployment
Replicas: 2
Image: nginx:1.14.2
ContainerPort: 80
Environment variable: NGINX__PORT=8080

Exposed Deployment using ClusterIP Service

Created Ingress
Host: nginx.final.eu
Backend service: nginx-deployment port 80

Validation commands
kubectl get namespace
kubectl get deployment -n btu-final
kubectl get deployment nginx-deployment -o yaml -n btu-final

Task 15 – ConfigMap Volume Mount

Created ConfigMap another-config
key4=value3

Created Pod nginx-configmap

Mounted ConfigMap into /also/a/path

Validation commands
kubectl get cm -n btu-final
kubectl get pod nginx-configmap -o yaml -n btu-final

Task 16 – Docker Image Build and Export

Created Dockerfile using bash base image

Executed ping killercoda.com

Built image pinger:3.0

Exported image to /root/pinger3.0.tar in OCI format

Validation commands
docker images
ls /root/

Task 17 – Pod Scheduling with Resource Requests

Created Pod nginx-resources in namespace btu-final

Image: nginx

CPU request: 200m

Memory request: 1Gi

Validation commands
kubectl get pods -n btu-final
kubectl get pod nginx-resources -o yaml -n btu-final

Task 18 – Deployment with Limits and ServiceAccount

Created Deployment neptune-10ab in namespace btu-final

Replicas: 3

Image: httpd:2.4-alpine

Memory request: 20Mi

Memory limit: 50Mi

Pods run under ServiceAccount neptune-sa-v2

Validation commands
kubectl get pods -n btu-final
kubectl get sa -n btu-final

Task 19 – DaemonSet for Node Configuration

Created namespace configurator

Created DaemonSet configurator

Image: bash

Mounted hostPath /configurator

Wrote configuration file to /configurator/config

Kept container running using sleep

Validation command
kubectl get daemonset -n configurator -o yaml

Task 20 – Pod, Service and Port Forwarding

Created namespace httpd-app

Created Pod app-pod using httpd:latest

Created Service app-svc of type ClusterIP

Forwarded local port using kubectl port-forward

Verified application using curl

Validation commands
kubectl get pod -n httpd-app -o yaml
kubectl get service app-svc -n httpd-app -o yaml

Task 21 – Redis ConfigMap

Created ConfigMap redis-config
maxmemory=2mb
maxmemory-policy=allkeys-lru

Validation command
kubectl get cm redis-config -o yaml

Task 22 – Minimal Ingress

Created Ingress minimal-ingress

Domain: hello.com

Backend service: apache-svc port 80

Validation command
kubectl get ingress minimal-ingress -o yaml

Summary
This project demonstrates real-world Kubernetes administration skills including persistent storage management, secure configuration, workload orchestration, networking with services and ingress, resource optimization, and node-level configuration.
