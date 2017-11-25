from networks.network_new import *

net = Network()
net.train(train_csv="20sec_expand_bootstrap/balanced_labels_SDM_bootstrap5_train.csv",
          validate_csv="20sec_expand_bootstrap/balanced_labels_SDM_bootstrap5_val.csv", 
          spectrs_dir="20sec_expand_bootstrap/spectro5/",
          nb_epochs=100000000,
          verbose_step=3,
          model_name="balanced_20sec_1gpu_good_spectro_expand_dataset_bootstrap5")