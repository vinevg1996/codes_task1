#!/usr/bin/python
from discrete_source import DiscreteSource

import sys
import json
import random

discreteSource = DiscreteSource(sys.argv)

if (discreteSource.IsSourceWithMemory()):
    times = discreteSource.ProcessWithMemory()
else:
    times = discreteSource.ProcessWithoutMemory()

if (times != -1):
    event_list = discreteSource.GetEventList()
    if(len(event_list) > 0):
        print("event_list = ", event_list)
        print("\nsequence meets ", times, "times")
        probability = float(times) / float(discreteSource.GetN()) 
        print("probability = ", probability)
else:
    print("\nInfiniteProcess")