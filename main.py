import os
from PyQt5.QtWidgets import*

from PyQt5.QtCore import Qt#en boy oranını boyutlardımak için kullanılır
from PyQt5.QtGui import QPixmap#Ekranda görüntülenecek resmi optimize eder.
from PIL import Image

#3.hafta
from PIL.ImageQt import ImageQt #grafikleri pillowdan Qt ye çevirmek için
from PIL.ImageFilter import*

app=QApplication([])
win=QWidget()
win.resize(700,500)
win.setWindowTitle('Easy Editor')
lb_image=QLabel("Resim gelecek")
btn_dir=QPushButton("Dosya")
lw_files=QListWidget()

btn_left=QPushButton("Sol")
btn_right=QPushButton("Sağ")
btn_flip=QPushButton("Ayna")
btn_sharp=QPushButton("Keskinlik")
btn_bw=QPushButton("S/B")

#hizalama
row=QHBoxLayout() #ana satır
col1=QVBoxLayout()#1.dikey
col2=QVBoxLayout()#2.dikey
col1.addWidget(btn_dir)
col1.addWidget(lw_files)
col2.addWidget(lb_image, 95)
row_tools=QHBoxLayout()
row_tools.addWidget(btn_left)
row_tools.addWidget(btn_right)
row_tools.addWidget(btn_flip)
row_tools.addWidget(btn_sharp)
row_tools.addWidget(btn_bw)
col2.addLayout(row_tools)

row.addLayout(col1,20)
row.addLayout(col2,80)
win.setLayout(row)

win.show()

def filter(files,extensions):
    result =[]
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result

#2.hafta
def chooseWorkdir():
    global workdir
    workdir =QFileDialog.getExistingDirectory()

def showFilenamesList():
    extensions=['.jpg','.jpeg','.png','.gif','.bmp']
    chooseWorkdir()
    filenames=filter(os.listdir(workdir),extensions)
    lw_files.clear()
    for filename in filenames:
        lw_files.addItem(filename)

class ImagePrecessor():
    def __init__(self):
        self.image=None 
        self.dir=None 
        self.filename=None
        self.save_dir="Modified/"
    
    def loadImage(self,dir,filename):
        '''Yükleme sırasında dosya yolunu ve adını hatırlıyoruz.'''
        self.dir = dir #dosya yol
        self.filename = filename
        image_path = os.path.join(dir,filename)
        #çalışma klasörüne giden yolda dosya adı ve yolu oluştur.
        self.image =Image.open(image_path)#resmi aç.
    
    def do_bw(self):
        self.image = self.image.convert("L")#siyah yap
        self.saveImage()#kaydet
        image_path=os.path.join(self.dir,self.save_dir,self.filename)#yola ulaş
        self.showImage(image_path)#göster.
    
    def saveImage(self):
        '''dosyanın bir kopyasını alt klasöre kaydeder'''
        path =os.path.join(self.dir,self.save_dir)
        #os.path.exists(path)---belirtilen yol varsa 
        # os.path.isdir(path)---yol bir liste veye dizin mi
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)#yeni dizin oluşturduk.
        image_path = os.path.join(path, self.filename)#dosyaya gidiyoruz.
        self.image.save(image_path)#kaydet

    #3.hafta
    #geçerli resmi uygulama pencerisinde gösterme
    def showImage(self, path):
        lb_image.hide()
        pixmapimage = QPixmap(path)#dosyanı ntam yolunda grafikleri görüntülemek için QPixmap nesnesi oluşturduk
        w, h = lb_image.width(), lb_image.height()#resmi yerleştirmek için alanın boyutlarını öğrendik.
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)#kırpma olmadan resmi boyutlandırdık.
        lb_image.setPixmap(pixmapimage)#resmi yerleştiriyoruz.
        lb_image.show()

    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)#alt klasör olan modified e kaydediyoruz.
        self.showImage(image_path)

    

    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_sharpen(self):
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)   

    #programdaki yazılı işlevi uygulamak için,görüntü adları listesinin bir öğesinde tuşlama işlevi oluşturalım
def showChosenImage():
    if lw_files.currentRow() >= 0:#liste öğesi boş değilse.
        filename = lw_files.currentItem().text()#dosya isimlerimdem herhangi birine tıklandığında dosyann adını al
        workimage.loadImage(workdir,filename)#seçilen resmin yüklenmesi. dosya listesinden ve isinden
        image_path=os.path.join(workimage.dir,workimage.filename)#yol ve isimden dosyaya ulaştık
        #workimage.showImage(os.path.join(workdir, workimage.filename))
        workimage.showImage(image_path)

workimage=ImagePrecessor() 
lw_files.currentRowChanged.connect(showChosenImage)


btn_bw.clicked.connect(workimage.do_bw)
btn_dir.clicked.connect(showFilenamesList)

#3.hafta
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_sharp.clicked.connect(workimage.do_sharpen)
btn_flip.clicked.connect(workimage.do_flip)




app.exec()
