from datetime import datetime

strung = "1790-10-24"

def edad_x_nacimiento(fecha_nacimiento, fecha_referencia):
        anio_nac = fecha_nacimiento.year
        anio_ref = fecha_referencia.year
        
        edad = max(anio_ref, anio_nac) - min(anio_ref, anio_nac)
        return edad
    
nac = datetime.strptime("1780-12-24", "%Y-%m-%d")
mat = datetime.strptime("1800-02-12", "%Y-%m-%d")

print(edad_x_nacimiento(nac,mat))