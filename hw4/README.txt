AY250 Homework 4
Sean Lubner

################ General ################
There are 3 main ipython notebooks:
* hw4_features_dev is used to extract features from the 50_categories and pickle the resulting rectangularized data.  This notebook may be used to re-create this training data set pickle if desired.
* hw4_classifier_dev is used to create and train an optimal random forest classifier on the training data set generated from hw4_features_dev.  This file also pickles the classifier for use on a later validation set.  This notebook should be used to re-create the classifier pickle if.
* hw4_final is used by the grader to load the classifier generated from hw4_classifier_dev and apply it to a validation set of images.


################ Applying to Validation Set ################
The ipython notebooks hw4_classifier_dev and hw4_final should be used by the grader to evaluate the classifier on a validation set.  

Step 1:
run the hw4_classifier_dev notebook (or, if prefered, save the notebook as a .py file, and run that).  This will create and pickle a random forest classifier based on the already pickled training data (to avoid sending a very large classifier pickle file through github).  This will also provide feedback metrics on this classifier

Step 2:
run the hw4_final notebook (or, if prefered, save the notebook as a .py file, and run that).  This will populate the namespace with the necessary functions.  

Step 3:
Call the function: 
	(predictions, file_names) = run_final_classifier(path, forest="./trained_classifier.p")
where path should be the absolute or relative directory to the validation image set, and forest should be the path to the pickled trained classifier (set as default).
Calling this function will provide on-screen feedback regarding progress, and will generate a .txt file with all the predictions for the validation image set in the same directory.  It will also store the predictions, along with a list of the validation image file names, in the variables 'predictions' and 'file_names' respectively (assuming the function is called as shown above).


################ Features List ################
Note 1: features are neatly listed and documented in the code as well (hw4_features_dev).
Note 2: for efficiency, I will describe similarly groupable features with common language, rather than listing each one.  They are, for the most part, self-explanatory.

* image size (number of pixels), and aspect ratio (width/height)
* the average value, median value, and standard deviation of the red, green, blue, and luminosity (combined RGB) channels
* the average value, median value, and standard deviation of the pixel value for vertical and horizontal edge maps, as well as the proportion of pixels above a certain threshold value for the horizontal and vertical edge maps.
* The number of image peaks

-- The above totals 23 features in all


################ Classifier Metrics ################
Note: all of these metrics are visible in the code as well (hw4_classifier_dev)
Best Score = 
Random Guessing = 2% ( = 1/(# of classes) )
Machine learning is 14 times better than random guessing

Top 3 features (see notebook for full importance list):
