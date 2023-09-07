#!/usr/bin/env python3

# In the Keycloak's realm, we need to have
# - a client (realm-management), which has "openid-connect" Client Protocol, "confidential" Access Type, "Direct Access Grants Enabled", "Service Accounts Enabled", "Valid Redirect URIs" *,
#   with roles:
#       create-client, impersonation, manage-authorization, manage-clients, manage-events, manage-identity-providers, manage-realm, manage-users, query-clients, query-groups,
#       query-realms, query-users, view-authorization, view-events, view-identity-providers, view-realm
#   with composite roles:
#       - realm-admin (with "realm-management" client roles: create-client, impersonation, manage-authorization, manage-clients, manage-events, manage-identity-provider,
#                                                           manage-realm, manage-users, query-clients, query-groups, query-realms, query-users, view-authorization,
#                                                           view-clients, view-events, view-identity-providers, view-realm, view-users)
#       - view-clients (with "realm-management" client roles: query-clients)
#       - view-users (with "realm-management" client roles: query-groups, query-users)
#   with mappers:
#       - Client ID (with "User Session Note" mapper type, "clientId" user session note, "clientId" token claim name)
#       - Client IP Address (with "User Session Note" mapper type, "clientAddress" user session note, "clientAddress" token claim name)
#       - Client Host (with "User Session Note" mapper type, "clientHost" user session note, "clientHost" token claim name)
#   with Service Account Roles:
#       - "account" client roles: manage-account, manage-account-links, view-profile
#       - "realm-management" client roles: everything
# - a simple user, without any role (realmadmin, in our case)
#
# https://github.com/marcospereirampj/python-keycloak
# https://www.keycloak.org/docs-api/8.0/rest-api/index.html

import os
import sys
import json
import select
import pprint
import argparse

pp = pprint.PrettyPrinter(indent=4)

from keycloak.exceptions import raise_error_from_response, KeycloakGetError
from keycloak.urls_patterns import URL_ADMIN_CLIENT_ROLE
from keycloak import KeycloakAdmin

