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


class Tag(object):
    '''
    Timeline tag object.

    :param data: Data attached to the tag

    :param position: Position on the timeline this tag would be found at.
    :type position: float
    '''
    def __init__(self, data, position):
        self.data = data
        self.position = position


class Timeline(object):
    '''
    Timeline class is responsible for controlling all the visible objects

    :param event_dispatcher: The event dispatcher for catching/responding and sending events to the rest of the system
    :type event_dispatcher: EventDispatcher
    '''
    tracks = []
    starts = []
    ends = []
    visible_tracks = []
    tags = {}
    insert_pos = 0
    turn_number = 1
    ed = None

    start_idx = 0
    end_idx = 0

    def __init__(self, event_dispatcher):
        self.ed = event_dispatcher

    def determine_visible(self, time):
        pass

    def add(self, obj, start_time=None):
        '''
        This method adds an object to the timeline to display.

        :param obj: The object to be controlled by the timeline
        :type obj: TrackObject

        :param start_time: The timeline time slot that this object's life begins at.  Defaults to adding right after the last animation has completed.
        :type start_time: float
        '''
        assert issubclass(obj.__class__, TrackObject)
        self.tracks += [obj]

    def add_turn(self):
        '''
        Inserts a turn tag to the timeline, automatically using the last position and incrementing the turn number.
        '''
        self.insert_tag('turn', self.turn_number)
        self.turn_number += 1

    def insert_tag(self, tag_name, data=None, position=None):
        '''
        Inserts a tag on the timeline.  The tags are all organized by name.

        :param tag_name: The name of the tag
        :type tag_name: string

        :param data: Data to attach to the tag.  This can be any data that makes sense with the tag.  For example a 'turn' tag should probably have the turn number encoded with it.

        :param position: Timeline time slot of where the tag is inserted.  Defaults to right after the last animation has completed.
        :type position: float
        '''
        if not position:
            position = self.insert_pos

        if tag_name not in self.tags:
            self.tags[tag_name] = []

        insert_at_end = True

        try:
            if position < self.tags[tag_name][-1].position:
                insert_at_end = False
        except IndexError:
            pass

        self.tags[tag_name] += [Tag(data, position)]

        # Only sorts if we've inserted a tag out of order!
        if not insert_at_end:
            self.tags[tag_name].sort(key=lambda x: x.position)

