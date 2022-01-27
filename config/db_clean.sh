#!/usr/bin/env bash

PATHOLOGY=""
DOCKER_COMPOSE_FILE=""
DRY_RUN=0
CREATE_DBS_CONTAINER_NAME="create_dbs"

help(){
	cat <<EOF
Usage: $0 [OPTION]
This script will delete the MIP portalbackend DB experiments which don't target the selected pathology(-ies).
Then, it will also delete the users who are not referenced in the experiments anymore.

	OPTION
	======
	--pathology|-p [PATHOLOGY(-IES)]			Pathology(-ies) to keep in the DB. Multiple pathologies must be comma-separated.
	--docker-compose|-d [DOCKER_COMPOSE_FILE]		Path to the docker-compose.yml file from which the script will get the container name and the DB connection details.
	--dry-run|-r				Inspect what will be kept.
	--help|-h						Prints this help page
EOF
}

POSITIONAL=()
while [[ $# -gt 0 ]]; do
	case $1 in
		--pathology|-p)
			if [[ "$2" != "" ]]; then
				PATHOLOGY=$2
				shift
			fi
			shift
			;;
		--docker-compose|-d)
			if [[ -f $2 && "$(cat $2|grep $CREATE_DBS_CONTAINER_NAME)" != "" ]]; then
				DOCKER_COMPOSE_FILE=$2
				shift
			else
				echo "Invalid docker-compose file!" >/dev/stderr
				exit 1
			fi
			shift
			;;
		--dry-run|-r)
			DRY_RUN=1
			shift
			;;
		--help|-h)
			help
			exit 0
			;;
		*)
			POSITIONAL+=("$1")
			shift
			;;
	esac
done
set -- "${POSITIONAL[@]}"



queries=()
if [[ "$PATHOLOGY" != "" ]]; then
	experiment_where=""
	while IFS=$'\n' read -r pathology; do
		if [[ "$experiment_where" != "" ]]; then
			experiment_where+=" AND "
		fi
		experiment_where+="NOT algorithm::JSONB->'parameters' @> '[{\"name\": \"pathology\", \"value\": \"$pathology\"}]' AND NOT algorithm::JSONB->'parameters' @> '[{\"label\": \"pathology\", \"value\": \"$pathology\"}]'"
	done <<< "$(echo $PATHOLOGY | tr ',' '\n')"

	user_where="public.user.username NOT IN (SELECT DISTINCT created_by_username FROM experiment)"

	if [[ $DRY_RUN -eq 1 ]]; then
		field="dataset"
		query="SELECT
				${field}
			FROM (
				SELECT
					jsonb_array_elements(parameters::JSONB)->'name' AS name,
					jsonb_array_elements(parameters::JSONB)->'value' AS ${field}
				FROM (
					SELECT
						algorithm::JSONB->'parameters'
					FROM
						experiment
					WHERE
						${experiment_where}
				) algorithm(parameters)
			) res
			WHERE
				name = '\"${field}\"'"
		#query="SELECT algorithm::JSON->'parameters' FROM experiment WHERE ${experiment_where}"
		queries+=("$query")

		queries+=("SELECT username FROM public.user WHERE ${user_where}")
	else
		queries+=("SELECT COUNT(*) AS experiments_to_be_deleted FROM experiment WHERE ${experiment_where}")
		queries+=("DELETE FROM experiment WHERE ${experiment_where}")

		queries+=("SELECT COUNT(*) AS users_to_be_deleted FROM public.user WHERE ${user_where}")
		queries+=("DELETE FROM public.user WHERE ${user_where}")
	fi
else
	help
	exit 1
fi

DB_HOST=""
DB_PORT=""
DB_NAME=""
DB_USER=""
if [[ ${#queries} -gt 0 && "$DOCKER_COMPOSE_FILE" != "" ]]; then
	cmd="psql"
	params=()

	DB_HOST=localhost
	params+=("-h $DB_HOST")

	DB_PORT=$(cat $DOCKER_COMPOSE_FILE | grep -A10 "${CREATE_DBS_CONTAINER_NAME}:" | grep "DB_PORT: " | awk '{print $NF}')
	if [[ "$DB_PORT" != "" ]]; then
		params+=("-p $DB_PORT")
	fi

	DB_NAME=$(cat $DOCKER_COMPOSE_FILE | grep -A10 "${CREATE_DBS_CONTAINER_NAME}:" | grep "DB4: " | awk '{print $NF}')
	if [[ "$DB_NAME" != "" ]]; then
		params+=("-d $DB_NAME")
	fi

	DB_USER=$(cat $DOCKER_COMPOSE_FILE | grep -A10 "${CREATE_DBS_CONTAINER_NAME}:" | grep "DB_ADMIN_USER: " | awk '{print $NF}')
	if [[ "$DB_USER" != "" ]]; then
		params+=("-U $DB_USER")
	fi
fi

if [[ "$DB_HOST" != "" && "$DB_PORT" != "" && "$DB_NAME" != "" && "$DB_USER" != ""  ]]; then
	CONTAINER_NAME=$(cat $DOCKER_COMPOSE_FILE | grep -A15 "${CREATE_DBS_CONTAINER_NAME}:" | grep -A1 "depends_on:" | tail -1 | awk '{print $NF}')
	if [[ "$CONTAINER_NAME" != "" ]]; then
		container_id=$(docker ps --filter "name=$CONTAINER_NAME" | grep -v '^CONTAINER' | awk '{print $1}')
		for query in "${queries[@]}"; do
			confirm_query=1
			if [[ "$(echo $query | grep -iw 'delete from')" != "" ]]; then
				confirm_query=0
			fi

			if [[ $confirm_query -ne 1 ]]; then
				echo -n "Delete records? (yes to confirm) "
				read -r confirm_query
				if [[ "$confirm_query" = "yes" ]]; then
					confirm_query=1
				fi
			fi
			if [[ $confirm_query -eq 1 ]]; then
				docker exec -it $container_id $cmd ${params[@]} -c "$query"
			fi
		done
	else
		echo "Can't find the portalbackend DB container!"
		exit 1
	fi
else
	echo "Can't find any DB connection details in the docker-compose file!"
	exit 1
fi
