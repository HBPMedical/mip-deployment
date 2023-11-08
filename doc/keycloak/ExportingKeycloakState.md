### Exporting Keycloak state (Users/Roles/Groups)

You can use this command:
```
docker exec -it {CONTAINER_ID} /opt/jboss/keycloak/bin/standalone.sh -Djboss.socket.binding.port-offset=100 -Dkeycloak.migration.action=export -Dkeycloak.migration.provider=singleFile  -Dkeycloak.migration.realmName=MIP -Dkeycloak.migration.usersExportStrategy=REALM_FILE -Dkeycloak.migration.file=/tmp/mip.json
```

The configurations will be saved on the `keycloak.json` file in the `config/keycloak` folder.