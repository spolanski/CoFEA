# trace generated using paraview version 5.9.1

#### import the simple module from the paraview
from paraview.simple import *
import glob as gb

def csv (name):

	#### disable automatic camera reset on 'Show'
	paraview.simple._DisableFirstRenderCameraReset()
	# create a new 'XML Unstructured Grid Reader'
	path = '/home/maciej/Documents/CoFEA/Hertz/Elmer/Post/' + name
	veryfinequadhexvtu = XMLUnstructuredGridReader(registrationName=name, FileName=[path])
	veryfinequadhexvtu.CellArrayStatus = ['GeometryIds']
	veryfinequadhexvtu.PointArrayStatus = ['stress_xx', 'stress_yy', 'stress_zz', 'stress_xy', 'stress_yz', 'stress_xz', 'vonmises', 'displacement contact distance', 'displacement contact gap', 			'displacement contact normalload', 'displacement contact slipload', 'displacement contact weight', 'displacement contact active', 'displacement contact stick', 'displacement', 'displacement 			contact load']
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
	plotOverLine1.Source.Point1 = [0, 0, 0.0]
	plotOverLine1.Source.Point2 = [0, -5.0, 0.0]
	plotOverLine1.Source.Resolution = 1000

	UpdatePipeline(time=1.0, proxy=plotOverLine1)

	# save data
	save_path_1 = path.replace('.vtu','_elmer_mises.csv')
	save_path_2 = save_path_1.replace('Meshes','CSV/Mises')
	SaveData(save_path_2, proxy=plotOverLine1, WriteTimeSteps=0,
	    Filenamesuffix='_%d',
	    ChooseArraysToWrite=0,
	    PointDataArrays=['GeometryIds', 'arc_length', 'displacement', 'displacement contact active', 'displacement contact distance', 'displacement contact gap', 'displacement contact load', 'displacement 			contact normalload', 'displacement contact slipload', 'displacement contact stick', 'displacement contact weight', 'stress_xx', 'stress_xy', 'stress_xz', 'stress_yy', 'stress_yz', 'stress_zz', 			'vonmises', 'vtkValidPointMask'],
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
	plotOverLine2.Source.Point1 = [0.0, -0.1, 0.0]
	plotOverLine2.Source.Point2 = [5.0, -0.1, 0.0]
	plotOverLine2.Source.Resolution = 1000




	# save data
	save_path_3 = save_path_2.replace('_elmer_mises.csv','_elmer_sigmayy.csv')
	save_path_4 = save_path_3.replace('Mises','Sigma_yy')

	SaveData(save_path_4, proxy=plotOverLine2, WriteTimeSteps=0,
	    Filenamesuffix='_%d',
	    ChooseArraysToWrite=0,
	    PointDataArrays=['GeometryIds', 'arc_length', 'displacement', 'displacement contact active', 'displacement contact distance', 'displacement contact gap', 'displacement contact load', 'displacement 			contact normalload', 'displacement contact slipload', 'displacement contact stick', 'displacement contact weight', 'stress_xx', 'stress_xy', 'stress_xz', 'stress_yy', 'stress_yz', 'stress_zz', 			'vonmises', 'vtkValidPointMask'],
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
