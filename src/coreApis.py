from params import params

class coreApis():
    def __init__(self):
        param=params()
        self.GetDataProject = param.coreurl + '/sys/dataproject'
        self.GetDataFile = param.coreurl + '/sys/datafile'

        self.Upload = param.coreurl + '/data/upload'
        self.Download = param.coreurl + '/data/download'
        self.GetColumn = param.coreurl + '/data/getcol' 
        self.GetFileStatus = param.coreurl + '/data/getstatus'
        self.DeleteFile = param.coreurl + '/data/delete'

        self.GetImg = param.coreurl + '/viz/getimg'
        self.GetDataVizAlgoList = param.coreurl + '/viz/data/getalgo'
        self.DoDataViz = param.coreurl + '/viz/data/do'

        self.GetPreprocessAlgoList = param.coreurl + '/preprocess/getalgo'
        self.DoPreprocess = param.coreurl + '/preprocess/do'
        self.PreviewPreprocess = param.coreurl + '/preprocess/preview'
        self.GetCorrelationAlgoList = param.coreurl + '/correlation/getalgo'
        self.DoCorrelation = param.coreurl + '/correlation/do'
        self.GetAnalyticAlgo = param.coreurl + '/analytic/getalgo'
        self.GetAnalyticAlgoParam = param.coreurl + '/analytic/getparam'
        self.DeleteModel = param.coreurl + '/analytic/delete'
        self.DoModelTrain = param.coreurl + '/analytic/train'
        self.GetModelStatus = param.coreurl + '/analytic/get/status'
        self.GetModelPreview = param.coreurl + '/analytic/preview'
        self.DoModelPredict = param.coreurl + '/analytic/predict'
        self.DoModelTest = param.coreurl + '/analytic/test'
        self.GetModelParameter = param.coreurl + '/analytic/get/param'
        self.GetModelFailReason = param.coreurl + '/analytic/get/fail'
        self.StopTraining = param.coreurl + '/analytic/stop'



