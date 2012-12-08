'''
The timeline is responsible for telling what to draw, when and under what state. This is the backbone of the visualizer and will be responsible for presenting information in the most accurate way possible given the desired playback format.
'''
from __future__ import print_function
#from eventdispatcher import event_handler


class TrackObject(object):
    '''
    The TrackObject is the base class for anything that wants to be renderered on the Timeline.

    This contains metadata concerning the life and death of an object for retained-mode rendering.
    '''
    life = 0
    death = float('Inf')

    def __init__(self):
        pass


class Timeline(object):
    '''
    Timeline class is responsible for controlling all the visible objects
    '''
    tracks = []
    starts = []
    ends = []

    def __init__(self, event_dispatcher):
        self.ed = event_dispatcher

    def add(self, obj, start_turn=None):
        assert issubclass(obj.__class__, TrackObject)
        self.tracks += [obj]


