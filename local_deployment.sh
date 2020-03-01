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
MIP_GITHUB_OWNER="HBPMedical"
MIP_GITHUB_PROJECT="mip-deployment"
MIP_BRANCH="master"


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

contains(){
	[[ $1 =~ (^|[[:space:]])"$2"($|[[:space:]]) ]] && return 0 || return 1
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
	local docker_ps=$(docker ps 2>/dev/null|awk '!/^CONTAINER/')
	if [ "$docker_ps" != "" ]; then
		echo -n "Portal Frontend								"
		echo $(check_docker_container mip_frontend_1)

		echo -n "Portal Backend								"
		echo $(check_docker_container mip_portalbackend_1)

		echo -n "Portal Backend PostgreSQL DB						"
		echo $(check_docker_container mip_portalbackend_db_1)

		echo -n "Galaxy									"
		echo $(check_docker_container mip_galaxy_1)

		echo -n "KeyCloak								"
		echo $(check_docker_container mip_keycloak_1)

		echo -n "KeyCloak PostgreSQL DB							"
		echo $(check_docker_container mip_keycloak_db_1)

		echo -n "Exareme Master								"
		echo $(check_docker_container mip_exareme_master_1)

		echo -n "Exareme Keystore							"
		echo $(check_docker_container mip_exareme_keystore_1)
	else
		check_exareme_required_ports short
		if [ $? -eq 1 ]; then
			echo "It seems dockerd is running without allowing connections. Maybe you should call $0 stop --force"
		else
			echo "No docker container is currently running!"
		fi
	fi
}

check_running_details(){
	local docker_ps=$(docker ps 2>/dev/null|awk '!/^CONTAINER/')
	if [ "$docker_ps" != "" ]; then
		docker ps
	else
		check_exareme_required_ports short
		if [ $? -eq 1 ]; then
			echo "It seems dockerd is running without allowing connections. Maybe you should call $0 stop --force"
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
			fi
		fi
	done
	cd $path
}

run_mip(){
	local images_list="mip_frontend_1 mip_portalbackend_1 mip_portalbackend_db_1 mip_galaxy_1 mip_keycloak_1 mip_keycloak_db_1 mip_exareme_master_1 mip_exareme_keystore_1"
	local ko_list=""
	for image in $images_list; do
		local image_check=$(check_docker_container $image)
		if [ "$image_check" != "ok" ]; then
			ko_list=$ko_list" "$image_check
		fi
	done

	if [ "$ko_list" = "" ]; then
		echo "The MIP frontend seems to be already running! Maybe you want $0 restart"
		exit 1
	else
		if [ -d $INSTALL_PATH/$ENV/$MIP_GITHUB_PROJECT ]; then
			local path=$(pwd)
			cd $INSTALL_PATH/$ENV/$MIP_GITHUB_PROJECT
			./run.sh
			cd $path
		else
			echo "No such directory: $INSTALL_PATH/$ENV/$MIP_GITHUB_PROJECT"
			exit 1
		fi
	fi
}

logs(){
	local image="mip_$1_1"
	contains "mip_frontend_1 mip_portalbackend_1 mip_portalbackend_db_1 mip_galaxy_1 mip_keycloak_1 mip_keycloak_db_1 mip_exareme_master_1 mip_exareme_keystore_1" $image
	if [ $? -ne 0 ]; then
		echo "Usage: $0 logs [frontend|portalbackend|portalbackend_db|galaxy|keycloak|keycloak_db|exareme_master|exareme_keystore]"
		exit 1
	fi

	local process_id=$(docker ps|grep $image|awk '{print $1}')
	if [ "$process_id" != "" ]; then
		docker logs -f $process_id
	else
		echo "$1 docker container is not running!"
	fi
}

stop_mip(){
	if [ "$1" = "--force" ]; then
		echo -n "WARNING: This will kill any docker container, swarm node, and finally kill any docker daemon running on this machine! Are you sure you want to continue? [y/n] "
		read answer
		if [ "$answer" = "y" ]; then
			local docker_ps=$(docker ps -q 2>/dev/null)
			if [ "$docker_ps" != "" ]; then
				docker stop $docker_ps
			fi
			docker swarm leave --force 2>/dev/null

			check_exareme_required_ports short
			if [ $? -eq 1 ]; then
				killall -9 dockerd
			fi
		fi
	elif [ "$1" != "" ]; then
		echo "Usage: $0 stop"
	else
		if [ -d $INSTALL_PATH/$ENV/$MIP_GITHUB_PROJECT ]; then
			local path=$(pwd)
			cd $INSTALL_PATH/$ENV/$MIP_GITHUB_PROJECT
			./stop.sh
			cd $path
		else
			echo "No such directory: $INSTALL_PATH/$ENV/$MIP_GITHUB_PROJECT"
			exit 1
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
			run_mip
			;;
		stop)
			check_docker
			stop_mip $2
			;;
		restart)
			check_docker
			stop_mip
			sleep 2
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
			logs $2
			;;
		uninstall)
			check_os
			stop_mip
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
