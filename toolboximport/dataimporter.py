import pandas as pd
import os
from pathlib import Path

BASEDIR = Path(__file__).resolve().parent.parent
IMPORTDIR = BASEDIR / 'import'

class Import:
    def __init__(self, filename="", import_dir=IMPORTDIR, sheet=0) -> None:
        '''
        arguments:
        -----
            filename: str nombre del archivo XLSX. 
            import_dir: Path object. Si el archivo a importar no se encuentra en 'import'
                        default: BASEDIR / 'import'
        '''
        if os.path.exists(os.path.join(import_dir, filename)):
            self.file = os.path.join(import_dir, filename)
        else:
            raise FileNotFoundError(f"No se pudo encontrar el archivo {filename}")
        
        self.sheet = sheet
    
    def readfile(self):
        df = pd.read_excel(self.file, sheet_name=self.sheet)
        print(df.head)
        print(df.iloc[:, 2].unique())
        
        
if __name__ == '__main__':
    filename = 'Catalogación Archivo Parroquial de Aucará.xlsx'
    test = Import(filename=filename, sheet=2)
    test.readfile()