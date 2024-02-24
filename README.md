# Code Smell Detection example - Keras version
This classic example of code smell detection is well suited as a lightweight test when learning FEDn and developing on FEDn in pseudo-distributed mode. A normal high-end laptop or a workstation should be able to sustain several clients. 

The example is also useful for general scalability tests in fully distributed mode; please check the following papers for more details about the dataset.

1. Arcelli Fontana, F., Mäntylä, M. V., Zanoni, M., & Marino, A. (2016). Comparing and experimenting with machine learning techniques for code smell detection. Empirical Software Engineering, 21, 1143-1191.
2. Pecorelli, F., Di Nucci, D., De Roover, C., & De Lucia, A. (2020). A large empirical assessment of the role of data balancing in machine-learning-based code smell detection. Journal of Systems and Software, 169, 110693.
3. Alkharabsheh, K., Crespo, Y., Fernández-Delgado, M., Cotos, J. M., & Taboada, J. A. (2019). Assessing the influence of size category of the project in god class detection, an experimental approach based on machine learning (MLA). In International Conference on Software Engineering & Knowledge Engineering (pp. 361-366).


## Provide local training and test data

1. Based on your needs (number of clients you want, the training dataset size, and the testing dataset size), download the datasets using the link mentioned in the source papers and prepare the dataset partitions as you want (create n partitions) using the following command, or you can do it manually for each dataset
  
```
python create_data_partitions.py
```


2. To run the experiment correctly, you should use and download FEDn Release v0.3.3b1 from the following link

```
https://github.com/scaleoutsystems/fedn/releases/tag/v0.3.3b1
```

For more details about how to install and configure FEDn, please check the following FEDn documentation.

```
https://fedn.readthedocs.io/en/stable/
```




## Configuring the Reducer  
Navigate to 'https://localhost:8090' (or the URL of your Reducer) and follow the instructions to upload the compute package in 'package/package.tar.gz' and the initial model in 'initial_model/initial_model.npz'. 

## Creating a compute package
Whenever you make updates to the client code (such as altering any of the settings in the above-mentioned file), you need to re-package the computing package:

```bash
tar -czvf package.tar.gz client
```
To clear the system and set a new compute package, see: https://github.com/scaleoutsystems/fedn/blob/master/docs/FAQ.md

For an explanation of the compute package structure and content: https://github.com/scaleoutsystems/fedn/blob/develop/docs/tutorial.md
 
## Creating a new initial model
The baseline model (LSTM) is specified in the file 'client/init_model.py'. This script creates an untrained neural network and serializes that to a file.  If you wish to alter the initial model, edit 'init_model.py' and 'models/imdb_model.py', then regenerate the initial model file (install dependencies as needed, see requirements.txt):

```bash
python init_model.py 
```
### Configuring the client
We have made it possible to configure a couple of settings to vary the conditions for the training. These configurations are exposed in the file 'settings.yaml': 

```yaml 
# Parameters for local training
test_size: 0.25
batch_size: 32
epochs: 1
```

## Attaching a client to the federation

1. First, download 'client.yaml' from the Reducer 'Network' page, and replace the content in your local 'client.yaml'. 
2. Start a client. Here there are different options (see below): 
    - Docker 
    - docker-compose
 
#### docker-compose
To start N clients: 

```bash
docker-compose -f docker-compose.dev.yaml -f extra-hosta.yaml up --build 
```
### Start training 
When clients are running, navigate to the 'Control' page of the Reducer to start the training. 




## License
Apache-2.0 (see LICENSE file for full information).



[comment]: <> (## Start the client)

[comment]: <> (The easiest way to start clients for quick testing is by using Docker. We provide a docker-compose template for convenience. First, edit 'fedn-network.yaml' to provide information about the reducer endpoint. Then:)

[comment]: <> (```bash)

[comment]: <> (docker-compose -f docker-compose.yaml up --scale client=2 )

[comment]: <> (```)

[comment]: <> (> Note that this assumes that a FEDn network is running &#40;see separate deployment instructions&#41;. The file 'docker-compose.yaml' is for testing against a local pseudo-distributed FEDn network. Use 'docker-compose.decentralised.yaml' if you are connecting against a reducer part of a distributed setup and provide a 'extra_hosts' file.)

[comment]: <> (The easiest way to start clients for quick testing is by using Docker. We provide a docker-compose template for convenience. First, edit 'fedn-network.yaml' to provide information about the reducer endpoint. Then:)

[comment]: <> (The easiest way to distribute data across client is to start this command instead of the previous one )

[comment]: <> (```bash)

[comment]: <> (docker-compose -f docker-compose.decentralised.yaml up --build)

[comment]: <> (```)


[comment]: <> (## Configure and start a client using cpu device)

[comment]: <> (The easiest way to start clients for quick testing is to use shell script.The following )

[comment]: <> (shell script will configure and start a client on a blank Ubuntu 20.04 LTS VM:    )


[comment]: <> (```bash)

[comment]: <> (#!/bin/bash)

[comment]: <> (# Install Docker and docker-compose)

[comment]: <> (sudo apt-get update)

[comment]: <> (sudo sudo snap install docker)

[comment]: <> (# clone the nlp_imdb example)

[comment]: <> (git https://github.com/scaleoutsystems/FEDn-client-casa-keras.git)

[comment]: <> (cd FEDn-client-casa-keras)

[comment]: <> (# if no available data, download it from archive)

[comment]: <> (# wget https://archive.org/download/data_20210225/data.zip)

[comment]: <> (# sudo apt install unzip)

[comment]: <> (# unzip -o data.zip)

[comment]: <> (# sudo rm data.zip)

[comment]: <> (# Make sure you have edited extra-hosts.yaml to provide hostname mappings for combiners)

[comment]: <> (# Make sure you have edited client.yaml to provide hostname mappings for reducer)

[comment]: <> (sudo docker-compose -f docker-compose.yaml -f extra-hosts.yaml up --build)

[comment]: <> (```)

[comment]: <> (### Start prediction- global model serving)

[comment]: <> (We have made it possible to use the trained global model for prediction, to start the UI make sure that the FEDn-network is)

[comment]: <> (is started and run the flask app &#40;python predict/app.py&#41;)

[comment]: <> (```bash)

[comment]: <> (# prediction/)

[comment]: <> (python app.py)

[comment]: <> (```)


[comment]: <> (## License)

[comment]: <> (Apache-2.0 &#40;see LICENSE file for full information&#41;.)
