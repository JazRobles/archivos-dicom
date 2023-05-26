# Create your views here.
import os
import pydicom
from django.shortcuts import render
from django.http import HttpResponse

def extract_dicom_data(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dicom_folder = os.path.join(BASE_DIR, 'myapp', 'DICOM')
    structure_names = []
    doses = []

    for filename in os.listdir(dicom_folder):
        file_path = os.path.join(dicom_folder, filename)

        # Verificar que se está accediendo a los archivos DICOM correctos
        print("File Path:", file_path)

        if os.path.isfile(file_path) and filename.endswith(".dcm"):
            ds = pydicom.dcmread(file_path)

            # Verificar los nombres de los atributos y secuencias en los archivos DICOM
            print("DICOM Attributes:")
            print(ds)

            if "StructureSetROISequence" in ds:
                structure_name = ds.StructureSetROISequence[0].ROIName
                structure_names.append(structure_name)

            if "DoseGridSequence" in ds:
                dose = ds.DoseGridSequence[0].DoseGridScaling
                doses.append(dose)

    # Verificar los valores de structure_names y doses
    print("Structure Names:", structure_names)
    print("Doses:", doses)

    structure_doses = list(zip(structure_names, doses))

    context = {
        "structure_doses": structure_doses
    }
    return render(request, "myapp/dicom_data.html", context)
