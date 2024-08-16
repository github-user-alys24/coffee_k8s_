# Group - Alyssa, Ayumi, Terrence, Shae
# T2 Coffee k8s application

K8s Cluster Workflow
Preprocessing > handles data cleaning, and builds the raw-data and preprocessed-data PV and PVC to be used down the pipeline
├── preprocessing-kubemanifest.yaml
│   └── deployment 
│   	└── preprocessing-app
│   └── service 
│   	└── preprocessing-service
│   └── PV and PVC 
│   	└── raw-data-pv and raw-data-pvc
│   	└── preprocessed-data-pv and preprocessed-data-pvc

Training > trains the GBT model, and saves and loads the model; additionally builds the model PV and PVC
├── training-kubemanifest.yaml
│   └── deployment 
│   	└── training-app
│   └── service 
│   	└── training-service
│   └── PV and PVC 
│   	└── preprocessed-data-pv and preprocessed-data-pvc
│   	└── model-pv and model-pvc

Inference > makes a comparison between model's prediction against actual values
├── inference-kubemanifest.yaml
│   └── deployment 
│   	└── inference-app
│   └── service 
│   	└── inference-service
│   └── PV and PVC 
│   	└── preprocessed-data-pv and preprocessed-data-pvc
│   	└── model-pv and model-pvc

Prediction > makes predictions based on new, unseen data given by the user
├── inference-kubemanifest.yaml
│   └── deployment 
│   	└── prediction-app
│   └── service 
│   	└── prediction-service
│   └── PV and PVC 
│   	└── preprocessed-data-pv and preprocessed-data-pvc
│   	└── model-pv and model-pvc


PV and PVC Storage
raw-data-pv
├── raw_data 			 	# Mounted at /mnt/raw_data within the minikube VM
│   └── coffee_shop.csv
preprocessed-pv
├── preprocessed_data 	   	# Mounted at /mnt/preprocessed_data within the minikube VM
│   └── X_test.csv
│   └── X_train.csv
│   └── y_test.csv
│   └── y_train.csv
│   └── results.json
model-pv
├── model 			    	# Mounted at /mnt/model within the minikube VM
│   └── gbt_model.pkl


File directory
coffee_k8/ 
├── raw_data/			 	# Contains the raw dataset
│   └── coffee_shop.csv
├── script/ 				# Holds .py files, and dockerfiles for image building
│   └── dockerfile-preprocessing
│   └── dockerfile-training
│   └── dockerfile-prediction
│   └── dockerfile-inference
│   └── preprocessing.py
│   └── modelTraining.py
│   └── prediction.py
│   └── inference.py
│   └── preprocessing-requirements.txt
├── k8/ 					# Holds manifest files needed for deployment
│   └── preprocessing-kubemanifest.yaml
│   └── training-kubemanifest.yaml
│   └── prediction-kubemanifest.yaml
│   └── inference-kubemanifest.yaml
│   └── website.yaml
├── template/ # Holds the template for website
│   └── index.php
└── docker-compose.yml		# Compose file for testing with docker
└── run.sh            		# Runs k8s cluster
└── coffee-slides.pptx		# Slides
└── README.md            	# README

User's guide
# BEFORE RUNNING, change the file directories in the run.sh file
# Running with run.sh
# In WSL command line,
cd /mnt/c/Users/your-user/your-file-path/coffee
./run.sh
# If unable to run ./run.sh directly, download dos2unix
sudo apt-get install dos2unix
./run.sh 					# Runs the entire deployment
>> Access the application through localhost:8081

Localhost routes
website > localhost:8081
preprocessing > localhost:8080
inference > localhost:8083
prediction > localhost:8084


