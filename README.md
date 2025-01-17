# PS_MPI

## 1. Changes  
Refined version of ymliao98/PS_MPI   
1. Use config.yml to simplify settings  
2. Simplified process to make it general  
3. Cut out useless code to make it elegant  
4. add your own datasets and models  

## 2. Customize
#### 1. Own dataset  
1. create corresponding dataset_name.py in /datasets  
2. define it in /datasets/dataset_name.py and return train\test dataset transformed  
3. import it in /datasets/__init__.py


#### 2. Own model
1. create corresponding model_name.py in /models  
2. define it in /models/model_name.py and return model class 
3. import it in /models/__init__.py and decide when to use your model in create_model_instance()


## 3. Run
The number after should be larger than config.yml:num_workers  
mpiexec --oversubscribe -n 1 python server.py : -n 10 python client.py  


## 4. Analysis tools
#### 1. Save last training record to anther direction
This will put newest result in /results and also delete empty runs dirs. Don't use when training not finished.  
python analysis_tools/generate_results.py


#### 2. Generate pictures  
Modify this according to your need. The current version will print required results into on figure. Edit it as your wish.
python analysis_tools/draw_pics.py


## 4. Clear ALL log and saved models  
WARNING: Clear all logs!  
rm -rf model_save server_log clients_log config_save __pycache__ 