import pylab
import pydicom
import sys
ImageFile=pydicom.read_file(sys.argv[1])
print(sys.argv[1].replace("dcm","tiff"))
pylab.imsave(sys.argv[1].replace("dcm","tiff"),ImageFile.pixel_array,cmap=pylab.cm.bone)
