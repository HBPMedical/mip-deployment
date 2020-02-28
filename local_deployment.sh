#!/usr/bin/env bash

REQUIRED_OS_DISTRIBUTOR_ID="Ubuntu"
REQUIRED_OS_RELEASE="18.04"
REQUIRED_DOCKER_VERSION="19.03.6"
INSTALL_PATH="$(pwd)"
ENV="local"
DOCKER_DOWNLOAD_HOST="download.docker.com"
CONFLICTING_PACKAGES="docker docker-engine docker.io containerd runc"
CONFLICTING_SNAP_PACKAGES="docker"
PREREQUIRED_PACKAGES="git apt-transport-https ca-certificates curl gnupg-agent software-properties-common net-tools lsof"
REQUIRED_PACKAGES="docker-ce docker-ce-cli containerd.io docker-compose"
MIP_GITHUB_OWNER="crochat"
MIP_GITHUB_PROJECT="mip-deployment-infrastructure"
MIP_BRANCH="release"
EXAREME_GITHUB_OWNER="crochat"
EXAREME_GITHUB_PROJECT="exareme"
EXAREME_BRANCH="master"


_get_docker_main_ip(){
	local dockerip=$(ip address show|grep 'inet.*docker0'|awk '{print $2}'|awk -F '/' '{print $1}')
	if [ "$dockerip" != "" ]; then
		DOCKER_MAIN_IP=$dockerip
	fi
}

check_os(){
	if [ "$(lsb_release -si)" != "$REQUIRED_OS_DISTRIBUTOR_ID" -o "$(lsb_release -sr)" != "$REQUIRED_OS_RELEASE" ]; then
		echo "Required OS version: Ubuntu 18.04!"
		exit 1
	fi
}

check_conflicting_packages(){
	local packages=""
	for package in $CONFLICTING_PACKAGES; do
		local match=$(dpkg --list|grep -E "^ii[ \t]+$package[ \t]+")
		if [ "$match" != "" ]; then
			packages="$packages $package"
		fi
	done

	if [ "$packages" != "" ]; then
		echo "Conflicting packages detected			: $packages" && echo
	fi
}

check_conflicting_snap_packages(){
	local packages=""
	for package in $CONFLICTING_SNAP_PACKAGES; do
		local match=$(snap list 2>/dev/null|grep "^$package[ \t]")
		if [ "$match" != "" ]; then
			packages="$packages $package"
		fi
	done

	if [ "$packages" != "" ]; then
		echo "Conflicting Snap packages detected		: $packages" && echo
	fi
}

uninstall_conflicting_snap_packages(){
	local next=0
	while [ $next -eq 0 ]; do
		local packages=""
		next=1
		for package in $CONFLICTING_SNAP_PACKAGES; do
			local match=$(snap list 2>/dev/null|grep "^$package[ \t]")
			if [ "$match" != "" ]; then
				packages="$packages $package"
				next=0
			fi
		done
		if [ $next -eq 0 ]; then
			snap remove $packages
		fi
	done
}

uninstall_conflicting_packages(){
	local next=0
	while [ $next -eq 0 ]; do
		local packages=""
		next=1
		for package in $CONFLICTING_PACKAGES; do
			local match=$(dpkg --list|grep -E "^ii[ \t]+$package[ \t]+")
			if [ "$match" != "" ]; then
				packages="$packages $package"
				next=0
			fi
		done
		if [ $next -eq 0 ]; then
			apt remove $packages
		fi
	done
}

install_required_packages(){
	if [ "$1" = "prerequired" -o "$1" = "required" ]; then
		local required_packages=""
		case "$1" in
			"prerequired")
				required_packages=$PREREQUIRED_PACKAGES
				;;
			"required")
				required_packages=$REQUIRED_PACKAGES
				;;
		esac

		local next=0
		while [ $next -eq 0 ]; do
			local packages=""
			next=1
			for package in $required_packages; do
				local match=$(dpkg --list|grep "^ii.*$package ")
				if [ "$match" = "" ]; then
					packages="$packages $package"
					next=0
				fi
			done
			if [ $next -eq 0 ]; then
				apt install $packages
			fi
		done
	fi
}

prepare_docker_apt_sources(){
	local next=0
	while [ $next -eq 0 ]; do
		next=1
		if [ "$(apt-key fingerprint 0EBFCD88 2>/dev/null)" = "" ]; then
			curl -fsSL https://$DOCKER_DOWNLOAD_HOST/linux/ubuntu/gpg | apt-key add -
			next=0
		fi
		if [ "$(grep -R $DOCKER_DOWNLOAD_HOST /etc/apt)" = "" ]; then
			add-apt-repository "deb [arch=amd64] https://$DOCKER_DOWNLOAD_HOST/linux/ubuntu $(lsb_release -cs) stable"
			apt update
			next=0
		fi
	done
}

