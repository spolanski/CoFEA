from paraview.simple import *
import glob as gb

# trace generated using paraview version 5.9.1
def csv(name):
#### disable automatic camera reset on 'Show'
	paraview.simple._DisableFirstRenderCameraReset()

# create a new 'XML Unstructured Grid Reader'
	path = '/home/maciej/Documents/CoFEA/Hertz/CCX/CoFEA/Results/post/' + name
	veryfinequadhexvtu = XMLUnstructuredGridReader(registrationName=name, FileName=[path])
	veryfinequadhexvtu.CellArrayStatus = []
	veryfinequadhexvtu.PointArrayStatus = ['U', 'S', 'S_Mises', 'S_Principal', 'E', 'E_Mises', 'E_Principal', 'CONTACT', 'ERROR']
	veryfinequadhexvtu.TimeArray = 'TimeValue'

# Properties modified on veryfinequadhexvtu
	veryfinequadhexvtu.TimeArray = 'None'

	UpdatePipeline(time=0.0, proxy=veryfinequadhexvtu)


	# create a new 'Plot Over Line'
	plotOverLine1 = PlotOverLine(registrationName='PlotOverLine1', Input=veryfinequadhexvtu,
    		Source='Line')
	plotOverLine1.PassPartialArrays = 1
	plotOverLine1.ComputeTolerance = 1
	plotOverLine1.Tolerance = 2.220446049250313e-16

# init the 'Line' selected for 'Source'
	plotOverLine1.Source.Point1 = [0.0, 0.0, 0.0]
	plotOverLine1.Source.Point2 = [0.0, -5.0, 0.0]
	plotOverLine1.Source.Resolution = 1000

	UpdatePipeline(time=1.0, proxy=plotOverLine1)
	
	
# save data
	save_path_1 = path.replace('.vtu','_ccx_mises.csv')
	save_path_2 = save_path_1.replace('Meshes','CSV/Mises')
	SaveData(save_path_2, proxy=plotOverLine1, WriteTimeSteps=0,
    		Filenamesuffix='_%d',
    		ChooseArraysToWrite=0,
		PointDataArrays=['CONTACT', 'E', 'ERROR', 'E_Mises', 'E_Principal', 'S', 'S_Mises', 'S_Principal', 'U', 'arc_length', 'vtkValidPointMask'],
		CellDataArrays=[],
		FieldDataArrays=[],
    		VertexDataArrays=[],
    		EdgeDataArrays=[],
    		RowDataArrays=[],
    		Precision=5,
    		UseScientificNotation=0,
    		FieldAssociation='Point Data',
    		AddMetaData=1,
    		AddTime=0)

	# create a new 'Plot Over Line'
	plotOverLine2 = PlotOverLine(registrationName='PlotOverLine2', Input=veryfinequadhexvtu,
    		Source='Line')
	plotOverLine2.PassPartialArrays = 1
	plotOverLine2.ComputeTolerance = 1
	plotOverLine2.Tolerance = 2.220446049250313e-16

# init the 'Line' selected for 'Source'
	plotOverLine2.Source.Point1 = [0.0, 0.0, 0.0]
	plotOverLine2.Source.Point2 = [5.0, 0.0, 0.0]
	plotOverLine2.Source.Resolution = 1000

	UpdatePipeline(time=1.0, proxy=plotOverLine1)
	
	
# save data
	save_path_3 = save_path_2.replace('_ccx_mises.csv','_ccx_sigmayy.csv')
	save_path_4 = save_path_3.replace('Mises','Sigma_yy')
	SaveData(save_path_4, proxy=plotOverLine1, WriteTimeSteps=0,
    		Filenamesuffix='_%d',
    		ChooseArraysToWrite=0,
		PointDataArrays=['CONTACT', 'E', 'ERROR', 'E_Mises', 'E_Principal', 'S', 'S_Mises', 'S_Principal', 'U', 'arc_length', 'vtkValidPointMask'],
		CellDataArrays=[],
		FieldDataArrays=[],
    		VertexDataArrays=[],
    		EdgeDataArrays=[],
    		RowDataArrays=[],
    		Precision=5,
    		UseScientificNotation=0,
    		FieldAssociation='Point Data',
    		AddMetaData=1,
    		AddTime=0)



result_file_names = gb.glob("Meshes/*.vtu")

for result_file_name in result_file_names:
	
	csv (result_file_name) 
