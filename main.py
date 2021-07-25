import GenerateData
import SetSFwithOurMethod

NumArray = [200, 300, 400, 500, 600]
for i in range(len(NumArray)):
    GenerateData.Generate(NumArray[i], [[100, 200], [100, 200], [200, 300], [200, 300], [300, 400], [300, 400]])
    SetSFwithOurMethod.SetSF(NumArray[i], 6, 10, 4)