check_docker(){
	if [ "$(command -v docker)" = "" ]; then
		echo "docker not installed!"
		exit 1
	fi

	local dockerversion=$(docker --version|awk '{print $3}'|cut -d',' -f1)
	local dockercheck=`(echo $REQUIRED_DOCKER_VERSION; echo $dockerversion)|sort -Vk3|tail -1`
	if [ "$dockercheck" = "$REQUIRED_DOCKER_VERSION" -a "$REQUIRED_DOCKER_VERSION" != "$dockerversion" ]; then
		echo "docker version $REQUIRED_DOCKER_VERSION is required!"
		exit 1
	fi
}

check_exareme_required_ports(){
	local next=0
	while [ $next -eq 0 ]; do
		check=$(netstat -atun | awk '(($1~/^tcp/) && (($4~/:2377$/) || ($4~/:7946/)) && ($NF~/LISTEN$/)) || (($1~/^udp/) && ($4~/\:7946/))')
		if [ "$check" = "" ]; then
			next=1
		else
			if [ "$1" != "short" ]; then
				echo "Exareme: required ports currently in use"
				echo "$check"
				echo "Please fix it (try with $0 stop), then press ENTER to continue"
				read
			else
				return 1
			fi
		fi
	done
}

check_docker_container(){
	local result=""

	local process_id=$(docker ps|grep $1|awk '{print $1}')
	if [ "$process_id" != "" ]; then
		local process_state=$(docker inspect $process_id --format '{{.State.Status}}')
		if [ "$process_state" = "running" ]; then
			result="ok"
		else
			result="$process_state"
		fi
	else
		result="NOT RUNNING!"
	fi

	echo $result
}

prerunning_backend_guard(){
	check_exareme_required_ports short
	if [ $? -eq 1 ]; then
		echo "It seems something is already using/locking required ports. Maybe you should call $0 restart"
		exit 1
	fi
}

check_running(){
	local dockerps=$(docker ps 2>/dev/null|awk '!/^CONTAINER/')
	if [ "$dockerps" != "" ]; then
		echo -n "Portal Frontend								"
		echo $(check_docker_container portal-frontend)

		echo -n "Portal Backend								"
		echo $(check_docker_container portal-backend)

		echo -n "PostgreSQL								"
		echo $(check_docker_container postgres)

		echo -n "Consul									"
		echo $(check_docker_container consul)

		echo -n "Exareme Master								"
		echo $(check_docker_container exareme-master)

		echo -n "Exareme Keystore							"
		echo $(check_docker_container exareme-keystore)
	else
		check_exareme_required_ports short
		if [ $? -eq 1 ]; then
			echo "It seems dockerd is running without allowing connections. Maybe you should call $0 stop-force"
		else
			echo "No docker container is currently running!"
		fi
	fi
}

check_running_details(){
	local dockerps=$(docker ps 2>/dev/null|awk '!/^CONTAINER/')
	if [ "$dockerps" != "" ]; then
		docker ps
		echo && echo
		docker service ls
	else
		check_exareme_required_ports short
		if [ $? -eq 1 ]; then
			echo "It seems dockerd is running without allowing connections. Maybe you should call $0 stop-force"
		else
			echo "No docker container is currently running!"
		fi
	fi
}

download_mip(){
	local path=$(pwd)
	local next=0
	while [ $next -eq 0 ]; do
		if [ ! -d $INSTALL_PATH/$ENV ]; then
			mkdir -p $INSTALL_PATH/$ENV
		fi

		if [ -d $INSTALL_PATH/$ENV/$MIP_GITHUB_PROJECT ]; then
			next=1
		else
			echo -e "MIP not found. Download it [y/n]? "
			read answer
			if [ "$answer" = "y" ]; then
				git clone https://github.com/$MIP_GITHUB_OWNER/$MIP_GITHUB_PROJECT $INSTALL_PATH/$ENV/$MIP_GITHUB_PROJECT
				cd $INSTALL_PATH/$ENV/$MIP_GITHUB_PROJECT
				if [ "$MIP_BRANCH" != "" ]; then
					git checkout $MIP_BRANCH
				fi
				if [ -d $INSTALL_PATH/$ENV/$MIP_GITHUB_PROJECT/$EXAREME_GITHUB_PROJECT ]; then
					rm -rf $INSTALL_PATH/$ENV/$MIP_GITHUB_PROJECT/$EXAREME_GITHUB_PROJECT
				fi
			fi
		fi
	done
	cd $path
}

download_exareme(){
	local path=$(pwd)
	local next=0
	while [ $next -eq 0 ]; do
		if [ ! -d $INSTALL_PATH/$ENV/$MIP_GITHUB_PROJECT/$EXAREME_GITHUB_PROJECT ]; then
			echo -e "Exareme not found. Download it [y/n]? "
			read answer
			if [ "$answer" = "y" ]; then
				cd $INSTALL_PATH/$ENV/$MIP_GITHUB_PROJECT
				git clone https://github.com/$EXAREME_GITHUB_OWNER/$EXAREME_GITHUB_PROJECT
				cd $INSTALL_PATH/$ENV/$MIP_GITHUB_PROJECT/$EXAREME_GITHUB_PROJECT
				git checkout $EXAREME_BRANCH
			fi
		else
			next=1
		fi
	done
	cd $path
}

