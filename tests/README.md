# Medical Informatics Platform (MIP), testing deployment

### Prerequisites

1. Install [python3.8](https://www.python.org/downloads/ "python3.8")

2. Install [poetry](https://python-poetry.org/ "poetry")
   It is important to install `poetry` in isolation, so follow the
   recommended installation method.

3. Install docker-compose


## Instructions to deploy:

1. Clone the repo:
    ```
    git clone https://github.com/HBPMedical/mip-deployment
    ```

2. Access the setup folder for the testing deployment:
    ```
    cd tests/setup/
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