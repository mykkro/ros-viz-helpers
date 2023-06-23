import yaml
import sys
from topicshow import showtopic
from fieldextract import fieldextract
from computer import compute

class HelperLaunch():
    
    def __init__(self):
        self.config_path = "config/config.yaml"
        
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


a = HelperLaunch()
a.run()


