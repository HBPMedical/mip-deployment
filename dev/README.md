# Development deployment

## Requirements
### Hardware
* 40 GB HDD
* 8 GB RAM
* 2 CPU Cores

### Software
* Ubuntu Server (minimal installation, without GUI)

### Prerequisites

1. Install [python3.8](https://www.python.org/downloads/ "python3.8")

2. Install [poetry](https://python-poetry.org/ "poetry")
   It is important to install `poetry` in isolation, so follow the
   recommended installation method.

3. Install docker-compose

4. Create Keycloak env file:
   ```
   cp .env.example .env
   ```

## Instructions to deploy:

1. Clone the repo:
    ```
    git clone https://github.com/HBPMedical/mip-deployment
    ```

2. Access the 'test' folder:
    ```
    cd mip-deployment/tests/
    ``` 

3. To start the MIP stack run the 'start.sh' script to setup all the containers:
    ```
    ./start.sh
    ```

4. To test if the MIP stack is properly setup run the 'test.sh':
    ```
    ./test.sh 
    ```
   
5. To stop the MIP stack run the 'stop.sh' script to stop all the containers:
    ```
    ./stop.sh
    ```
