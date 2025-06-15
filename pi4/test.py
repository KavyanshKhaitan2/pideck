from PIL import Image
from PIL.ImageQt import ImageQt
from io import BytesIO
import base64
from PySide6.QtGui import QPixmap

img = 'R0lGODlhDwAPAKECAAAAzMzM/////wAAACwAAAAADwAPAAACIISPeQHsrZ5ModrLlN48CXF8m2iQ3YmmKqVlRtW4MLwWACH+H09wdGltaXplZCBieSBVbGVhZCBTbWFydFNhdmVyIQAAOw==' 

im = Image.open(BytesIO(base64.b64decode(img)))
qim = ImageQt(im)
pix = QPixmap.fromImage(qim)
