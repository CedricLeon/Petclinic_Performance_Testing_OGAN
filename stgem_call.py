################################################################
# File calling the stgem library and starting the training Job #
################################################################

from stgem.job import Job
from adapter import Adapter

def myAdapter(input: [[-1, 1], [-1, 1]]) -> [[0, 100]]:  # 100 because of getFakeRewardFromEndpoint()
    adapter = Adapter()
    o1 = adapter.inputToEndpoint((input[0], input[1]), 0)  # 1: DEBUG = True
    return [100/(1+o1)]

description = {
    "sut": "python.PythonFunction",
    "sut_parameters": {"function": myAdapter},
    "objective_func": ["Minimize"],
    "objective_func_parameters": [
        {"selected": [0], "invert": True, "scale": True}],
    "objective_selector": "ObjectiveSelectorMAB",
    "objective_selector_parameters": {"warm_up": 30},
    "algorithm": "ogan.OGAN",
    "algorithm_parameters":
        {"input_dimension": 2,
         "use_predefined_random_data": False,
         "predefined_random_data": {"test_inputs": None, "test_outputs": None},
         "fitness_coef": 0.95,
         "train_delay": 0,
         "N_candidate_tests": 1,
         "ogan_model": "model_keras.OGANK_Model",
         "ogan_model_parameters": {
             "optimizer": "Adam",
             "d_epochs": 10,
             "noise_bs": 10000,
             "g_epochs": 1,
             "d_size": 512,
             "g_size": 512,
             "d_adam_lr": 0.001,
             "g_adam_lr": 0.0001,
             "noise_dimensions": 50,
             "noise_batch_size": 10000
         },
         "train_settings_init": {"epochs": 1, "discriminator_epochs": 10, "generator_epochs": 1},
         "train_settings": {"epochs": 1, "discriminator_epochs": 10, "generator_epochs": 1}
         },
    "job_parameters": {"max_tests": 80, "N_random_init": 20}
}

r = Job(description).start()
r.dump_to_file("stgem_call.pickle")
