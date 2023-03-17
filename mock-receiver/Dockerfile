# create spec
FROM alpine:latest as spec

RUN apk add jq

COPY "gp-connect-appointments-management-fhir.json" ./

# Spec shouldn't have healthceck endpoint. We're adding it to the finalised spec
COPY "health-status-endpoint.json" ./
RUN jq ".paths+=$(cat health-status-endpoint.json)" gp-connect-appointments-management-fhir.json > updated-spec.json


#Second stage: use spec in Prism
FROM stoplight/prism:latest
COPY --from=spec  /updated-spec.json  /usr/src/prism/packages/cli/gp-connect-appointments-management-fhir/specification/gp-connect-appointments-management-fhir.json

CMD ["mock" , "-h", "0.0.0.0", "-p" ,"9000" ,"gp-connect-appointments-management-fhir/specification/gp-connect-appointments-management-fhir.json"]
