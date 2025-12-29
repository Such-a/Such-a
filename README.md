Kubernetes Hands-On DevOps Project
Overview

This project contains practical Kubernetes tasks covering storage, networking, security, resource management, and workload deployment. It demonstrates real-world DevOps and Kubernetes administration skills.

Technologies

Kubernetes

Docker

Linux

YAML manifests

PersistentVolumes & PersistentVolumeClaims

ConfigMaps & Secrets

Deployments, Pods, DaemonSets

Services & Ingress

Resource Requests & Limits

ServiceAccounts

Tasks
Task 10 – Persistent Storage

Create file on node sk8s-node-0 at /opt/KDSP00101/data/index.html with content Acct=Finance

Create PersistentVolume task-pv-volume with hostPath /opt/KDSP00101/data (1Gi, ReadWriteOnce, StorageClass exam)

Create PersistentVolumeClaim task-pv-claim requesting 100Mi

Create Pod my-storage-app mounting PVC at /usr/share/nginx/html

Validation:

kubectl get pv,pvc
kubectl get pods
cat /opt/KDSP00101/data/index.html

Task 11 – Resource Requests & ServiceAccount

Deployment neptune-10ab with 3 replicas of httpd:2.4-alpine

Container name: neptune-pod-10ab

Memory request: 20Mi

Namespace: neptune

Validation:

kubectl get pods -n neptune
kubectl get sa -n neptune

Task 12 – Secrets & Environment Variables

Secret app-secret with key3=value1

Pod nginx-secret consumes secret as env variable BEST_VARIABLE

Validation:

kubectl get secret
kubectl get pods
kubectl get pod nginx-secret -o yaml

Task 13 – Pod Resource Requests

Pod nginx-resources using image nginx:stable

CPU request: 300m, Memory request: 1Gi

Validation:

kubectl get pods
kubectl get pod nginx-resources -o yaml

Task 14 – Deployment, Service & Ingress

Namespace btu-final

Deployment nginx-deployment (2 replicas, image nginx:1.14.2, containerPort 80, env NGINX__PORT=8080)

Expose Deployment via ClusterIP Service

Create Ingress nginx-deployment host nginx.final.eu backend service nginx-deployment:80

Validation:

kubectl get namespace
kubectl get deployment -n btu-final
kubectl get deployment nginx-deployment -o yaml -n btu-final

Task 15 – ConfigMap Volume Mount

ConfigMap another-config with key4=value3

Pod nginx-configmap mounts ConfigMap at /also/a/path

Validation:

kubectl get cm -n btu-final
kubectl get pod nginx-configmap -o yaml -n btu-final

Task 16 – Docker Image Build & Export

Dockerfile using bash base image, run ping killercoda.com

Build image pinger:3.0

Export image to /root/pinger3.0.tar

Validation:

docker images
ls /root/

Task 17 – Pod Scheduling with Resources

Pod nginx-resources in namespace btu-final

Requests: 200m CPU, 1Gi memory

Image: nginx

Validation:

kubectl get pods -n btu-final
kubectl get pod nginx-resources -o yaml -n btu-final

Task 18 – Deployment with Limits & ServiceAccount

Deployment neptune-10ab in namespace btu-final

3 replicas, memory request 20Mi, limit 50Mi

Pods run under ServiceAccount neptune-sa-v2

Validation:

kubectl get pods -n btu-final
kubectl get sa -n btu-final

Task 19 – DaemonSet for Node Configuration

Namespace configurator

DaemonSet configurator using bash image

Mount hostPath /configurator, write /configurator/config

Keep running using sleep 1d

Validation:

kubectl get daemonset -n configurator -o yaml

Task 20 – Pod, Service & Port Forward

Namespace httpd-app

Pod app-pod using image httpd:latest

Service app-svc ClusterIP, port 80

Port-forward to access web app using curl

Validation:

kubectl get pod -n httpd-app -o yaml
kubectl get service app-svc -n httpd-app -o yaml

Task 21 – Redis ConfigMap

ConfigMap redis-config

key: maxmemory=2mb, maxmemory-policy=allkeys-lru

Validation:

kubectl get cm redis-config -o yaml

Task 22 – Minimal Ingress

Ingress minimal-ingress

Domain hello.com → Service apache-svc:80

Validation:

kubectl get ingress minimal-ingress -o yaml

Summary

This project demonstrates Kubernetes skills including persistent storage, workload deployment, secure configuration, services, ingress, resource management, and node-level configuration.
