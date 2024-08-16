# Group - Alyssa, Ayumi, Terrence, Shae
> T2 Coffee k8s application

User's guide
#### BEFORE RUNNING, change the file directories in the run.sh file
###### Running with run.sh
######  In WSL command line,
cd /mnt/c/Users/your-user/your-file-path/coffee
./run.sh
######  If unable to run ./run.sh directly, download dos2unix
sudo apt-get install dos2unix
./run.sh 					# Runs the entire deployment
Access the application through localhost:8081

Localhost routes
website > localhost:8081
preprocessing > localhost:8080
inference > localhost:8083
prediction > localhost:8084


