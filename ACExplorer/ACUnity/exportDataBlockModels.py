from ACExplorer.ACUnity.decompressDatafile import decompressDatafile
from ACExplorer.misc import tempFiles
from ACExplorer.misc.dataTypes import BEHEX2, LE2DEC2, float32
from ACExplorer.misc.exportOBJMulti import exportOBJMulti
from ACExplorer.ACUnity import format
import sys


def exportDataBlockModels(fileTree, fileList, fileID):
	if not tempFiles.exists(fileID):
		decompressDatafile(fileTree, fileList, fileID)
	data = tempFiles.read(fileID)
	if len(data) == 0:
		raise Exception('file '+fileID+' is empty')
	data = data[0]

	if data['resourceType'] != 'AC2BBF68':
		return
	
	if 'dev' in sys.argv:
		reload(format)  # for development
	dataBlock = format.format(fileTree, fileList, fileID)
	# fileID, data and dataBlock all relate to the DataBlock file (Type AC2BBF68)
	# This is a list of every file called by that DataBlock
	# format.format will return this list of files into dataBlock
	
	fileIDList = []
	
	for n, fileID2 in enumerate(dataBlock['dataBlock']):
		if not tempFiles.exists(fileID2):
			decompressDatafile(fileTree, fileList, fileID2)
		data2 = tempFiles.read(fileID2)
		if len(data2) == 0:
			raise Exception('file '+fileID2+' is empty')
		data2 = data2[0]
		
		print 'Reading '+data2['fileName']+'. '+str(n+1)+' of '+str(len(dataBlock['dataBlock']))
	
		dataBlockChild = format.format(fileTree, fileList, fileID2)
		# fileID2, data2 and dataBlockChild all relate to the files contained in
		# the DataBlock file. The file could be of a number of types including
		# entities and entity groups
		if dataBlockChild['fileType'] == '0984415E':
			if 'LOD' in dataBlockChild and len(dataBlockChild['LOD']) > 0:
				fileID3 = dataBlockChild['LOD'][0]['fileID']
				if not tempFiles.exists(fileID3):
					decompressDatafile(fileTree, fileList, fileID3)
				data3 = tempFiles.read(fileID3)
				if len(data3) == 0:
					raise Exception('file '+fileID3+' is empty')
				data3 = data3[0]
				if data3['resourceType'] == '415D9568':
					fileIDList.append({'fileID':fileID3, 'transformationMtx': dataBlockChild['transformationMtx']})
				else:
					raise Exception(fileID3+' is not a 3D model')
		
		
		
		else:
			print 'Could not read following file. Unsupported type.'
			print data2['fileName']
			print dataBlockChild['fileType']
			print dataBlockChild['fileID']
	
	# fIn = open(data['dir'], 'rb')
	# fIn.seek(14)

	# count = LE2DEC2(fIn.read(4))
	# fileIDList = {}
	# ticker = 0
	# for n in range(count):
		# fIn.seek(2,1)
		# fileID2 = BEHEX2(fIn.read(8)).upper()
		# if not tempFiles.exists(fileID2):
			# decompressDatafile(fileTree, fileList, fileID2)
		# data2 = tempFiles.read(fileID2)
		# if len(data2) == 0:
			# raise Exception('file '+fileID2+' is empty')
		# data2 = data2[0]
		
		# print 'Reading '+data2['fileName']+'. '+str(n+1)+' of '+str(count)

		# if data2['resourceType'] == '0984415E':
			# fIn2 = open(data2['dir'], 'rb')
			# fIn2.seek(14)
			# fIn2.seek(49, 1)
			# xpos = float32(fIn2.read(4))
			# ypos = float32(fIn2.read(4))
			# zpos = float32(fIn2.read(4))
			# filePointer = fIn2.tell()
			# tempFile = fIn2.read()
			# meshLoc = tempFile.find('\x3B\x96\x6E\x53')
			# if meshLoc == -1:
				# continue
			# fIn2.seek(filePointer)
			# fIn2.seek(meshLoc+5, 1)
			# fileID3 = BEHEX2(fIn2.read(8)).upper()
			# if not tempFiles.exists(fileID3):
				# decompressDatafile(fileTree, fileList, fileID3)
			# data3 = tempFiles.read(fileID3)
			# if len(data3) == 0:
				# raise Exception('file '+fileID3+' is empty')
			# data3 = data3[0]
			# if data3['resourceType'] == '415D9568':
				# fileIDList[ticker] = {'id':fileID3, 'x':xpos, 'y':ypos, 'z':zpos}
				# ticker += 1
			# else:
				# raise Exception(fileID3+' is not a 3D model')
				
	print 'done reading'
	print 'exporting'

	exportOBJMulti(fileTree, fileList, fileID, fileIDList)
	
	print 'Done'