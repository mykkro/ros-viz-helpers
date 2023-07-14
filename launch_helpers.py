import yaml
import sys
from core_programs.topicshow import showtopic
from core_programs.fieldextract import fieldextract
from core_programs.computer import compute
from core_programs.timeseries import timeseriesplot
from core_programs.trajvizualizer import visualizetrajectory

class HelperLaunch():
    
    def __init__(self):
        self.config_path = "config/configros1.yaml"
        
        try:
            with open(self.config_path, "r", encoding="utf-8") as infile:
                self.config = yaml.safe_load(infile)
        except Exception as err:
            print(err)
            sys.exit(0)



    def run(self):
        for task in self.config["tasks"]:
            task_name = task["name"]
            task_inputs = task["inputs"]
            self.run_task(task_name, task_inputs, task)

    def run_task(self, task_name, task_inputs, task):
        
        if task_name == "rosbag_topicshow":
            showtopic(task_inputs["input"], 
                      task_inputs["msgpath"])
        
        if task_name == "field_extract":
            fieldextract(task_inputs["input"], 
                         task_inputs["output"], 
                         task_inputs["topic"],
                         task_inputs["field"],
                         task_inputs["msgpath"]
                         )
        
        if task_name == "compute_light":
            compute(task_inputs["input"],
                    task_inputs["output"],
                    task_inputs["urdf"])
        
        if task_name == "display_timeseries":
            timeseriesplot(task_inputs["input"],
                           task_inputs["output"],
                           task_inputs["field"],
                           task_inputs["fromframe"],
                           task_inputs["toframe"],
                           task_inputs["plot"]
                           )
        
        if task_name == "trajviz":
            visualizetrajectory(task_inputs["input"],
                                task_inputs["urdf"],
                                task_inputs["speed"],
                                task_inputs["repeat"],
                                task_inputs["timecol"],
                                task_inputs["poscol"],
                                )

a = HelperLaunch()
a.run()


