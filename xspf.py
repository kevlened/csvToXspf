## License
##-------
##Copyright 2011 Alastair Porter. All rights reserved.
##
##Redistribution and use in source and binary forms, with or without modification, are
##permitted provided that the following conditions are met:
##
##   1. Redistributions of source code must retain the above copyright notice, this list of
##      conditions and the following disclaimer.
##
##   2. Redistributions in binary form must reproduce the above copyright notice, this list
##      of conditions and the following disclaimer in the documentation and/or other materials
##      provided with the distribution.
##
##THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS ``AS IS'' AND ANY EXPRESS OR IMPLIED
##WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
##FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
##CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
##CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
##SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
##ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
##NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
##ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

#!/usr/bin/python

import xml.etree.ElementTree as ET

class XspfBase(object):
    NS = "http://xspf.org/ns/0/"

    def _addAttributesToXml(self, parent, attrs):
        for attr in attrs:
            value = getattr(self, attr)
            if value:
                el = ET.SubElement(parent, "{{{0}}}{1}".format(self.NS, attr))
                el.text = value


class Xspf(XspfBase):
    def __init__(self, obj={}, **kwargs):
        self.version = "1"

        self._title = ""
        self._creator = ""
        self._info = ""
        self._annotation = ""
        self._location = ""
        self._identifier = ""
        self._image = ""
        self._date = ""
        self._license = ""

        self._trackList = []

        if len(obj):
            if "playlist" in obj:
                obj = obj["playlist"]
            for k, v in list(obj.items()):
                setattr(self, k, v)

        if len(kwargs):
            for k, v in list(kwargs.items()):
                setattr(self, k, v)

    @property
    def title(self):
        """A human-readable title for the playlist. Optional"""
        return self._title
    @title.setter
    def title(self, title):
        self._title = title

    @property
    def creator(self):
        """Human-readable name of the entity (author, authors, group, company, etc)
           that authored the playlist. Optional"""
        return self._creator
    @creator.setter
    def creator(self, creator):
        self._creator = creator

    @property
    def annotation(self):
        """A human-readable comment on the playlist. This is character data,
           not HTML, and it may not contain markup. Optional"""
        return self._annotation
    @annotation.setter
    def annotation(self, annotation):
        self._annotation = annotation

    @property
    def info(self):
        """URI of a web page to find out more about this playlist. Optional"""
        return self._info
    @info.setter
    def info(self, info):
        self._info = info

    @property
    def location(self):
        """Source URI for this playlist. Optional"""
        return self._location
    @location.setter
    def location(self, location):
        self._location = location

    @property
    def identifier(self):
        """Canonical ID for this playlist. Likely to be a hash or other
           location-independent name. Optional"""
        return self._identifier
    @identifier.setter
    def identifier(self, identifier):
        self._identifier = identifier

    @property
    def image(self):
        """URI of an image to display in the absence of a trackList/image
           element. Optional"""
        return self._image
    @image.setter
    def image(self, image):
        self._image = image

    @property
    def date(self):
        """Creation date (not last-modified date) of the playlist. Optional"""
        return self._date
    @date.setter
    def date(self, date):
        self._date = date

    @property
    def license(self):
        """URI of a resource that describes the license under which this
           playlist was released. Optional"""
        return self._license
    @license.setter
    def license(self, license):
        self._license = license

    # Todo: Attribution, Link, Meta, Extension

    @property
    def track(self):
        return self._trackList
    @track.setter
    def track(self, track):
        self.add_track(track)

    def add_track(self, track={}, **kwargs):
        if isinstance(track, list):
            map(self.add_track, track)
        elif isinstance(track, Track):
            self._trackList.append(track)
        elif isinstance(track, dict) and len(track) > 0:
            self._trackList.append(Track(track))
        elif len(kwargs) > 0:
            self._trackList.append(Track(kwargs))

    def add_tracks(self, tracks):
        map(self.add_track, tracks)

    def toXml(self, encoding="utf-8"):
        root = ET.Element("{{{0}}}playlist".format(self.NS))
        root.set("version", self.version)

        self._addAttributesToXml(root, ["title", "info", "creator", "annotation",
                                         "location", "identifier", "image", "date", "license"])

        if len(self._trackList):
            track_list = ET.SubElement(root, "{{{0}}}trackList".format(self.NS))
            for track in self._trackList:
                track_list = track.getXmlObject(track_list)
        return ET.tostring(root, encoding)

class Track(XspfBase):
    def __init__(self, obj={}, **kwargs):
        self._location = ""
        self._identifier = ""
        self._title = ""
        self._creator = ""
        self._annotation = ""
        self._info = ""
        self._image = ""
        self._album = ""
        self._trackNum = ""
        self._duration = ""

        if len(obj):
            for k, v in list(obj.items()):
                setattr(self, k, v)

        if len(kwargs):
            for k, v in list(kwargs.items()):
                setattr(self, k, v)

    @property
    def location(self):
        """URI of resource to be rendered. Probably an audio resource, but MAY be any type of
           resource with a well-known duration. Zero or more"""
        return self._location
    @location.setter
    def location(self, location):
        self._location = location

    @property
    def identifier(self):
        """ID for this resource. Likely to be a hash or other location-independent name,
           such as a MusicBrainz identifier.  MUST be a legal URI. Zero or more"""
        return self._identifier
    @identifier.setter
    def identifier(self, identifier):
        self._identifier = identifier

    @property
    def title(self):
        """Human-readable name of the track that authored the resource which defines the
           duration of track rendering. Optional"""
        return self._title
    @title.setter
    def title(self, title):
        self._title = title

    @property
    def creator(self):
        """Human-readable name of the entity (author, authors, group, company, etc) that authored
           the resource which defines the duration of track rendering."""
        return self._creator
    @creator.setter
    def creator(self, creator):
        self._creator = creator

    @property
    def annotation(self):
        """A human-readable comment on the track. This is character data, not HTML,
           and it may not contain markup."""
        return self._annotation
    @annotation.setter
    def annotation(self, annotation):
        self._annotation = annotation

    @property
    def info(self):
        """URI of a place where this resource can be bought or more info can be found. Optional"""
        return self._info
    @info.setter
    def info(self, info):
        self._info = info

    @property
    def image(self):
        """URI of an image to display for the duration of the track. Optional"""
        return self._image
    @image.setter
    def image(self, image):
        self._image = image

    @property
    def album(self):
        """Human-readable name of the collection from which the resource which defines
           the duration of track rendering comes. Optional"""
        return self._album
    @album.setter
    def album(self, album):
        self._album = album

    @property
    def trackNum(self):
        """Integer with value greater than zero giving the ordinal position of the media
           on the album. Optional"""
        return self._trackNum
    @trackNum.setter
    def trackNum(self, trackNum):
        self._trackNum = trackNum

    @property
    def duration(self):
        """The time to render a resource, in milliseconds. Optional"""
        return self._duration
    @duration.setter
    def duration(self, duration):
        self._duration = duration

    # Todo: Link, Meta, Extension

    def getXmlObject(self, parent):
        track = ET.SubElement(parent, "{{{0}}}track".format(self.NS))

        self._addAttributesToXml(track, ["location", "identifier", "title", "creator",
                                        "annotation", "info", "image", "album",
                                        "trackNum", "duration"])
        return parent

Spiff = Xspf
