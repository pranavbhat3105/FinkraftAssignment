# FinkraftAssignment

Here is a small `README.md` file structured to cover all the required deliverables and setup instructions.

````markdown
# DevOps Project: Flask Application with CI/CD, HPA, and Monitoring

This repository contains a complete DevOps pipeline for the provided assignment, demonstrating core practices including containerization, automated CI/CD, Kubernetes deployment with Horizontal Pod Autoscaling (HPA), and a full Prometheus/Grafana monitoring stack.

## 🚀 Project Overview

The application is a lightweight Flask service exposing two endpoints: `/health` (for readiness checks) and `/stress` (used to simulate high CPU load).

| Component            | Tool                  | Purpose                                                            |
| :-----------------:  | :--------------------:| :----------------------------------------------------------------:|
| **Application**      | Python Flask          | Simple API endpoints and CPU-intensive endpoint for load testing. |
| **Containerization** | Docker                | Packaging the application for consistent deployment.              |
| **CI/CD**            | GitHub Actions        | Automates testing, Docker image building/pushing, and deployment. |
| **Deployment**       | Minikube + Helm       | Kubernetes cluster and package manager for deployment/HPA configuration. |
| **Auto Scaling**     | Kubernetes HPA        | Scales pods based on CPU utilization (min 2, max 10, target 50%). |
| **Monitoring**       | Prometheus + Grafana  | Metrics collection, visualization, and alerting.                  |

---

## 🛠️ Step-by-Step Setup and Execution

### 1. Local Prerequisites

Ensure you have the following installed locally:
* **Docker**
* **Minikube**
* **kubectl**
* **Helm**
* **Python 3.9+**

### 2. Kubernetes Cluster Setup

Start your Minikube cluster and ensure the **Metrics Server** (required for HPA) is active.

```bash
minikube start --driver=docker
# Optional: Verify Metrics Server is running
kubectl get apiservices | grep metrics
````

### 3\. CI/CD Pipeline Workflow

The CI/CD is managed by the workflow file: `.github/workflows/ci-cd.yml`.

| Stage  | Action             | Details |
| :---   | :---              | :---     |
| **CI** | Test, Build, Push | **GitHub Actions** runs Python linting/tests, builds the Docker image , and pushes it to DockerHub using configured  secrets. |
| **CD** | Deploy            | After a successful build, **Helm** is used to perform a rolling update (`helm upgrade --install`) on the Kubernetes cluster, deploying the new image tag. |

 Set the following secrets in your GitHub repository settings: `DOCKER_USERNAME`, `DOCKER_PASSWORD`, and `KUBE_CONFIG_DATA`.

### 4\. Auto Scaling Demonstration (HPA Test)

The HPA is configured in `flask-chart/templates/hpa.yaml` to scale the application from **2 to 10 replicas** when CPU utilization hits **50%**.

**Procedure:**

1.  **Monitor Status:** In one terminal, watch the HPA:

    ```bash
    watch kubectl get hpa
    ```

    *Initial state should show 2/10 Replicas.*

2.  **Apply Load:** Execute the `kubectl stress` command to target the CPU-intensive `/stress` endpoint.

    ```bash
    kubectl run -it --rm load-tester --image=quay.io/travisghansen/kubectl-stress -- /bin/sh -c "ab -n 50000 -c 100 -s 60 -T 'application/json' http://devops-release-flask-chart/stress"
    ```

3.  **Observation:** The HPA will respond by increasing the pod count (up to 10) to bring the CPU utilization back under 50%. **Capture a screenshot/video of the scaling in action.**

4.  **Stop Load:** To stop the stress test and observe the scale-down (a gradual process), simply delete the temporary pod:

    ```bash
    kubectl delete pod load-tester
    ```

-----

## 5\. Monitoring & Alerting Setup

We use the `kube-prometheus-stack` Helm chart to quickly deploy our observability tools.

### Setup and Grafana Access

1.  **Install Monitoring Stack:**

    ```bash
    helm repo add prometheus-community [https://prometheus-community.github.io/helm-charts](https://prometheus-community.github.io/helm-charts)
    helm install prometheus-stack prometheus-community/kube-prometheus-stack --namespace monitoring --create-namespace
    ```

2.  **Access Grafana:** Forward the port to access the Grafana GUI locally:

    ```bash
    # Get the Grafana service name (e.g., prometheus-stack-grafana)
    kubectl get svc -n monitoring 
    # Forward the port
    kubectl port-forward svc/<GRAFANA_SVC_NAME> 3000:80 -n monitoring
    ```

    Access at **`http://localhost:3000`**. Use the default `admin` username and retrieve the password from the Kubernetes secret.

### Alerting Details

  * **Tool:** Alertmanager (included in the stack).
  * **Alert Rule:** Defined via a `PrometheusRule` CRD (must be created separately, targeting your application deployment).
  * **Example Threshold:** An alert is configured to fire if the application's CPU utilization exceeds **80%** for a sustained period.
  * **Notification:** Alertmanager must be configured (via its Helm values) to integrate with a service like **Email (SMTP)** or **Slack** to send notifications when the threshold is breached. **A screenshot of a received alert notification is required.**

<!-- end list -->

```
```
