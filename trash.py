from networks.network import *

net = Network()
net.train(train_csv="40sec/spectrs_40sec_labels_train.csv",
          validate_csv="40sec/spectrs_40sec_labels_train.csv", 
          spectrs_dir="40sec/spectrs_40sec/",
          nb_epochs=100000000,
          verbose_step=10,
          model_name="40sec")