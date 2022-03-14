################################################################
# File unserializing the .pickle file resulting from training calling the stgem library and starting the training Job #
################################################################

import dill
from stgem.job import JobResult
from pprint import pprint

file_name = "stgem_call.pickle"

jobres = JobResult.restore_from_file(file_name)

#print(jobres.description)
#print(jobres.test_suite)
print("Success: " + str(jobres.success))
print("Timestamp: " + str(jobres.timestamp))

print("Test suite and result : ")
for i in range(0, 79):
    print(jobres.test_repository.get(i))

# print("Whole JobResult Object :")
# print(vars(jobres))
