# -- coding: utf-8 --
import sys
sys.path.append("C:\\Program Files (x86)\\Aldebaran Robotics\\Choreographe Suite 2.1\\lib")

from naoqi import ALProxy

def main():
    nao_ip = "127.0.0.1"
    nao_port = 51032

    behavior_name = sys.argv[1] if len(sys.argv) > 1 else None

    if not behavior_name:
        print("No se proporcionó el nombre del comportamiento.")
        return

    try:
        behavior = ALProxy("ALBehaviorManager", nao_ip, nao_port)

        if behavior.isBehaviorInstalled(behavior_name):
            print("Ejecutando comportamiento:", behavior_name)
            behavior.runBehavior(behavior_name)
        else:
            print("No existe el comportamiento/Gesto:", behavior_name)
    except Exception as e:
        print("Error:", e)

    print("Fin de la ejecucion")

if __name__ == "__main__":
    main()