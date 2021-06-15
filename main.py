import GenerateData
import SetSFwithOurMethod

NumArray = [100, 200, 300, 400, 500]
for i in range(len(NumArray)):
    GenerateData.Generate(NumArray[i], [0, 200])
    SetSFwithOurMethod.SetSF(NumArray[i], 4.5)