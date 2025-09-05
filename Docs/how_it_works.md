**Step 1 – Client Request**

- A client (say a mobile app or USSD gateway) sends a request to 159.203.54.10.nip.io.

- The request includes the path (e.g. /graphql or /ussd).

**Step 2 – Ingress & Kong**

- Kubernetes Ingress picks up the request since it’s bound to the kong ingress controller.

- Kong checks the ingress rules you defined:

- If path is /graphql → forward to api-gateway:8000.

- If path is /ussd → forward to telephony-integration:8003.

- Kong enforces plugins (e.g. CORS, timeouts) and handles TLS via Let’s Encrypt.

**Step 3 – API Gateway Service**

- For /graphql, the API Gateway pod receives the request.

- Inside, the gateway consults the service_map dict to determine which microservice should handle the query.

- It forwards the request to the correct internal service (e.g. user-profile, organization-profile, telephony-integration).

**Step 4 – Target Microservice**

- The chosen microservice (say user-profile-service) receives the request.

- FastAPI + Ariadne handle parsing, validate input, and run the resolver/mutation logic.

- The service may query PostgreSQL or Redis if needed.

**Step 5 – Response Flow Back**

- The microservice returns a response (JSON or GraphQL result) to the API Gateway.

- The gateway sends it back to Kong.

- Kong returns the response to the client over TLS.

**Step 6 – Client Sees Result**

The client gets the response, whether that’s a GraphQL payload or a USSD menu screen.
