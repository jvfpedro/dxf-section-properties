import ezdxf
import numpy as np
from PIL import Image, ImageDraw
import rasterio
from rasterio.transform import from_origin

def dxf_para_tiff(dxfa, res=0.1, pixel_value=255, output_tif='secao.tif'):
	# --- LEITURA DO DXF ---
	doc = ezdxf.readfile(dxfa)
	msp = doc.modelspace()

	# --- ENCONTRAR BOUNDING BOX DA SEÇÃO ---
	all_coords = []
	for e in msp:
		if e.dxftype() == 'LINE':
			all_coords.append((e.dxf.start[0], e.dxf.start[1]))
			all_coords.append((e.dxf.end[0], e.dxf.end[1]))
		elif e.dxftype() == 'LWPOLYLINE':
			all_coords.extend([(point[0], point[1]) for point in e])
		elif e.dxftype() == 'POLYLINE':
			all_coords.extend([(v.dxf.location.x, v.dxf.location.y) for v in e.vertices()])

	xs, ys = zip(*all_coords)
	xmin, xmax = min(xs), max(xs)
	ymin, ymax = min(ys), max(ys)

	width = int((xmax - xmin) / res)
	height = int((ymax - ymin) / res)

	# --- CRIAR IMAGEM E DESENHAR ---
	img = Image.new('L', (width, height), color=0)
	draw = ImageDraw.Draw(img)

	def world_to_pixel(x, y):
		return int((x - xmin) / res), int((ymax - y) / res)

	for e in msp:
		if e.dxftype() == 'LINE':
			p1 = world_to_pixel(e.dxf.start[0], e.dxf.start[1])
			p2 = world_to_pixel(e.dxf.end[0], e.dxf.end[1])
			draw.line([p1, p2], fill=pixel_value)
		elif e.dxftype() in ['LWPOLYLINE', 'POLYLINE']:
			pts = [world_to_pixel(v[0], v[1]) for v in e.get_points()]
			draw.polygon(pts, fill=pixel_value)

	# --- SALVAR TIFF ---
	array = np.array(img)
	transform = from_origin(xmin, ymax, res, res)

	with rasterio.open(
		output_tif,
		'w',
		driver='GTiff',
		height=array.shape[0],
		width=array.shape[1],
		count=1,
		dtype=array.dtype,
		transform=transform
	) as dst:
		dst.write(array, 1)
            
	return img

class Calculador:

    def __init__(self):
        pass

    def processa(self, img, D):
        
        matriz = np.asarray(img)

        img_largura, img_altura = img.size

        #primeira linha
        for i in range(img_altura):
            if np.any(matriz[i] != 0):
                linha_ini = i
                break

        #ultima linha
        for i in range(img_altura-1,0,-1):
            if np.any(matriz[i] != 0):
                linha_fim = i
                break

        #dimensões
        n_linhas = linha_fim - linha_ini + 1
        b = h = D / n_linhas

        #centro de gravidade
        soma_Ay = 0
        soma_Ax = 0
        soma_A = 0
        for i in range(img_altura):
            for j in range(img_largura):
                if matriz[i][j] > 0:
                    A = b * h
                    x_linha = (linha_fim-i+1)*b - b/2
                    y_linha = (linha_fim-i+1)*h - h/2
                    soma_Ay += A * y_linha
                    soma_Ax += A * x_linha
                    soma_A += A

        X_linha = soma_Ax/soma_A
        Y_linha = soma_Ay/soma_A

        #momento de inercia
        Ix = 0
        for i in range(img_altura):
            for j in range(img_largura):
                if matriz[i][j] > 0:
                    d = (linha_fim-i+1)*h - h/2 - Y_linha
                    Ix += b*h**3/12 + b*h*d**2

        Iy = 0
        for i in range(img_altura):
            for j in range(img_largura):
                if matriz[i][j] > 0:
                    d = (linha_fim-i+1)*b - b/2 - X_linha
                    Iy += h*b**3/12 + h*b*d**2


        #visualização da imagem
        posicao_linha = (h*linha_fim + h/2 - Y_linha) / h

        # --- PRINT DOS RESULTADOS ---

        print(f"A: {soma_A:.4f}")
        print(f"Iy: {Iy:.4f}")
        print(f"Ix: {Ix:.4f}")
        print(f"yc, inf: {Y_linha:.4f}")
        print(f"yc, sup: {(D-Y_linha):.4f}")
        print(f"Wc, inf: {(Ix/Y_linha):.4f}")
        print(f"Wc, sup: {(Ix/(D-Y_linha)):.4f}")
        print(f"Kc, inf: {((Ix/Y_linha)/soma_A):.4f}")
        print(f"Kc, sup: {((Ix/(D-Y_linha))/soma_A):.4f}")
        print()
        print()
    

calc = Calculador()


print(f"====== 01 i ======")
img1 = dxf_para_tiff("dxf/01_i.dxf", res=0.1, output_tif="tif/01_i.tif")
calc.processa(img1, D=2100)
print(f"====== 01 t ======")
img2 = dxf_para_tiff("dxf/01_t.dxf", res=0.1, output_tif="tif/01_t.tif")
calc.processa(img2, D=2100)
print(f"====== 02 i ======")
img3 = dxf_para_tiff("dxf/02_i.dxf", res=0.1, output_tif="tif/02_i.tif")
calc.processa(img3, D=2300)
print(f"====== 02 t ======")
img4 = dxf_para_tiff("dxf/02_t.dxf", res=0.1, output_tif="tif/02_t.tif")
calc.processa(img4, D=2300)
print(f"====== 03 i ======")
img5 = dxf_para_tiff("dxf/03_i.dxf", res=0.1, output_tif="tif/03_i.tif")
calc.processa(img5, D=2300)
print(f"====== 03 t ======")
img6 = dxf_para_tiff("dxf/03_t.dxf", res=0.1, output_tif="tif/03_t.tif")
calc.processa(img6, D=2300)