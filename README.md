This code is used to fine-tune a pre-trained model for semantic segmentation of clouds in images, and to make predictions using the model.
* To control the training parameters (learning rate, number of epochs, batch size, etc.) and adapt it to different images (image size, number of channels, etc.), change the appropriate value in the global_params.py file.
* In order to train the model run the main_train.py script, in order to run the prediction run the main_test.py script.
* The pre-process method and loss function can be controled from those scripts, by changing the preprocess_type argument. 
* The data is expected in the path '/opt/DL_project/', under 'Training' and 'Test' directories. If you want to chane the path you need to adjust it in the scripts mantianed above.
* The pre-trained model can be downloaded from https://vault.sfu.ca/index.php/s/2Xk6ZRbwfnjrOtu
* This work is based on the work described here: https://github.com/SorourMo/Cloud-Net-A-semantic-segmentation-CNN-for-cloud-detection/tree/master?tab=readme-ov-file
