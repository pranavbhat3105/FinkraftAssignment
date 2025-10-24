# FinkraftAssignment

Here is a small `README.md` file structured to cover all the required deliverables and setup instructions.

````markdown
# DevOps Project: Flask Application with CI/CD, HPA, and Monitoring

This repository contains a complete DevOps pipeline for the provided assignment, demonstrating core practices including containerization, automated CI/CD, Kubernetes deployment with Horizontal Pod Autoscaling (HPA), and a full Prometheus/Grafana monitoring.

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
<img width="1275" height="67" alt="Screenshot 2025-10-24 162057" src="https://github.com/user-attachments/assets/5bf13d25-d687-4c0c-9535-c08519cc1e33" />

### 3\. CI/CD Pipeline Workflow

The CI/CD is managed by the workflow file: `.github/workflows/ci-cd.yml`.

| Stage  | Action             | Details |
| :---   | :---              | :---     |
| **CI** | Test, Build, Push | **GitHub Actions** runs Python linting/tests, builds the Docker image , and pushes it to DockerHub using configured  secrets. |
| **CD** | Deploy            | After a successful build, **Helm** is used to perform a rolling update (`helm upgrade --install`) on the Kubernetes cluster (EKS), deploying the new image tag. |

 Set the following secrets in your GitHub repository settings: `DOCKER_USERNAME`, `DOCKER_PASSWORD`, `AWS_IAM_ARN` and `KUBE_CONFIG_DATA`.

### 4\. Auto Scaling Demonstration (HPA Test)

The HPA is configured in `flask-chart/templates/hpa.yaml` to scale the application from **2 to 10 replicas** when CPU utilization hits **50%**.

**Procedure:**

1.  **Monitor Status:** In one terminal, watch the HPA:

    ```bash
    watch kubectl get hpa
    ```

    *Initial state should show 2/10 Replicas.*

    <img width="1516" height="169" alt="Screenshot 2025-10-24 161239" src="https://github.com/user-attachments/assets/906fb920-20d4-441c-b977-0aa25ca8febf" />


3.  **Apply Load:** Execute the `kubectl stress` command to target the CPU-intensive `/stress` endpoint.

    ```bash
    kubectl run -it --rm load-tester --image=quay.io/travisghansen/kubectl-stress -- /bin/sh -c "ab -n 50000 -c 100 -s 60 -T 'application/json' http://10.97.232.38:3000/stress"
    ```

4.  **Observation:** The HPA will respond by increasing the pod count (up to 10) to bring the CPU utilization back under 50%. ****

   <img width="1457" height="588" alt="Screenshot 2025-10-24 161407" src="https://github.com/user-attachments/assets/28ffac94-2fe5-41b7-849a-cbb99b133c58" />


6.  **Stop Load:** To stop the stress test and observe the scale-down (a gradual process), simply delete the temporary pod:

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
    <img width="1904" height="874" alt="Screenshot 2025-10-24 161101" src="https://github.com/user-attachments/assets/a76bcc61-8483-448d-90a7-e742f4928c63" />


2.  **Access Grafana:** Forward the port to access the Grafana GUI locally:

<img width="1900" height="863" alt="Screenshot 2025-10-24 160835" src="https://github.com/user-attachments/assets/1895bc1e-a909-4342-9c65-94b6e2835b69" />


<img width="1517" height="740" alt="Screenshot 2025-10-24 161029" src="https://github.com/user-attachments/assets/82af1e5f-1694-408c-9675-ebaa12866464" />

<img width="1876" height="868" alt="Screenshot 2025-10-24 160811" src="https://github.com/user-attachments/assets/58319635-3524-450f-bc9a-93c8059b5f22" />



    Access at **`http://localhost:3000`**. Use the default `admin` username and retrieve the password from the Kubernetes secret.

### Alerting Details

  * **Tool:** Alertmanager 
  * **Alert Rule:**
  * All configs added in the repo

  * **Notification:** Alertmanager must be configured (via its Helm values) to integrate with a service like **Email (SMTP)

  *<img width="1637" height="729" alt="Screenshot 2025-10-24 160903" src="https://github.com/user-attachments/assets/4e7e3de7-5a8f-4797-9822-d4ca12a60150" />

  * <img width="1635" height="711" alt="Screenshot 2025-10-24 160926" src="https://github.com/user-attachments/assets/ad9d8229-4e8b-4d3c-b71c-624ae48cbfeb" />


  * **Example Threshold:** An alert is configured to fire if the application's CPU utilization exceeds **50%** for a sustained period.
    <img width="1257" height="368" alt="Screenshot 2025-10-24 162204" src="https://github.com/user-attachments/assets/0d1a2cc4-2bf8-4a3c-acb9-6abb81258584" />

 

<!-- end list -->

