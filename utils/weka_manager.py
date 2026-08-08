import os
import jpype
import weka.core.jvm as jvm

_started = False

JVM_PATH = r"C:\Program Files\Eclipse Adoptium\jdk-21.0.12.8-hotspot\bin\server\jvm.dll"

def start_weka():
    global _started

    if _started:
        return

    if not jpype.isJVMStarted():
        jpype.startJVM(
            JVM_PATH,
            convertStrings=True
        )

    jvm.started = True

    _started = True


def stop_weka():
    global _started

    if jpype.isJVMStarted():
        jpype.shutdownJVM()

    _started = False