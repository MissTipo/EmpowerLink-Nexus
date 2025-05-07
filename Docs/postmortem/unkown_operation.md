# 📑 EmpowerLink Nexus: 16-Hour Debugging Postmortem

**Date:** May 6, 2025  
**Author:** Dorine Tipo  

---

## 🎯 Summary  

A series of cascading infrastructure misconfigurations and oversights resulted in a 16+ hour debugging marathon while setting up live GraphQL data for UI graphs. The root causes included missing services, inconsistent IP addressing, namespace misalignment, image deployment mismatches, and CORS misconfigurations.

---

## 📌 Timeline & Issues  

1. **Google Cloud Service Deletion**
   - All existing services were unexpectedly deleted by Google Cloud.
   - **Action:** Migrated to DigitalOcean Kubernetes.
   - **Impact:** Full CI/CD migration and service redeployment.

2. **GraphQL “Unknown Operation” Error**
   - Schema, resolvers, and API Gateway configs were confirmed correct.
   - Discovered inclusivity index service lacked Redis — even though it was listed in `requirements.txt`.
   - **Cause:** Deployment workflow wasn’t replacing images due to filename mismatch.
   - **Fix:** Corrected workflow file names and cleaned up old deployments.

3. **Internal Curl Worked, External Did Not**
   - Deployed Kong via Helm.
   - Initially missing Admin API — later added.
   - Still faced “unknown operation” externally.
   - **Cause:** Old external IP from previous Kong instance was still being used.

4. **Nip.io IP Mismatch**
   - New Kong external IP wasn’t registered with nip.io.
   - **Fix:** Updated nip.io to point to the new IP.

5. **CORS Error**
   - New issue after IP fix: CORS error appeared.
   - **Cause:** Incorrect `http` URI used in the frontend instead of `https`.
   - **Complication:** CORS plugins were already active on Ingress and Kong, leading to namespace confusion.

6. **Namespace Swapping & Route Mismatch**
   - Swapped Ingress from `default` to `kong` namespace.
   - Deployed API Gateway attached to both namespaces.
   - **Root Cause of “failure to get a peer from the ring-balancer” error:**  
     Kong Ingress in `kong` namespace lacked an external IP while the frontend was routing through it.

7. **Final Fix**
   - Deleted redundant `kong` namespace Ingress.
   - Cleaned up stale routes.
   - API Gateway correctly routed through `default` namespace’s Ingress with external IP.
   - Confirmed CORS headers via `curl -i -X OPTIONS`.
   - End-to-end success.

---

## 📊 Impact  

- 16 hours of cumulative debugging and infrastructure adjustments.
- Temporary unavailability of public endpoints.
- Repeated redeployments and configuration updates.
- Blocked frontend live data integration for graphs.

---

## 🔍 Root Causes  

- Service loss due to cloud provider wipe.
- Image deployment workflow bugs.
- IP address misalignment post-redeployment.
- Namespace inconsistency in Kong Ingress.
- Frontend URI misconfiguration causing misleading CORS errors.
- Overlapping Ingresses in multiple namespaces without clear separation of concerns.

---

## ✅ What Went Well  

- Consistent, systematic debugging.
- Quick adaptation to DigitalOcean platform.
- Solid use of `curl` and Kong Admin API for visibility.
- Redis issue discovered and resolved during investigation.
- Maintained composure through incremental troubleshooting.

---

## ❌ What Could Have Gone Better  

- Automating dynamic retrieval and configuration of external IP post-redeployment.
- Consolidating Kong Ingress resources to a single namespace.
- CI/CD workflow should enforce image pull policy and delete old deployments explicitly.
- Improved logging and monitoring during migration.

---

## 📌 Action Items  

| Task | Owner | Priority |
|:------|:------|:------|
| Automate external IP registration to nip.io in CI/CD | Dorine | High |
| Refactor Kong Ingress to run exclusively in `default` or dedicated `infra` namespace | Dorine | Medium |
| Add strict image pull policy and post-deploy cleanup job | Dorine | High |
| Improve frontend config management for environment-based URIs | Dorine | Medium |
| Write detailed docs for service recovery/migration checklist | Dorine | Medium |

---

**Note:** This experience reinforced the importance of **infrastructure state consistency, explicit resource naming, dynamic config management, and clean separation of deployment concerns**.

---