class MIPKeycloakAdmin(KeycloakAdmin):
    _realm = None
    _verbose_level = 0

    def __init__(self, server_url, username=None, password=None, realm_name='master', client_id='admin-cli', verify=True,
                    client_secret_key=None, custom_headers=None, user_realm_name=None, auto_refresh_token=None, verbose_level=0):

        super().__init__(server_url, username=username, password=password, realm_name=realm_name, client_id=client_id, verify=verify,
                client_secret_key=client_secret_key, custom_headers=custom_headers, user_realm_name=user_realm_name, auto_refresh_token=auto_refresh_token)

        self._verbose_level = verbose_level
        self._realm = self.get_realm(realm_name)

    def get_realm(self, realm_id):
        realm = None

        realms = self.get_realms()
        for tmpRealm in realms:
            if tmpRealm['id'] == realm_id:
                realm = tmpRealm

        return realm

    def get_realm_default_groups(self):
        if self._realm is not None and 'defaultGroups' in self._realm:
            return self._realm['defaultGroups']

    def set_realm_default_groups(self, groups):
        result = False

        if self._realm is not None and 'defaultGroups' in self._realm:
            payload = {}
            payload['defaultGroups'] = []
            for group in groups:
                if not group.startswith('/'):
                    group = '/' + group
                if group not in payload['defaultGroups']:
                    payload['defaultGroups'].append(group)

            if len(payload['defaultGroups']) > 0:
                result = self.update_realm(self._realm['id'], payload)
                if isinstance(result, dict) and len(result.keys()) > 0:
                    result = True
                else:
                    result = False
            self._realm = self.get_realm(self._realm['id'])

        return result

    def get_composite_client_roles_of_role(self, client_id, role_name):
        return self._get_composite_client_roles_of_role(URL_ADMIN_CLIENT_ROLE + '/composites', client_id, role_name)

    def _get_composite_client_roles_of_role(self, client_roles_composite_url, client_id, role_name):
        params_path = {'id': client_id, 'realm-name': self.realm_name, 'role-name': role_name}
        data_raw = self.raw_get(client_roles_composite_url.format(**params_path))
        return raise_error_from_response(data_raw, KeycloakGetError)

    def get_roles_list(self, client_id=None, role_name=None):
        roles_list = None

        roles = []
        member_of_composite = []

        if role_name is not None:
            role = None
            if client_id is None:
                role = self.get_realm_role(role_name)
            else:
                role = self.get_client_role(client_id, role_name)

            if role is not None:
                if role['composite'] is True:
                    if client_id is None:
                        roles = self.get_composite_realm_roles_of_role(role_name)
                    else:
                        roles = self.get_composite_client_roles_of_role(client_id, role_name)
        else:
            if client_id is None:
                roles = self.get_realm_roles()
            else:
                roles = self.get_client_roles(client_id)

        for role in roles:
            if roles_list is None:
                roles_list = []
            role_dict = {'name': role['name'], 'composite': role['composite']}
            if role['composite'] is True:
                roles_composite = self.get_roles_list(client_id, role['name'])
                if roles_composite is not None:
                    role_dict['composites'] = roles_composite

            roles_list.append(role_dict)

        roles_list = self.roles_list_to_dict(roles_list)

        return roles_list

    def roles_list_to_dict(self, roles_list, depth=0):
        import collections

        children_of_composite_role = []
        sorted_roles_dict = collections.OrderedDict()

        for role in roles_list:
            if not isinstance(role, dict):
                role = {'name': role}
            if 'composites' in role and role['name'] not in sorted_roles_dict:
                sorted_roles_dict[role['name']], children = self.roles_list_to_dict(role['composites'], depth+1)
                if len(children) > 0:
                    for child in children:
                        if child not in children_of_composite_role:
                            children_of_composite_role.append(child)
            else:
                sorted_roles_dict[role['name']] = role['name']
                if depth > 0:
                    children_of_composite_role.append(role['name'])

        if depth == 0:
            for child in children_of_composite_role:
                if child in sorted_roles_dict:
                    del sorted_roles_dict[child]
            return sorted_roles_dict
        else:
            return sorted_roles_dict, children_of_composite_role

    def _create_client(self, client_name):
        return self.create_client(payload={
            'clientId': client_name,
            'clientAuthenticatorType': 'client-secret',
            'surrogateAuthRequired': False,
            'protocol': 'openid-connect',
            'enabled': True,
            'redirectUris': ['*'],
            'webOrigins': [],
            'bearerOnly': False,
            'consentRequired': False,
            'standardFlowEnabled': True,
            'implicitFlowEnabled': False,
            'directAccessGrantsEnabled': True,
            'serviceAccountsEnabled': False,
            'publicClient': False,
            'fullScopeAllowed': True,
            'frontchannelLogout': False,
            'protocolMappers': [
                {
                    'name': 'clientRole',
                    'protocol': 'openid-connect',
                    'consentRequired': False,
                    'protocolMapper': 'oidc-usermodel-client-role-mapper',
                    'config': {
                        'usermodel.clientRoleMapping.clientId': client_name,
                        'multivalued': True,
                        'userinfo.token.claim': True,
                        'id.token.claim': True,
                        'access.token.claim': True,
                        'claim.name': 'authorities'
                    }
                },
                {
                    'name': 'realmRole',
                    'protocol': 'openid-connect',
                    'consentRequired': False,
                    'protocolMapper': 'oidc-usermodel-realm-role-mapper',
                    'config': {
                        'multivalued': True,
                        'userinfo.token.claim': True,
                        'id.token.claim': True,
                        'access.token.claim': True
                    }
                }
            ]
        },
        skip_exists=True)

    def synchronize_client(self, client_id, pathologies):
        client_id_id = None
        client_secret = None
        result = self._create_client(client_id)
        client_id_id = self.get_client_id(client_id)

        client = self.get_client(client_id_id)
        if client is not None:
            secrets = self.get_client_secrets(client['id'])
            if secrets is not None and 'value' in secrets:
                client_secret = secrets['value']
            if client_secret is not None:
                if self._verbose_level >= 0:
                    print('        client_id: <%s>' %(client['clientId']))
                    print('        client_secret: <%s>' %(client_secret))
                    print()
        else:
            sys.exit('Client <%s> does not exist and cannot be created either!' %(client_id))

        client_roles = [
            {'name': 'DC_ADMIN', 'composite': False, 'description': 'Data catalog administrator'},
            {'name': 'RESEARCH_DATASET_ALL', 'composite': False, 'description': 'All datasets, without distinction'},
            {'name': 'RESEARCH_EXPERIMENT_ALL', 'composite': False},
            {'name': 'RESEARCH_PATHOLOGY_ALL', 'composite': False, 'description': 'All pathologies, without distinction'},
        ]

        full_role_list = []
        for role in client_roles:
            if role['name'] not in full_role_list:
                full_role_list.append(role['name'])

        pathologies_datasets = {}
        for pathology in pathologies:
            dc_control_role = {'name': 'DC_CONTROL_%s' %(pathology['name']), 'composite': False, 'description': 'Data catalog - %s CDE' %(pathology['name'])}
            if dc_control_role['name'] not in full_role_list:
                full_role_list.append(dc_control_role['name'])
                client_roles.append(dc_control_role)

            full_pathology_role_list = []
            pathology_composite_role = {'name': 'RESEARCH_PATHOLOGY_%s' %(pathology['name']), 'composite': True, 'description': '%s pathology composite role' %(pathology['name'])}

            for node in pathology['nodes']:
                dc_hospital_role = {'name': 'DC_HOSPITAL_%s' %(node['name']), 'composite': False, 'description': 'Data catalog - Worker %s hospital' %(node['name'])}
                if dc_hospital_role['name'] not in full_role_list:
                    full_role_list.append(dc_hospital_role['name'])
                    client_roles.append(dc_hospital_role)

                for dataset in node['datasets']:
                    dataset_role = {'name': 'RESEARCH_DATASET_%s' %(dataset['name']), 'composite': False, 'description': '%s - Worker %s' %(pathology['name'], node['name'])}
                    if dataset_role['name'] not in [pathology_dataset_role['name'] for pathology_dataset_role in full_pathology_role_list]:
                        full_pathology_role_list.append(dataset_role)
                    if dataset_role['name'] not in full_role_list:
                        full_role_list.append(dataset_role['name'])
                        client_roles.append(dataset_role)

            if pathology_composite_role['name'] not in full_role_list:
                full_role_list.append(pathology_composite_role['name'])
                client_roles.append(pathology_composite_role)
                if len(full_pathology_role_list) > 0:
                    pathologies_datasets[pathology_composite_role['name']] = full_pathology_role_list

        if client_id_id is not None:
            old_client_roles = self.get_client_roles(client_id=client_id_id)
            if len(old_client_roles) > 0:
                if self._verbose_level >= 2:
                    print('        Deleting existing <%s> client roles...\n' %(client_id))
                for old_role in old_client_roles:
                    result = self.delete_client_role(client_role_id=client_id_id, role_name=old_role['name'])

            for new_role in client_roles:
                new_role['clientRole'] = True
                if self._verbose_level >= 2:
                    print('        Creating <%s> client role: %s (composite: %s)' %(client_id, new_role['name'], new_role['composite']))
                result = self.create_client_role(client_role_id=client_id_id, payload=new_role, skip_exists=False)
                if new_role['composite'] and new_role['name'] in pathologies_datasets:
                    composites = []
                    for composite in pathologies_datasets[new_role['name']]:
                        if self._verbose_level >= 3:
                            print('            Assigning <%s> client role <%s> as a composite of <%s> role' %(client_id, composite['name'], new_role['name']))
                        composite_role = self.get_client_role(client_id_id, composite['name'])
                        composites.append(composite_role)
                    if len(composites) > 0:
                        result = self.add_composite_client_roles_to_role(client_role_id=client_id_id, role_name=new_role['name'], roles=composites)

    def copy_group_members(self, client_id, copy_from_client_id, group_name):
        src_group = None
        dst_group = None
        src_members = None
        dst_members = None

        src_group_name = '%s_%s' %(copy_from_client_id.upper(), group_name)
        src_group = self.get_group_by_path('/%s' %(src_group_name))
        if src_group is not None:
            src_members = self.get_group_members(src_group['id'])

        if src_members is not None:
            dst_group_name = '%s_%s' %(client_id.upper(), group_name)
            dst_group = self.get_group_by_path('/%s' %(dst_group_name))
            if dst_group is not None:
                dst_members = self.get_group_members(dst_group['id'])

                if self._verbose_level >= 3:
                    print('            Copying missing users from source group <%s> to destination group <%s>' %(src_group_name, dst_group_name))
                for src_member in src_members:
                    if dst_members is None or src_member['id'] not in [dst_member['id'] for dst_member in dst_members]:
                        self.group_user_add(src_member['id'], dst_group['id'])

    def _assign_client_roles_to_group(self, client_id, group_name):
        client_id_id = self.get_client_id(client_id)
        dst_group_name = '%s_%s' %(client_id.upper(), group_name)
        dst_group = self.get_group_by_path('/%s' %(dst_group_name))
        if client_id_id is not None and dst_group is not None:
            roles_list = []
            role_names_list = []
            if group_name == 'DC_ADMIN':
                role_names_list = [group_name]
            elif group_name.startswith('DC_HOSPITAL_'):
                role_names_list = [group_name]
            elif group_name == 'PROCESSOR':
                role_names_list = ['RESEARCH_DATASET_ALL', 'RESEARCH_EXPERIMENT_ALL', 'RESEARCH_PATHOLOGY_ALL']
            elif group_name.startswith('CONTROLLER_'):
                pathology = group_name[11:]
                role_names_list = ['DC_CONTROL_%s' %(pathology), 'RESEARCH_PATHOLOGY_%s' %(pathology)]
            elif group_name.startswith('RESEARCHER_'):
                pathology = group_name[11:]
                role_names_list = ['RESEARCH_PATHOLOGY_%s' %(pathology)]
            elif group_name == 'WORKFLOW_ADMIN':
                role_names_list = [group_name]

            for role_name in role_names_list:
                role = self.get_client_role(client_id_id, role_name)
                if role is not None:
                    roles_list.append(role)

            if len(roles_list) > 0:
                for role in roles_list:
                    if self._verbose_level >= 3:
                        print('            Assigning <%s> client role <%s> to realm group: <%s>' %(client_id, role['name'], dst_group_name))
                self.assign_group_client_roles(dst_group['id'], client_id_id, roles_list)

    #def _clean_group(self, client_id, group_name)

    def get_orphan_groups(self):
        result = []

        if hasattr(self, '_orphan_groups') and self._orphan_groups is not None:
            result = self._orphan_groups

        return result

    def _get_client_matching_groups(self, client_id):
        result = []

        groups = self.get_groups()
        for group in groups:
            if group['name'].startswith('%s_' %(client_id.upper())):
                result.append(group)

        return result

    def _group_members_backup(self, group_id):
        result = False

        group = self.get_group(group_id)
        if group is None:
            if self._verbose_level >= 1:
                print('group not found: %s' %(group_id))
            return False
        members_backup = None

        if os.path.isfile(self._group_members_backup_filename):     # If we already find the file at the backup time, we should suspect a previous crash and may find a group members backup inside
            try:
                with open(self._group_members_backup_filename, 'r') as f:
                    members_backup = json.load(f)
            except Exception as e:
                if self._verbose_level >= 0:
                    print(e)
                return False
        if members_backup is None:
            members_backup = {}

        group_members = self.get_group_members(group['id'])
        if group_members is not None and len(group_members) > 0 and group['name'] not in members_backup:
            members_backup[group['name']] = group_members
        else:   # We better not touch the file in this case, as it may be required by the restore method
            members_backup = None

        if members_backup is not None:
            try:
                with open(self._group_members_backup_filename, 'w') as f:
                    if self._verbose_level >= 1:
                        print('        Saving users from destination group <%s> into backup file: <%s>' %(group['name'], self._group_members_backup_filename))
                    json.dump(members_backup, f)
                    result = True
            except Exception as e:
                if self._verbose_level >= 0:
                    print(e)
                return False
        else:
            result = True

        return result

    def _group_members_restore(self, group_id):
        result = False

        group = self.get_group(group_id)
        if group is None:
            return False
        members_backup = None

        if os.path.isfile(self._group_members_backup_filename):
            try:
                with open(self._group_members_backup_filename, 'r') as f:
                    members_backup = json.load(f)
                    f.close()
                    if len(members_backup) == 0:
                        os.remove(self._group_members_backup_filename)
                        members_backup = None
            except Exception as e:
                if self._verbose_level >= 0:
                    print(e)
                return False

        if members_backup is not None and group['name'] in members_backup:
            try:
                dst_members = self.get_group_members(group['id'])
                if self._verbose_level >= 1:
                    print('            Restoring missing users from backup file <%s> to destination group: <%s>' %(self._group_members_backup_filename, group['name']))
                for src_member in members_backup[group['name']]:
                    if dst_members is None or src_member['id'] not in [dst_member['id'] for dst_member in dst_members]:
                        self.group_user_add(src_member['id'], group['id'])

                members_backup.pop(group['name'], None)
                if len(members_backup) == 0 and os.path.isfile(self._group_members_backup_filename):
                    os.remove(self._group_members_backup_filename)
                result = True
            except Exception as e:
                if self._verbose_level >= 0:
                    print(e)
                return False
        else:
            result = True

        return result

    def _consolidate_group(self, client_id, group_name, copy_from_client_id=None):
        result = False

        dst_group_name = '%s_%s' %(client_id.upper(), group_name)
        dst_group = self.get_group_by_path('/%s' %(dst_group_name))
        if dst_group is not None:
            if copy_from_client_id is None:
                result = self._group_members_backup(dst_group['id'])
            else:
                result = True

            if result:
                if self._verbose_level >= 2:
                    print('        Deleting realm group: <%s>' %(dst_group_name))
                self.delete_group(dst_group['id'])

        if self._verbose_level >= 2:
            print('        Creating realm group: <%s>' %(dst_group_name))
        self.create_group(payload={'name': dst_group_name, 'path': '/%s' %(dst_group_name), 'subGroups': []})
        dst_group = self.get_group_by_path('/%s' %(dst_group_name))

        if dst_group is not None:
            self._assign_client_roles_to_group(client_id, group_name)
            if copy_from_client_id is not None:
                self.copy_group_members(client_id, copy_from_client_id, group_name)
            else:
                result = self._group_members_restore(dst_group['id'])

        return result

    def consolidate_groups(self, client_id, pathologies, copy_from_client_id=None):
        realm_id = None
        default_groups = None

        if self._realm is not None:
            realm_id = self._realm['id']

            tmp_default_groups = self.get_realm_default_groups()
            if tmp_default_groups is not None and len(tmp_default_groups) > 0:
                for group in tmp_default_groups:
                    group = group[1:]
                    if default_groups is None:
                        default_groups = []
                    default_groups.append(group)

        self._orphan_groups = []
        self._group_members_backup_filename = '/tmp/kc_group_members_backup.json'
        group_patterns = ['DC_ADMIN', 'DC_HOSPITAL', 'PROCESSOR', 'CONTROLLER', 'RESEARCHER', 'WORKFLOW_ADMIN']

        old_client_matching_groups = self._get_client_matching_groups(client_id)
        sync_client_group_names = []

        for group in old_client_matching_groups:
            match = False
            for pattern in group_patterns:
                group_name = group['name'][len(client_id+'_'):]
                if group_name.startswith(pattern):
                    match = True
                    break
            if not match and group['name'] not in [group['name'] for group in self._orphan_groups]:
                self._orphan_groups.append(group)

        nodes = []
        for base_group_name in group_patterns:
            if base_group_name == 'DC_HOSPITAL':
                for pathology in pathologies:
                    for node in pathology['nodes']:
                        if node['name'] not in nodes:
                            group_name = '%s_%s' %(base_group_name, node['name'])
                            self._consolidate_group(client_id, group_name, copy_from_client_id)
                            sync_client_group_names.append('%s_%s' %(client_id.upper(), group_name))
                            nodes.append(node['name'])
            elif base_group_name in ['CONTROLLER', 'RESEARCHER']:
                for pathology in pathologies:
                    group_name = '%s_%s' %(base_group_name, pathology['name'])
                    self._consolidate_group(client_id, group_name, copy_from_client_id)
                    sync_client_group_names.append('%s_%s' %(client_id.upper(), group_name))
            else:
                self._consolidate_group(client_id, base_group_name, copy_from_client_id)
                sync_client_group_names.append('%s_%s' %(client_id.upper(), base_group_name))

        for group in old_client_matching_groups:
            if group['name'] not in sync_client_group_names and group['name'] not in [group['name'] for group in self._orphan_groups]:
                self._orphan_groups.append(group)

        if default_groups is not None:
            restore_default_groups = False
            for group in sync_client_group_names:
                if group in default_groups and not restore_default_groups:
                    restore_default_groups = True

            if restore_default_groups:
                missing_default_groups = []
                result = self.set_realm_default_groups(default_groups)
                for group in default_groups:
                    if not group.startswith('/'):
                        group = '/' + group
                    if ('defaultGroups' not in self._realm) or ('defaultGroups' in self._realm and group not in self._realm['defaultGroups']):
                        missing_default_groups.append(group[1:])

                if len(missing_default_groups) > 0:
                    if self._verbose_level >= 0:
                        print('ERROR! Impossible to restore the default groups!')
                    for group in missing_default_groups:
                        if self._verbose_level >= 0:
                            print('  THE FOLLOWING DEFAULT GROUP IS NOW MISSING!! YOU REALLY SHOULD RESTORE IT MANUALLY RIGHT NOW: %s' %(group))

