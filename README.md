# nyaaCategorizer

Data located at: <br>
[nyaaCategorizer_database repo](https://github.com/hiddenMedic/nyaaCategorizer_database) <br><br>

<h2>Models</h2> <br>
Model 1 <br>
trainModel.zip, nyaaCategorizer.ipynb <br>
accuracy: 0.5989, cr accuracy: 0.28 <br>

Model 2 <br>
trainModel_balanced.zip, nyaaCategorizer_balanced.ipynb <br>
accuracy: 0.1159, cr accuracy: 0.03 <br> 
+ balanced classes (class_weights) <br> <br>

Model 3 <br>
trainedModel_balanced_nosub_extra.zip, nyaaCategorizer_balanced_nosub_extra.ipynb <br>
accuracy: 0.987, cr accuracy: 0.57 <br>
+ balansirane klase (class_weights) <br>
+ only look at the main category (subcategories converted) <br>
+ extra <br>
extra = { <br> 
    + shuffle the dataset at the beginning, //irrelevant <br>
    + removed fileAmount feature, <br> 
    + removed more100File feature, <br>
    + increased epochs from 5 to 10, <br>
    + decreased batch size from 100 to 64, <br>
    + removed Dropout layers, <br>
    + learning_rate=0.0001 <br>
} <br> <br>

Model 4 <br>
trainedModel_balanced_nosub_extra_maincat.zip, nyaaCategorizer_balanced_nosub_maincats_extra.ipynb <br>
accuracy=0.9919, cr accuracy: 0.56 <br>
+ balansirane klase (class_weights) <br>
+ only look at the main category (subcategories converted)<br>
+ discard all data that is 'Software' or 'Pictures' since there isnt a lot of it<br>
+ extra /\<br>
+ use only one mid layer instead of 3<br>
+ removed "from_logits=True"<br>
+ changed accuracy to categorical_accuracy<br>
versions = {<br>
    1. above + removed Software and Pictures data<br>
    2. added back fileAmount = same<br>
    3. only one mid layer (instead of 3) -- best performance (f1: 0.59)<br>
    4. removed "from_logits=True", changed accuracy to categorical_accuracy - same as always<br>
}<br><br>

Model 5<br>
trainedModel_final.zip, nyaaCategorizer_final.ipnyb<br>
accuracy: 0.9907, cr accuracy: 0.58 <br>
+ no class balancing<br>
+ only look at the main category (subcategories converted)<br>
+ discard all data that is 'Software' or 'Pictures' since there isnt a lot of it<br>
+ back to 3 Dense layers <br>
+ added metrics<br><br>

Model 6<br>
trainedModel_LSTM.zip, nyaaCategorizer_lstm.ipynb<br>
accuracy: 0.9860, cr accuracy: 0.57<br>
+ LSTM with 2 dense layers of 128 and 64 nodes<br><br>

Model 7<br>
nyaaCategorizer_final_allcats.zip, nyaaCategorizer_final_allcats.ipynb<br>
accuracy: 0.9189, cr accuracy: 0.27<br>
+ same as final, but on all categories, with class balancing<br><br>

Model 8<br>
nyaaCategorizer_final_allmaincats.zip, nyaaCategorizer_final_allmaincats.ipnyb<br>
accuracy: 0.9903, cr accuracy: 0.57<br>
+ same as final, but on all main categories<br><br>

<h2>Figures</h2><br>
Lograithm of sorted file sizes: <br>
<img src="https://github.com/hiddenMedic/nyaaCategorizer/blob/main/images/2_logFilesize.png?raw=true">
Model1 evaluation: <br>
<img src="https://github.com/hiddenMedic/nyaaCategorizer/blob/main/images/model1/6_evaluate.png?raw=true">
Model1 classification report: <br>
<img src="https://github.com/hiddenMedic/nyaaCategorizer/blob/main/images/model1/7_classificationReport.png?raw=true">
Model1 confusion matrix: <br>
<img src="https://github.com/hiddenMedic/nyaaCategorizer/blob/main/images/model1/8_confusionMatrix.png?raw=true">

Refer to /images for other figures. 
