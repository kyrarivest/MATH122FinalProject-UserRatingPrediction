# MATH122 FinalProject - User Rating Prediction

Our final project for MATH 122 uses a K-nearest neighbors inspired model to predict product ratings for 4500 given users.

The data we are given two data sets: 
- [[https://c569257608da4dcaafbc-my.sharepoint.com/:x:/g/personal/kyrarivest_brandeis_edu/ESnHmQiYEqtEuUTzZBAM9aMBa4lJ11yGAOXs3PN4rxFfKg?e=WGI6ZD][user_history.csv]]: provides the browser history times of 4500 users for 100 different websites
- [[https://c569257608da4dcaafbc-my.sharepoint.com/:x:/g/personal/kyrarivest_brandeis_edu/Edf-Cftx1QBEg4nT0CrTVMABGhJfDwSN6SKW3Vd9Yry8RA?e=faePVb][user_ratings.csv]] : provides the product ratings of 3000 different users for 75 different products. All 3000 users provide the ratings of some but not all 75 products.

* File Descriptions

This repository includes four different files for the model.



My project builds off a method called ~ClassicalGSG~
and has introduced by the Dickson Lab in [[https://github.com/ADicksonLab/ClassicalGSG][ClassicalGSG: Prediction of logP Using Classical
Molecular Force Fields and Geometric Scattering for Graphs]]. The goal was to build off of this project by studying how to model behavees when the size of the feature space is decreased.

There are seven datasets that that was used in this project: FDA, Huuskonen, NonStar, Star, OpenChem, SAMPL6, and SAMPL7. The method used to reduce the size of the feature space is [[https://jakevdp.github.io/PythonDataScienceHandbook/05.09-principal-component-analysis.html][principal component analysis (PCA)]]. This repository contains serveral run examples, each using a different number of PCA components. Below are instructions for how to simulate a new example.




* Installation

You will need to download this repository. Navigate to where you want this repo to go on your computer and type:

#+begin_src sh
  git clone https://github.com/kyrarivest/ACRES_REU_Project_2021.git
#+end_src

You will also need to install a couple packages if you do not already have them:

#+begin_src sh
  conda install -c pytorch pytorch
  conda install -c scikit-learn
  conda install -c matplotlib
#+end_src

You can also check to see if you have them installed:

#+begin_src sh
  conda list | grep scikit-learn
  conda list | grep pytorch
  conda list | grep matplotlib
#+end_src



* Usage: Training

You will first need to prepare the data to train the neural network model. You need to decide which dataset you want to train on and how many PCA components to use. Once you know this, navigate to the *prepare_data.sb* file under [[https://github.com/kyrarivest/ACRES_REU_Project_2021/blob/main/examples/prepare_data.sb][ClassicalGSG/examples/prepare_data.sb]]. To edit the file, enter it using the vi command:

#+BEGIN_SRC bash
 vi prepare.ab
 i
#+END_SRC

On the line that execute the *prepare_data.py* file, you have to replace the template inputs with your own. Specify:

- The number of PCA components (note: this cannot be larger than the numbeer of molecules in the dataset or else the PCA algorithm won't work)
- The dataset you want to use (choose ~FDA~, ~Huuskonen~, ~Star~, ~NonStar~, ~openchem~, ~SAMPL6~, or ~SAMPL7~)
- Wether you are preparing data to train the model or test it with a different dataseet than it was already trained on (choose ~train~ or ~test~)

Save your changes and exit the file:

#+BEGIN_SRC bash
 esc key
 :wq
#+END_SRC

Now run the *prepare_data.sb* file. This will copy the template directory [[https://github.com/kyrarivest/ACRES_REU_Project_2021/tree/main/examples/cgenffgsg][~classicalgsg~]] and create a new directory set up with the correct PCA number and dataset so that the model can be trained. The directory will be named *cgenffe + <PCA number>*. This directory will contain 5 ~train_run~ folders. The training is split up into these 5 folders for [[https://towardsdatascience.com/why-and-how-to-cross-validate-a-model-d6424b45261f][cross validation]]. To run the *prepare_data.sb* file:

#+BEGIN_SRC bash
 sbatch prepare_data.sb
#+END_SRC

Once the new directory has been generated, navigate into it. If this is not a new *cgenffe + <PCA number>* example (it has been trained before), first run the reset.py file to clear the example of it's existing models:

#+BEGIN_SRC bash
python reset.py
#+END_SRC

Then, to train the model, execute the *start_training.sh* file which will initiate training in all 5 ~train_run~ files:

#+BEGIN_SRC bash
sbatch start_training.sh
#+END_SRC

Wait until the training is finished which could take around 30-60min deepending on which dataset you use. If you do not set up email notifications in the *start_training.sh* file, you can check to see if the trianing is done by navigating into each ~train_run~ foldeer and looking at the *train-log*. When a training round is complete, the log will display the training time as the last line in the file.

* Usage: Testing
When the model has finished training, you can then test it. In the *cgenffe + <PCA number>* directory where you executed training, you can also execute testing. Note: if you are testing with a seperate dataset than you used for training, you will have to go back to the [[https://github.com/kyrarivest/ACRES_REU_Project_2021/blob/main/examples/prepare_data.sb][ClassicalGSG/examples/prepare_data.sb]] and re-prepare test data. Otherwise you can test right away. Navigate to the *cgenffe + <PCA number>* directory and run:

#+BEGIN_SRC bash
sbatch start_test.sh
#+END_SRC

This should not take more than 5 min to run. This will enter the testing [[https://www.investopedia.com/terms/r/r-squared.asp#:~:text=R%2Dsquared%20(R2),variables%20in%20a%20regression%20model.&text=It%20may%20also%20be%20known%20as%20the%20coefficient%20of%20determination.][R Squared]] and [[https://towardsdatascience.com/what-does-rmse-really-mean-806b65f2e48e#:~:text=Root%20Mean%20Square%20Error%20(RMSE)%20is%20a%20standard%20way%20to,model%20in%20predicting%20quantitative%20data.&text=This%20tells%20us%20heuristically%20that,the%20vector%20of%20observed%20values.][Root Mean Squared Error]] values into the *results.json* file. Next, run the *save_results.py* file to both print the results out to see and save the averages to the *results.txt* file located in the ~ClassicalGSG~ directory for easier result compiling.

#+BEGIN_SRC bash
python save_results.py
#+END_SRC

You can then view the [[https://github.com/kyrarivest/ACRES_REU_Project_2021/blob/main/examples/results.txt][*results.txt*]] file to see a list of the results for multiple PCA training/testing model examples if you run many. The first value is the r squared and the second value is the RMSE.
