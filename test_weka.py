from utils.weka_manager import start_weka

from weka.classifiers import Classifier

start_weka()

print("✅ JVM Started")

cls = Classifier(classname="weka.classifiers.trees.J48")

print("✅ J48 Loaded Successfully")