<a href="OperatingMIPFederation.md#SynchronizingKeycloakRoles">Operating the MIP Federation</a> -> `Synchronizing the KeyCloak Roles`

# Synchronizing the KeyCloak Roles
The Authentication (AuthN) and the authorization (AuthZ) processes of the MIP are managed by *KeyCloak*, which is usually, as the opposite of the *Local* MIP, an **external** service, which is by default in the EBRAINS infrastructure.  
The roles are taken into account by the MIP Web interface, each role name being parsed and then checked to show (or not) certain items (features, pathologies, datasets...)  
Then, within a federation, which may have many different pathologies and datasets, amongst many different nodes, the number of roles can rapidly increase, and also, each time you change anything related to these things, you will have to change roles accordingly into the KeyCloak interface (to have an idea of the MIP-related roles naming convention, read this [guide](../../documentation/UserAuthorizations.md).

The KeyCloak's interface is excruciatingly slow and clearly not ergonomic at all. Additionally, it's way not MIP-comprehensive. All this will make you lose a considerable amount of time, and with the complexity and sensitivity of this process, you will probably do mistakes as well!

In an attempt to drastically reduce the required time to do this, and also eliminate the risk of human errors, a roles synchronization script has been written, and is introduced into the *mip-deployment* starting with the MIP 6.5 release.  
This script should be automatically installed in the **pusher** node, as it **has** to be executed from there!

### Preparing the *realm-management* client and the *realmadmin* realm user in KeyCloak
Prior to run anything here, you need to make sure that the KeyCloak server's *realm* is ready to be used by the script. In other words, the *keycloak_roles_sync.py* script needs a realm client (with certain configurations and roles) and a realm user (using this realm client).  
For that purpose, you will need to use a KeyCloak Administrator who has all the required privileges to fully manage the realm.

In order to do this, follow this <a id="PreparingKeycloak" href="PreparingKeycloakRealmClient.md">guide</a>.

### Exporting the MIP Federation data structure
As the synchronization script will use a JSON file representing the federation structure (nodes, pathologies, datasets), we have to generate this file with the *mip* script, prior to using the *keycloak_roles_sync.py* script.  

In the *tmux* session (opened as **mipadmin** user), in the **pusher** window (#0)
```
mip --pusher --federation <FEDERATION_NAME> --export-data-structure data consolidate > mip_data_structure.json
```
The *mip_data_structure.json* can be any other file you want.  
Obviously, you'll have to **re**-run this anytime you will change **anything** about the
* nodes (adding or removing a node, or changing its hostname)
* pathologies (adding, removing or renaming or moving from/to any node)
* datasets (adding, removing, or renaming, or moving from/to any node)

### Using the *keycloak_roles_sync.py* script
In the *tmux* session (opened as **mipadmin** user), in the **pusher** window (#0)
```
keycloak_roles_sync.py --admin-client-secret <ADMIN_CLIENT_SECRET> --admin-password '<ADMIN_PASSWORD>' --sync-client-id '<SYNC_CLIENT_ID>' --data-structure-json-file mip_data_structure.json
```

For this script, the different parameters are
|Parameter|Description|Mandatory|
| -- | -- | -- |
|*--server-url* \<SERVER_URL>*|KeyCloak server URL (if different from the default EBRAINS one)||
|*--realm-name \<REALM_NAME>*|KeyCloak Realm name (if different from the default EBRAINS one)||
|*--admin-client-id \<ADMIN_CLIENT_ID>*|KeyCloak Realm Administrator client-id (if different from the default EBRAINS one)||
|*--admin-client-secret \<ADMIN_CLIENT_SECRET>*|KeyCloak Realm Administrator client-secret|**yes**|
|*--admin-username \<ADMIN_USERNAME>*|KeyCloak Realm Administrator username (if different from the default EBRAINS one)||
|*--admin-password '\<ADMIN_PASSWORD>'*||**yes**|
|*--sync-client-id \<SYNC_CLIENT_ID>*|KeyCloak Realm client-id to create/synchronize. You are strongly encourage to use the MIP Federation name here!|**yes**|
|*--copy-users-from-client-id \<CLIENT_ID_TO_COPY_FROM>*|If you want to copy the user/group relationships from another client/group_prefix||
|*--data-structure-json-file \<DATA_STRUCTURE_JSON_FILE>*|JSON data structure file to use as a pattern for roles/groups creation/synchronization|**yes**|

Alternatively, you can generate the JSON structure with the *mip* script, and then, "pipe" it to the *keycloak_roles_sync.py* script. In this sense, the last parameter here is not "really" mandatory.  
This should look like
```
mip --pusher --federation <FEDERATION_NAME> --export-data-structure data consolidate | keycloak_roles_sync.py --admin-client-secret <ADMIN_CLIENT_SECRET> --admin-password '<ADMIN_PASSWORD>' --sync-client-id '<SYNC_CLIENT_ID>'
```
