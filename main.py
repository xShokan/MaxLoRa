import GenerateData
import SetSFwithOurMethod

NumArray = [100, 300, 400, 500, 600]
for i in range(len(NumArray)):
    GenerateData.Generate(NumArray[i], [[50, 100], [50, 150], [100, 200], [150, 250], [200, 300], [250, 350]])
    SetSFwithOurMethod.SetSF(NumArray[i], 6, 4.8, 4)
    break