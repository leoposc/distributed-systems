#!/bin/bash

# Get the Minikube IP address
MINIKUBE_IP=$(minikube ip)

# Define the hostname to add to /etc/hosts
HOSTNAME="play.music.local"

# Check if the entry already exists
if grep -q "$HOSTNAME" /etc/hosts; then
  echo "$HOSTNAME already exists in /etc/hosts"
else
  # Add the Minikube IP and the hostname to /etc/hosts
  echo "$MINIKUBE_IP $HOSTNAME" | sudo tee -a /etc/hosts > /dev/null
  echo "Added $HOSTNAME to /etc/hosts with IP $MINIKUBE_IP"
fi
