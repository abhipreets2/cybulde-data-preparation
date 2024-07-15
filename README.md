# Cyberbullying Data Preparation And Tokenizer Training

# (1) Data preparation

## Objectives
- Data is stored in GCP (done in [cybulde-data-versioning](https://github.com/abhipreets2/cybulde-data-versioning) repo).
- Process this data parallelly to be in a format to be picked up by the machine learning model.
- Keep a track of required packages and containerizer code for reproducibility.


## How to use this repo

### Setting up the code
- Clone the repo.
- Make sure you have gcloud and gsutils installed and autheticated (since the config files of gcloud will be mounted to the docker container).
- Spin up a container using:
					    ``` docker compose up ```
- At this point you should have a docker container through which we will execute our python scripts
- Exec into the container using:
						```docker exec -it <container id> bash ```
- Now you should be inside the terminal of docker container; execute the python script using:
						```python -W ignore cybulde/process_data.py```
						
- We are all done, the script will execute and read and clean the data and store it back to GCP.
- If you want to download the data locally, you can do so by changing the **fetch_data** parameter to **true**. If you want to create local dask instead of the cloud implementation change **dask_cluster** to **local_dask_cluster**. Both of these parameter can be tweaked via the config file **data_processing_config.yaml**
```
defaults:
  - data_processing_config_schema
  - dask_cluster: gcp_dask_cluster
  - dataset_reader_manager: ghc_jigsaw_twitter
  - dataset_cleaner_manager: dataset_cleaner


version: v9
fetch_data: false
processed_data_save_dir: gs://cybulde-data-store/data/processed
```

### Setting up GCP
GCP uses the following resource in the project
- To store the data we will be needing a **Bucket**.
- To store git tokens we are using **Secret Manager** which will be accessed by the VM to fetch the correct version of data.
- **Compute engine** will be responsible for reading and cleaning the data.(no setup needed for this as this will be created through dask)
- All our workers and scheduler should be using the same setup in order to work together, for this we will use **Artifact Registry** to push docker image, this can be picked up by the compute engine for initial setup.
- In order to view the dask daskboard and interaction between scheduler and worker we will need to setup some **Firewall rules**, these rules can be found in the network parameter of [dask documentation](https://cloudprovider.dask.org/en/latest/gcp.html)

## System Design

![image](https://github.com/user-attachments/assets/b2e55ba9-927d-4a49-8fb1-b276dacd061a)

## Python script
- Create a schema in config_schemas for classes which require huge number parameters (makes it easier to track and maintain changes).
- Generate config.yaml files to use and track config.
- Use pydantic to maintain proper config structure.
- Create dask cluster to parallelly read and process the data

## Docker
The docker container should be able to:
- Fetch data from GCP
- Create VMs in GCP to process the data parallelly, local implementation also included
- Volumes to mount (in my case I had to mention the absolute path)
	- The code directory (the volume mount is disabled in docker-compose.yaml while push images to GCP and instead copied in the DockerFile)
	- ~/.config/gcloud

## Hydra working
- In order to use hydra we have to make use of `@hydra.main(config_path=<config_path>, config_name=<config_name>, version_base=None)` decorator, this decorator will return a DictConfig object that can be used by the base function
- We supply the config.yaml file to the above decorator, the config.yaml file will contain the schema, the schema the class which needs to be instantiate using `_target_` and other parameters
- We can override the default parameters in the schema by mentioning it in the config.yaml file
- We also have to dump individual configs in the ConfigStore so we can use them in our final config (hence we have a wrapper on top of `@hydra.main()` called get_config or something similar)

## Configs
- n_workers in local_dask_cluster.yaml overriden to **12** (6x2), because my system has 6 cores each with 2 threads
- local_dask_cluster_schema is assigned to the group dask_cluster because within the main config (config.yaml) it is mentioned as dask_cluster: local_dask_cluster_schema. So while storing the config using ConfigStore we have to assign it the proper group.

## How to use hydra
- Setting up a custom decorator `@get_config` which will be responsible for storing all the required config schema in the ConfigStore. This will help hydra to read the main config file and get the sub configs within it using the ConfigStore.
- Using task_function within the `@get_config` decorator to return control back to the calling function with the correct parameters.
- There is another way that hydra works, suppose we have something like this 
```
defaults:
  - config_schema
  - dask_cluster: local_dask_cluster
```
in this case there is nothing stored in the config store as "local_dask_cluster",
but hydra will start looking for a folder within the main config folder called "dask_cluster" within which a "local_dask_cluster.yaml" should be present in order to be used.


Data storage:
- This can be either a local implementation or cloud, in my case I have used GCP bucket to store the actual data. 
- GIT does not store the actual data it is only used to track the version. DVC integration with GIT enables us to do this, different version of data will have different tags in the GIT repo.
- GCP bucket is where we store the raw and cleaned data.

Compute:
- We are using the concept of distributed data processing to process our data, the scheduler will create multiple workers which will be doing the data cleaning task and reporting back to the scheduler.
- The compute will read the data and apply transformations on it to make the data clean. Finally the cleaned and labelled data will be stored in GCP bucket from where it can be picked up by the machine learning model.


## Issues faced
- Because of the recent pygit2 naming changes, dvc is not working as intended. To fix this downgrade the version of pygit. This issues is reported [here](https://github.com/iterative/dvc/issues/10431)
- If you have been running docker with sudo until now as I did, it is time to switch up. Using `sudo docker push` looks for credentials in the /root/.docker instead of ~/.docker, as reported [here](https://www.googlecloudcommunity.com/gc/Developer-Tools/Permission-quot-artifactregistry-repositories-uploadArtifacts/m-p/665497/highlight/true#M1638)
- If we have multiple gcloud auth accounts we can get the below error, if scope is not defined for one of the accounts; 
	```google.auth.exceptions.RefreshError: ('invalid_scope: Invalid OAuth scope or ID token audience provided.', {'error': 'invalid_scope', 'error_description': 'Invalid OAuth scope or ID token audience provided.'})```
	
	To solve this I check the `gcloud auth list` and removed all the accounts using `gcloud revoke <account_name>` and then added the owner account back using `gcloud auth login` 
- For some reason hydra does not instantiate `GCPCluster` in dask when we use `instantiate()` , to tackle this `custom_instantiate()` is added in  config_utils.py 
