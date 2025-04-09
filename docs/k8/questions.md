# K8s Deployment Questions

1. Basic steps get familiar with kubectl and k8s (1p)
    1. How to connect to a cluster
		To connect to a Cluster you can use:
        ~~~bash
        kubectl config use-context [CLUSTER_NAME]
        ~~~
        in this picture below I ran `kubectl config use-context docker-desktop` to connect to my local Windows Docker-Desktop Cluster. 
	    ![Pasted image 20250409140833](imgs/Pasted%20image%2020250409140833.png)
    2. What is the context used for?
		A context in Kubernetes ties together a cluster, a user, and a namespace. It's used by kubectl to know where and how to interact with a Kubernetes cluster.
2. Write down the following commands as a cheat sheet for kubectl: (4p)
    1. Get all pods for all namespaces
	    `kubectl get pods --all-namespaces`
	    ![Pasted image 20250409140938](imgs/Pasted%20image%2020250409140938.png)
    2. Get all nodes
	    `kubectl get nodes`
	    ![Pasted image 20250409141000](imgs/Pasted%20image%2020250409141000.png)
    3. Get all services for all namespace
	    `kubectl get svc --all-namespaces`
	    ![Pasted image 20250409141014](imgs/Pasted%20image%2020250409141014.png)
    4. Run a nginx pod directly with kubectl
	    `kubectl run nginx --image=nginx`
	    ![Pasted image 20250409141028](imgs/Pasted%20image%2020250409141028.png)
    5. Access the container logs of the nginx pod
	    `kubectl logs nginx`
	    ![Pasted image 20250409141040](imgs/Pasted%20image%2020250409141040.png)
    6. Get a shell into the nginx container
	    `kubectl exec -it nginx -- /bin/bash`
	    ![Pasted image 20250409141051](imgs/Pasted%20image%2020250409141051.png)
    7. Port Forward the nginx container to localhost
	    `kubectl port-forward pod/nginx 8080:80`
	    ![Pasted image 20250409141100](imgs/Pasted%20image%2020250409141100.png)
3. Kubernetes resources (1p)
    1. What are the most common kubernetes resources/objects?
	    Pod: Smallest deployable unit.
		Deployment: Manages ReplicaSets (and thus Pods).
		Service: Stable network endpoint for Pods.
		Ingress: HTTP(S) routing to Services.
		ConfigMap, Secret, PersistentVolume, etc.
    2. What are the different methods to make a service available outside of the k8s cluster?
	    NodePort
	    LoadBalancer
		Ingress
		Port-forward (local dev only)

---
4. Deployment (14p)
    1. Create a deployment for the service container (aka recipe service). (Should include livenessProbes)
    2. Craate a deployment for the postgresql container. (Should include livenessProbes, no need for persistence yet)
    3. Create a service for both deployments.
    4. Create ingress for the recipe service.
    5. (Optional) Create a secret for db password and use it in the deployments. 
We created 6 files and applied it to our local kubectl for testing:
![Pasted image 20250409144556](imgs/Pasted%20image%2020250409144556.png)

After the application we checked if all pods are running:
`kubectl get pods`
![Pasted image 20250409144618](imgs/Pasted%20image%2020250409144618.png)

After that we checked the services:
`kubectl get svc`
![Pasted image 20250409144634](imgs/Pasted%20image%2020250409144634.png)

To confirm that our livenessProbes are working we let the pods run for a bit:
![Pasted image 20250409144820](imgs/Pasted%20image%2020250409144820.png)

As we can observe after 8 minutes of running there were no restarts or crashed in to be seen through `kubectl describe pod <pod name>` so they are running fine.

To test that the recipe-service is running correctly we forwarded the port to 8080:

`kubectl port-forward service/recipe-service 8080:80`
![Pasted image 20250409144844](imgs/Pasted%20image%2020250409144844.png)

Then opened our browser with the url “localhost:8080/health” and got a HTTP Status Code 200 confirming the service is running correctly.

![Pasted image 20250409144854](imgs/Pasted%20image%2020250409144854.png)




5. Security (5p)
    1. What are some common security concerns in a Kubernetes environment, and how can they be addressed?

|Concern|Description|Solution|
|---|---|---|
|Over-permissive RBAC|Users/pods might have more privileges than needed|Use least privilege via roles and role bindings|
|Secret leakage|Secrets may be exposed in plaintext or logs|Store secrets in Kubernetes Secrets, use volumeMounts, and enable encryption at rest|
|Running containers as root|Increases risk of container breakout|Use securityContext to drop root privileges|
|Unrestricted service exposure|Services (e.g. databases) may be exposed to the public|Use Ingress + firewall rules; avoid LoadBalancer on internal services|
|Image vulnerabilities|Pulling untrusted images can introduce exploits|Use signed, scanned images from trusted sources (e.g., Trivy, GHCR)|
|Pod-to-pod traffic unrestricted|Any pod can talk to any other pod|Apply NetworkPolicies|
    2. Create service account via a yaml file
    3. Create role and rolebinding(should bind to the service account) which can read all pods in the default namespace via yaml file
    4. Start a pod with kubectl installed in a interactive shell and try if can get all pods in this namespace. (Tip: Add Service Account to run command `--overrides='{ "spec": { "serviceAccount": "<name>" }  }'` 

Its all working:
![Pasted image 20250409150537](imgs/Pasted%20image%2020250409150537.png)