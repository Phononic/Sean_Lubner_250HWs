AY250 Homework 4
Sean Lubner

################ General ################
There are 3 main ipython notebooks:

* hw4_features_dev.ipynb is used to extract features from the 50_categories and pickle the resulting rectangularized data as extracted_features.p.  This notebook may be used to re-create this training data set pickle if desired (in which case run both code block cells, in order).  Depending on the computer, this will take around 3 hours.

* hw4_classifier_dev.ipynb is used to create and train an optimal random forest classifier on the training data set generated from hw4_features_dev.ipynb.  This file also pickles the classifier as trained_classifier.p for use on a later validation set.  This notebook should be used to re-create the classifier pickle.

* hw4_final.ipynb is used by the grader to load the classifier generated from hw4_classifier_dev.ipynb and apply it to a validation set of images.


################ Applying to Validation Set ################
The ipython notebooks hw4_classifier_dev.ipynb and hw4_final.ipynb should be used by the grader to evaluate the classifier on a validation set.  

Step 1: (create classifier)
run the hw4_classifier_dev.ipynb notebook (or, if prefered, save the notebook as a .py file, and run that).  This will create and pickle a random forest classifier, trained_classifier.p, based on the already pickled training data, extracted_features.p (the grader is asked to recreate the classifier pickle to avoid uploading a very large classifier pickle file to github ~ 270 MB).  This notebook will also provide comprehensive feedback metrics for this classifier.  Depending on the computer, this will take around a couple minutes to run.

Step 2: (prepare namespace)
run the first main code block cell in the hw4_final.ipynb notebook (or, if prefered, save the notebook as a .py file, and run that).  This will populate the namespace with the necessary functions to perform the feature extraction and classification.  

Step 3: (feature extraction & classification)
With the namespace populated, call the function: 
	(predictions, file_names) = run_final_classifier(path, forest="./trained_classifier.p")
where 'path' should be the absolute or relative directory to the validation image set, and 'forest' should be the path to the pickled trained classifier (already set as default).

Calling this function will provide on-screen feedback regarding progress, and will generate an Output.txt file with all the predictions for the validation image set in the same directory.  It will also store the predictions, along with a list of the validation image file names, in the variables 'predictions' and 'file_names' respectively (assuming the function call is made as shown above) for automated grading and convenience purposes.  Depending on the computer, this will take around 2.5 seconds per image to run.


################ Features List ################
Note 1: features are neatly listed and documented in the code as well (hw4_features_dev.ipynb).
Note 2: for efficiency, I will describe similarly groupable features with common language, rather than listing each one individually.  They are, for the most part, self-explanatory.  The full documentation is in the notebook.

* image size (number of pixels), and aspect ratio (width/height)
* the average value, median value, and standard deviation of the red, green, blue, and luminosity (combined RGB) channels
* the average value, median value, and standard deviation of the pixel value for vertical and horizontal edge maps, as well as the proportion of pixels above a certain threshold value for the vertical and horizontal edge maps.
* The number of image peaks

-- The above totals 23 features in all


################ Classifier Metrics ################
Note: all of these metrics are visible in the code as well (hw4_classifier_dev.ipynb)

Best Score = 31 % accuracy (for 10-fold CV)
Random Guessing = 2% ( = 1/(# of classes) )
Machine learning is more than 15 times better than random guessing!

Top 3 features (see notebook for full ranked list):
1) aspect ratio of image (unexpected...)
2) pixel count / size of image (also unexpected...)
3) number of image peaks (makes more sense) 
