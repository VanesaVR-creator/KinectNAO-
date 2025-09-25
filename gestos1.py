import os
import time
import subprocess
from pykinect2 import PyKinectV2, PyKinectRuntime

py27_EXE   = r"C:\Python27\python.exe"             
NAO = r"C:\Users\Equipo 3\Desktop\KinectNao2.7\main.py"       

kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Body)

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

print("Esperando datos del Kinect... (Ctrl + C para salir)")
gesto_anterior = None  

try:
    while True:
        if not kinect.has_new_body_frame():
            time.sleep(0.05)
            continue

        bodies = kinect.get_last_body_frame()
        if bodies is None:
            continue

        limpiar_pantalla()
        for idx, body in enumerate(bodies.bodies, start=1):
            if not body.is_tracked:
                continue

            joints = body.joints
            cabeza            = joints[PyKinectV2.JointType_Head]
            centro_hombros    = joints[PyKinectV2.JointType_SpineShoulder]
            hombro_der        = joints[PyKinectV2.JointType_ShoulderRight]
            hombro_izq        = joints[PyKinectV2.JointType_ShoulderLeft]
            codo_der          = joints[PyKinectV2.JointType_ElbowRight]
            codo_izq          = joints[PyKinectV2.JointType_ElbowLeft]
            mano_der          = joints[PyKinectV2.JointType_HandRight]
            mano_izq          = joints[PyKinectV2.JointType_HandLeft]
            cadera            = joints[PyKinectV2.JointType_SpineBase]
            rodilla_izq       = joints[PyKinectV2.JointType_KneeLeft]
            pie_der           = joints[PyKinectV2.JointType_FootRight]
            pie_izq           = joints[PyKinectV2.JointType_FootLeft]

            print(f"Cuerpo {idx}:")
            print(f"  Cabeza:  x={cabeza.Position.x:.2f},  y={cabeza.Position.y:.2f},  z={cabeza.Position.z:.2f}")
            print(f"  Hombro D: x={hombro_der.Position.x:.2f}, y={hombro_der.Position.y:.2f}, z={hombro_der.Position.z:.2f}")
            print(f"  Hombro I: x={hombro_izq.Position.x:.2f}, y={hombro_izq.Position.y:.2f}, z={hombro_izq.Position.z:.2f}")
            print("-" * 60)

            gesto_actual = None

            # Despertar: 
            if (mano_izq.Position.y > cabeza.Position.y and mano_der.Position.y > cabeza.Position.y):
                gesto_actual = "despertar"

            # Descansar:
            elif (mano_der.Position.x < centro_hombros.Position.x and mano_izq.Position.x > centro_hombros.Position.x):
                gesto_actual = "descansar"

            # Saludo: 
            elif mano_der.Position.y > cabeza.Position.y:
                gesto_actual = "saludo"

            # Limpiar frente: 
            elif (centro_hombros.Position.y < mano_der.Position.y < cabeza.Position.y):
                gesto_actual = "limpiar_frente"

            # Sentarse:
            elif cadera.Position.y < rodilla_izq.Position.y:
                gesto_actual = "sentarse"

            # Levantarse: 
            elif mano_izq.Position.y > cabeza.Position.y:
                gesto_actual = "levantarse"

            # Avanzar / Retroceder / Izq / Der
            elif pie_der.Position.z > cadera.Position.z + 0.05 > pie_izq.Position.z:
                gesto_actual = "avanzar"
            elif pie_izq.Position.z > cadera.Position.z + 0.05 > pie_der.Position.z:
                gesto_actual = "retroceder"
            elif mano_der.Position.z > centro_hombros.Position.z + 0.10 and mano_izq.Position.z < centro_hombros.Position.z + 0.10:
                gesto_actual = "izquierda"
            elif mano_izq.Position.z > centro_hombros.Position.z + 0.10 and mano_der.Position.z < centro_hombros.Position.z + 0.10:
                gesto_actual = "derecha"

            
            if gesto_actual and gesto_actual != gesto_anterior:
                print(f"Gesto detectado: {gesto_actual} → ejecutando Python 2.7")
                subprocess.run([py27_EXE, NAO, gesto_actual])
                gesto_anterior = gesto_actual

        time.sleep(0.30) 

except KeyboardInterrupt:
    print("\nFin del programa.")