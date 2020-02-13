#!/usr/bin/env bash

INSTALL_PATH="$(pwd)"
ENV="local"
DOCKER_DOWNLOAD_HOST="download.docker.com"
CONFLICTING_PACKAGES="docker docker-engine docker.io containerd runc"
PREREQUIRED_PACKAGES="git apt-transport-https ca-certificates curl gnupg-agent software-properties-common net-tools lsof"
REQUIRED_PACKAGES="docker-ce docker-ce-cli containerd.io docker-compose"
MIP_GITHUB_OWNER="crochat"
MIP_GITHUB_PROJECT="mip-deployment-infrastructure"
MIP_BRANCH="release"
EXAREME_GITHUB_OWNER="madgik"
EXAREME_GITHUB_PROJECT="exareme"
EXAREME_BRANCH="master"


_get_docker_main_ip(){
	dockerip=$(ip address show|grep 'inet.*docker0'|awk '{print $2}'|awk -F '/' '{print $1}')
	if [ "$dockerip" != "" ]; then
		DOCKER_MAIN_IP=$dockerip
	fi
}

uninstall_conflicting_tools(){
	local next=0
	while [ $next -eq 0 ]; do
		local packages=""
		next=1
		for package in $CONFLICTING_PACKAGES; do
			local match=$(dpkg --list|grep -E '^ii[ \t]+$package[ \t]+')
			if [ "$match" != "" ]; then
				packages="$packages $package"
				next=0
			fi
		done
		if [ $next -eq 0 ]; then
			sudo apt remove $packages
		fi
	done
}

install_required_tools(){
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
				sudo apt install $packages
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
			sudo add-apt-repository "deb [arch=amd64] https://$DOCKER_DOWNLOAD_HOST/linux/ubuntu $(lsb_release -cs) stable"
			next=0
		fi
	done
}

check_exareme_required_ports(){
	local next=0
	while [ $next -eq 0 ]; do
		check=$(netstat -atun | awk '(($1~/^tcp/) && (($4~/:2377$/) || ($4~/:7946/)) && ($NF~/LISTEN$/)) || (($1~/^udp/) && (($4~/\:4789$/) || ($4~/\:7946/)))')
		if [ "$check" = "" ]; then
			next=1
		else
			echo "Exareme: required ports currently in use"
			echo "$check"
			echo "Please fix it, then press a key to continue"
			read
		fi
	done
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
		echo "$INSTALL_PATH/$ENV/$MIP_GITHUB_PROJECT/data" > $INSTALL_PATH/$ENV/$MIP_GITHUB_PROJECT/$EXAREME_GITHUB_PROJECT/Local-Deployment/data_path.txt
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
	local path=$(pwd)
	cd $INSTALL_PATH/$ENV/$MIP_GITHUB_PROJECT/$EXAREME_GITHUB_PROJECT/Local-Deployment
	./deployLocal.sh
	cd $path
}

prepare_mip_env(){
	_get_docker_main_ip

	cat <<EOF >$INSTALL_PATH/$ENV/$MIP_GITHUB_PROJECT/.env
HOST="$(hostname)"
FRONTEND_URL="http://localhost"
EXAREME_URL="http://$DOCKER_MAIN_IP:9090"
WORKFLOW_URL="http://88.197.53.100:8091/Galaxy_Middleware_API-1.0.0-SNAPSHOT/api"
GALAXY_URL="http://88.197.53.10:8090/nativeGalaxy"
EOF
}

run_mip(){
	echo -e "Run MIP [y/n]? "
	read answer
	if [ "$answer" = "y" ]; then
		$INSTALL_PATH/$ENV/$MIP_GITHUB_PROJECT/run.sh
	fi
}

delete_mip(){
	if [ -d $INSTALL_PATH/$ENV/$MIP_GITHUB_PROJECT ]; then
		echo -e "Delete full MIP [y/n]? "
		read answer
		if [ "$answer" = "y" ]; then
			sudo docker swarm leave --force 2>/dev/null
			rm -rf $INSTALL_PATH/$ENV/$MIP_GITHUB_PROJECT
		fi
	fi
	if [ -d $INSTALL_PATH/$ENV ]; then
		rmdir $INSTALL_PATH/$ENV
	fi
}

main(){
	if [ "$1" != "uninstall" ]; then
		uninstall_conflicting_tools
		install_required_tools prerequired
		prepare_docker_apt_sources
		install_required_tools required
		check_exareme_required_ports
		download_mip
		download_exareme
		generate_local_data_path_txt
		generate_local_exareme_yaml
		exareme_local_deployment
		prepare_mip_env
		run_mip
	else
		delete_mip
	fi
	echo "done"
}

main $@