def main():
    argsparser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    argsparser.add_argument('-l', '--server-url', dest='server_url', default='https://iam.ebrains.eu', help='Keycloak server base URL', type=str)
    argsparser.add_argument('-r', '--realm-name', dest='realm_name', default='MIP', help='Keycloak Realm name', type=str)
    argsparser.add_argument('-a', '--admin-client-id', dest='admin_client_id', default='realm-management', help='Keycloak Realm Administrator client-id', type=str)
    argsparser.add_argument('-k', '--admin-client-secret', dest='admin_client_secret', help='Keycloak Realm Administrator client-secret', type=str)
    argsparser.add_argument('-u', '--admin-username', dest='admin_username', default='realmadmin', help='Keycloak Realm Administrator username', type=str)
    argsparser.add_argument('-p', '--admin-password', dest='admin_password', help='Keycloak Realm Administrator password', type=str)
    argsparser.add_argument('-s', '--sync-client-id', dest='sync_client_id', help='Keycloak Realm client-id to create/synchronize. Commonly MIP federation name. Will be used as group prefix as well.', type=str)
    argsparser.add_argument('-c', '--copy-users-from-client-id', dest='copy_from_client_id', help='If you want to copy the user/group relationships from another client/group_prefix', type=str)
    argsparser.add_argument('-i', '--data-structure-json-file', dest='data_structure_json_file', default=sys.stdin, nargs='?', help='JSON data structure file to use as a pattern for roles/groups creation/synchronization', type=argparse.FileType('r'))
    argsparser.add_argument('-v', dest='verbose_level', action='count', default=0, help='Verbose level')

    args = argsparser.parse_args()
    args = vars(args)

    params_keys = []
    for key in args.keys():
        params_keys.append(key)
    for key in params_keys:
        if args[key] is None or args[key] == '':
            args.pop(key)
    if 'copy_from_client_id' not in args:
        args['copy_from_client_id'] = None

    for arg in ['server_url', 'realm_name', 'admin_client_id', 'admin_client_secret', 'admin_username', 'admin_password', 'sync_client_id']:
        if arg not in args:
            sys.exit('Missing required argument: <%s>' %(arg))

    pathologies = None
    keycloak_adm = None
    if 'data_structure_json_file' in args:
        #if args['data_structure_json_file'] is sys.stdin:
        #    if not select.select([sys.stdin,],[],[],0.0)[0]:
        #        sys.exit('Missing JSON input!')
        try:
            pathologies = json.load(args['data_structure_json_file'])
            args['data_structure_json_file'].close()
        except Exception as e:
            sys.exit(e)

    if pathologies is not None:
        try:
            keycloak_adm = MIPKeycloakAdmin(server_url=args['server_url'] + '/auth/',
                                            username=args['admin_username'],
                                            password=args['admin_password'],
                                            realm_name=args['realm_name'],
                                            user_realm_name=None,
                                            client_id=args['admin_client_id'],
                                            client_secret_key=args['admin_client_secret'],
                                            verify=True,
                                            verbose_level=args['verbose_level'])
        except Exception as e:
            sys.exit(e)

    if keycloak_adm is not None:
        if args['verbose_level'] >= 0:
            print('Synchronizing <%s> client in Keycloak <%s> realm (on server <%s>), connecting with realm admin user <%s> (realm admin client <%s>)...' %(args['sync_client_id'], args['realm_name'], args['server_url'], args['admin_username'], args['admin_client_id']))
        users_count = keycloak_adm.users_count()
        if args['verbose_level'] >= 1:
            print('    There are %s users on this realm' %(users_count))

        if args['verbose_level'] >= 0:
            print('    Synchronizing client <%s>...' %(args['sync_client_id']))
        keycloak_adm.synchronize_client(args['sync_client_id'], pathologies)
        if args['verbose_level'] >= 0:
            print('    Consolidating <%s> realm groups...' %(args['realm_name']))
        keycloak_adm.consolidate_groups(args['sync_client_id'], pathologies, copy_from_client_id=args['copy_from_client_id'])

        orphan_groups = keycloak_adm.get_orphan_groups()
        if len(orphan_groups) > 0:
            if args['verbose_level'] >= 0:
                print('\n\n')
            for orphan_group in orphan_groups:
                if args['verbose_level'] >= 0:
                    print('WATCH OUT! Orphan group (does not match the client group naming convention). You may be wanting to delete it: %s' %(orphan_group['name']))

if __name__ == '__main__':
    main()
