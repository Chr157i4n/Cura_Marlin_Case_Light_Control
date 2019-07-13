# Cura PostProcessingPlugin
# Author:   Christian Köhlke
# Date:     July 13, 2019

# Description:  postprocessing-script to activate the LED on a GT2560 V3.0 Board with Marlin
#
#
# G-Code Command:
#
# M42 P6 S255
#
# M42 to change a hardware pins state
# P6 is the hardware pin of the LED connector
# Change Sxxx to vary duty cycle.
 
from ..Script import Script
from UM.Application import Application

class LED(Script):
    def __init__(self):
        super().__init__()

    def getSettingDataString(self):
        return """{
            "name": "LED",
            "key": "LED",
            "metadata": {},
            "version": 2,
            "settings":
            {
                "Layer":
                {
                    "label": "Layer",
                    "description": "On which Layer this script should change the LEDs",
                    "type": "int",
                    "default_value": 0,
                    "minimum_value": 0
                },
                "LastLayer":
                {
                    "label": "Last Layer",
                    "description": "this will change the LEDs on the last Layer. This will ignore the Layer setting",
                    "type": "bool",
                    "default_value": false
                },
                "Brightness":
                {
                    "label": "Brightness",
                    "description": "Brightness of the LEDs. 0 to turn off the LEDs",
                    "type": "float",
                    "default_value": 100,
                    "minimum_value": 0,
                    "maximum_value": 100
                }
                
                
            }
        }"""

    def execute(self, data):
        
        LED_Layer = self.getSettingValueByKey("Layer")
        LED_LastLayer = self.getSettingValueByKey("LastLayer")
        LED_Brightness = self.getSettingValueByKey("Brightness")
        last_Layer=-1
        for layer in data:
            layer_index = data.index(layer)
            lines = layer.split("\n")
            for line in lines:
                if line.startswith(";LAYER:"):
                    last_Layer=last_Layer+1
        
        layer_indexI=-1
        for layer in data:
            layer_index = data.index(layer)
            lines = layer.split("\n")
            for line in lines:
                if line.startswith(";LAYER:"):
                    layer_indexI=layer_indexI+1
                    line_index = lines.index(line)
                    if (layer_indexI==LED_Layer and LED_LastLayer==False):
                        lines.insert(line_index + 1, "M42 P6 S"+str(LED_Brightness))                   
                    if (layer_indexI==last_Layer and LED_LastLayer==True):
                        lines.insert(line_index + 1, "M42 P6 S"+str(LED_Brightness))                          
            result = "\n".join(lines)
            data[layer_index] = result
        return data
