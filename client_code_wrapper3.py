import sys, traceback, os
from datetime import datetime


def codeWrapper():
    clientpath='/workspace'
    sys.path.append(clientpath)

    #file_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(clientpath)
    # file_path = os.path.join(file_path, "output" + datetime.utcnow().strftime('_%Y%m%d_%Hh%Mm%Ss_UTC') + ".log")
    old_stdout = sys.stdout
    log_file = open("output" + datetime.utcnow().strftime('_%Y%m%d_%Hh%Mm%Ss_UTC') + ".log", "w")
    sys.stdout = log_file

    try:
        # CHANGE THE IMPORT STATEMENT TO MATCH YOUR MAIN CODE
        import __clientfile__
    except Exception:
        print("Exception in user code:")
        print("-"*60)
        traceback.print_exc(file=sys.stdout)
        print("-"*60)



    sys.stdout = old_stdout
    log_file.close()

if __name__ == "__main__":
    codeWrapper()