generate_local_data_path_txt(){
	if [ ! -s $INSTALL_PATH/$ENV/$MIP_GITHUB_PROJECT/$EXAREME_GITHUB_PROJECT/Local-Deployment/data_path.txt ]; then
		echo "LOCAL_DATA_FOLDER=$INSTALL_PATH/$ENV/$MIP_GITHUB_PROJECT/data" > $INSTALL_PATH/$ENV/$MIP_GITHUB_PROJECT/$EXAREME_GITHUB_PROJECT/Local-Deployment/data_path.txt
	fi
}

generate_local_exareme_yaml(){
	if [ ! -s $INSTALL_PATH/$ENV/$MIP_GITHUB_PROJECT/$EXAREME_GITHUB_PROJECT/Local-Deployment/exareme.yaml ]; then
		cat <<EOF >$INSTALL_PATH/$ENV/$MIP_GITHUB_PROJECT/$EXAREME_GITHUB_PROJECT/Local-Deployment/exareme.yaml
EXAREME_IMAGE: "hbpmip/exareme"
EXAREME_TAG: "v21.3.0"
EOF
	fi
}

exareme_local_deployment(){
	if [ "$(check_docker_container exareme-master)" = "ok" -a "$(check_docker_container exareme-keystore)" = "ok" ]; then
		echo "The MIP backend seems to be already running! There's no need to deploy it again, but maybe you want $0 restart"
	else
		prerunning_backend_guard
		local path=$(pwd)
		cd $INSTALL_PATH/$ENV/$MIP_GITHUB_PROJECT/$EXAREME_GITHUB_PROJECT/Local-Deployment
		./deployLocal.sh
		cd $path
	fi
}

prepare_mip_env(){
	_get_docker_main_ip

	cat <<EOF >$INSTALL_PATH/$ENV/$MIP_GITHUB_PROJECT/.env
HOST=$(hostname)
FRONTEND_URL=http://localhost
EXAREME_URL=http://$DOCKER_MAIN_IP:9090
WORKFLOW_URL=http://88.197.53.100:8091/Galaxy_Middleware_API-1.0.0-SNAPSHOT/api
GALAXY_URL=http://88.197.53.10:8090/nativeGalaxy
EOF
}

run_mip(){
	if [ "$(check_docker_container postgres)" = "ok" -a "$(check_docker_container consul)" = "ok" -a "$(check_docker_container portal-backend)" = "ok" -a "$(check_docker_container portal-frontend)" = "ok" ]; then
		echo "The MIP frontend seems to be already running! Maybe you want $0 restart"
		exit 1
	else
		$INSTALL_PATH/$ENV/$MIP_GITHUB_PROJECT/run.sh
	fi
}

logs(){
	docker service logs -f $(hostname)_exareme-master
}

stop_mip(){
	local docker_ps=$(docker ps -q 2>/dev/null)
	if [ "$docker_ps" != "" ]; then
		docker stop $docker_ps
	fi
	docker swarm leave --force 2>/dev/null

	if [ "$1" = "force" ]; then
		check_exareme_required_ports short
		if [ $? -eq 1 ]; then
			killall -9 dockerd
		fi
	fi
}

delete_mip(){
	if [ -d $INSTALL_PATH/$ENV/$MIP_GITHUB_PROJECT ]; then
		echo -e "Delete full MIP [y/n]? "
		read answer
		if [ "$answer" = "y" ]; then
			docker swarm leave --force 2>/dev/null
			rm -rf $INSTALL_PATH/$ENV/$MIP_GITHUB_PROJECT
		fi
	fi
	if [ -d $INSTALL_PATH/$ENV ]; then
		rmdir $INSTALL_PATH/$ENV
	fi
}

main(){
	if [ "$(id -u)" != "0" ]; then
		echo "Call me with sudo!"
		exit 1
	fi

	case "$1" in
		start)
			check_docker
			exareme_local_deployment
			run_mip
			;;
		stop)
			check_docker
			stop_mip
			;;
		stop-force)
			check_docker
			stop_mip force
			;;
		restart)
			check_docker
			stop_mip
			sleep 2
			exareme_local_deployment
			run_mip
			;;
		check-required)
			check_os
			check_conflicting_packages
			check_conflicting_snap_packages
			check_docker
			check_exareme_required_ports
			echo "ok"
			;;
		status)
			check_docker
			check_running
			;;
		status-details)
			check_docker
			check_running_details
			;;
		logs)
			check_docker
			logs
			;;
		uninstall)
			check_os
			delete_mip
			;;
		install)
			check_os
			stop_mip
			delete_mip
			uninstall_conflicting_packages
			uninstall_conflicting_snap_packages
			install_required_packages prerequired
			prepare_docker_apt_sources
			install_required_packages required
			check_exareme_required_ports
			download_mip
			download_exareme
			generate_local_data_path_txt
			generate_local_exareme_yaml
			exareme_local_deployment
			prepare_mip_env
			echo -e "Run MIP [y/n]? "
			read answer
			if [ "$answer" = "y" ]; then
				run_mip
			fi
			;;
		*)
			echo "Usage: $0 [check-required|install|uninstall|start|stop|status|status-details|restart|logs]"
			;;
	esac
}

main $@
