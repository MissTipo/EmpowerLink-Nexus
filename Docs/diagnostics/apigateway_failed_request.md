**Step 1 – Reproduce and Scope the Issue**

-Try the failing request yourself with curl or Postman.

-Confirm the exact error: is it a 4xx (bad request), 5xx (server issue), or a timeout?

-Check if the failure affects all routes or just a specific service (e.g. /graphql works but /ussd fails).

**Step 2 – Check the Gateway Logs**

-Look at the API Gateway’s container logs (kubectl logs <pod>) to see if the request even reaches it.

-If there’s no trace, it might be an ingress/Kong issue.

-If it’s logged but errors, note whether it’s a routing problem (service map mismatch, bad URL) or a downstream error.

**Step 3 – Verify the Service Map / Config**

-Confirm the target service’s entry in the service_map dict (e.g. correct URL, port).

-Check the Kong ingress resource for matching paths.

-Look out for typos, path mismatches, or strip-path issues.

**Step 4 – Test Service Reachability Directly**

-Port-forward to the service (kubectl port-forward svc/telephony-integration 8003:8003) and hit it directly.

-If the service itself works, the issue is at the gateway/ingress level.

-If the service fails even directly, the bug is inside that service.

**Step 5 – Inspect Network/Ingress Layer**

-Check Kong ingress logs/events (kubectl describe ingress api-gateway-ingress).

-Verify the service is correctly registered in Kubernetes (kubectl get svc) and endpoints are ready (kubectl get endpoints).

-Make sure TLS and annotations (like strip-path) aren’t interfering.

**Step 6 – Narrow Down Root Cause**

-If gateway → service routing is misconfigured, fix the path/service_map.

-If service is unhealthy, fix the service.

-If ingress misroutes, adjust the ingress rule.

```
**TLDR**:
Start by reproducing the error, then check the gateway logs to see if the request arrives.
Next, validate the service map and ingress config, then try hitting the service directly
to separate gateway vs service bugs. Finally, check Kong and Kubernetes events for misrouting or
unhealthy endpoints.
Move layer by layer from ingress → gateway → service until the failure is isolated.
```
