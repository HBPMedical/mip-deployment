[Operating MIP Federation](OperatingMIPFederation.md#PreparingKeycloak) -> `Preparing KeyCloak Realm's Client`

# Preparing KeyCloak Realm's Client
1. Preparing KeyCloak realm's client

   In the KeyCloak's interface, you will have to create a client (**realm-management** in our case) which has
   * *openid-connect* Client Protocol
   * *confidential* Access Type
   * *Direct Access Grants Enabled*
   * *Service Accounts Enabled*
   * *Valid Redirect URIs* set to "*"

   Then, in its roles, prepare the following *Roles*
   * *create-client*
   * *impersonation*
   * *manage-authorization*
   * *manage-clients*
   * *manage-events*
   * *manage-identity-providers*
   * *manage-realm*
   * *manage-users*
   * *query-clients*
   * *query-groups*
   * *query-realms*
   * *query-users*
   * *view-authorization*
   * *view-events*
   * *view-identity-providers*
   * *view-realm*

   Also, you'll have to prepare "composite" *Roles*
   * *view-clients*, containing the following *realm-management* client's roles
     * *query-clients*
   * *view-users*, containing the following *realm-management* client's roles
     * *query-groups*
     * *query-users*
   * *realm-admin*, containing the following *realm-management* client's roles
     * *create-client*
     * *impersonation*
     * *manage-authorization*
     * *manage-clients*
     * *manage-events*
     * *manage-identity-providers*
     * *manage-realm*
     * *manage-users*
     * *query-clients*
     * *query-groups*
     * *query-realms*
     * *query-users*
     * *view-authorization*
     * *view-clients* (previously created composite role)
     * *view-events*
     * *view-identity-providers*
     * *view-realm*
     * *view-users* (previously created composite role)

   Then, you'll have to prepare *Mappers*
   * *Client ID*
     |Parameter|Value|
     | -- | -- |
     |*Mapper Type*|*User Session Note*|
     |*User Session Note*|*clientId*|
     |*Token Claim Name*|*clientId*|
   * *Client IP Address*
     |Parameter|Value|
     | -- | -- |
     |*Mapper Type*|*User Session Note*|
     |*User Session Note*|*clientAddress*|
     |*Token Claim Name*|*clientAddress*|
   * *Client Host*
     |Parameter|Value|
     | -- | -- |
     |*Mapper Type*|*User Session Note*|
     |*User Session Note*|*clientHost*|
     |*Token Claim Name*|*clientHost*|

   Finally, you'll have to prepare the following *Service Account Roles*, *Client Roles*
   * *account*
     * *manage-account* (composite role which contains "*manage-account-links*" *account* client's role)
   * *realm-management*
     * All the roles
1. Preparing KeyCloak realm's admin user

   Here, you just have to create a simple user, without any role, **realmadmin**, in our case
