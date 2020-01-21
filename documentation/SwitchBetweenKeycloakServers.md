#### Switch between different keycloak servers 
In order to switch between keycloak servers you will need to change some environment variables  

in docker-compose.yml 

Example setup: 

(if your keycloak is setup in IP: https://iam.humanbrainproject.eu with clientid : medical-informatics-platform, clientsecret: SaNJbC2YFHPhPM-tGiJ1b7tmAA): 
portalbackend: 
…. 

environment: 
CLIENT_ID: medical-informatics-platform 

CLIENT_SECRET:SaNJbC2YFHPhPM-tGiJ1b7tmAA 

AUTH_URI: "https://iam.humanbrainproject.eu/auth/realms/MIPTEST/protocol/openid-connect/auth" 

USER_INFO_URI: "https://iam.humanbrainproject.eu/auth/realms/MIPTEST/protocol/openid-connect/userinfo" 

TOKEN_URI: "https://iam.humanbrainproject.eu/auth/realms/MIPTEST/protocol/openid-connect/token" 

KEYCLOAK_URL: "https://iam.humanbrainproject.eu" 



Then to change and use a local keycloak server (located in e.g. 88.197.53.106 = keycloakUrl) change variables to: 

CLIENT_ID: *new_client_id* 

CLIENT_SECRET:*new_client_secret* 

AUTH_URI: "https://keycloakUrl:8095/auth/realms/MIP/protocol/openid-connect/auth" 

USER_INFO_URI: "https://keycloakUrl:8095/auth/realms/MIP/protocol/openid-connect/userinfo" 

TOKEN_URI: "https://keycloakUrl:8095/auth/realms/MIP/protocol/openid-connect/token" 

LOGOUT_URI: https://keycloakUrl:8095/auth/realms/MIP/protocol/openid-connect/logout 

KEYCLOAK_URL: "keycloakUrl" 

#### Change certificate 
Once you switch to a local keycloak you can also use your own self signed certificate.

Just replace the already existing

./certs/tls.key
and
./certs/tls.crt

with your own.

