#! /usr/bin/env python
# -*- coding:utf-8 -*-

from lxml import etree


class OpenStreetMap :
    
    def __init__ (self) :
        self.bounds = None
        self.nodes = []
        self.ways = []
        self.relations = []

    def fromXML (self, xml) :
        root = etree.fromstring(xml)
        self.bounds = OSMUtils.domToBounds(root)
        self.nodes = OSMUtils.domToNodes(root)
        self.ways = OSMUtils.domToWays(root)
        self.relations = OSMUtils.domToRelations(root)


class OSMUtils :
    
    @staticmethod
    def domToBounds (root) :
        bounds_dom = root.xpath('/osm/bounds')[0]
        a = bounds_dom.attrib
        return OSMBounds(
            OSMLocation(float(a['minlat']), float(a['minlon'])),
            OSMLocation(float(a['maxlat']), float(a['maxlon']))
        )

    @staticmethod
    def domToNodes (root) :
        nodes = []
        for node_dom in root.xpath('/osm/node') :
            node = OSMNode()
            node.fromXMLNode(node_dom)
            nodes.append(node)
        return nodes

    @staticmethod
    def domToWays (root) :
        ways = []
        for way_dom in root.xpath('/osm/way') :
            way = OSMWay()
            way.fromXMLNode(way_dom)
            ways.append(way)
        return ways

    @staticmethod
    def domToRelations (dom) :
        relations = []
        for relation_dom in dom.xpath('./relation') :
            relation = OSMRelation()
            relation.fromXMLNode(relation_dom)
            relations.append(relation)
        return relations

    @staticmethod
    def domToMembers (dom) :
        members = []
        for member_dom in dom.xpath('./member') :
            member = OSMMember()
            member.fromXMLNode(member_dom)
            members.append(member)
        return members

    @staticmethod
    def domToTags (dom) :
        tags = {}
        for tag_dom in dom.xpath('./tag') :
            key = tag_dom.attrib.get('k', '')
            value = tag_dom.attrib.get('v', '')
            if key != '' and value != '' :
                tags[key] = value
        return tags

    @staticmethod
    def domToNds (dom) :
        return [nd.attrib['ref'] for nd in dom.xpath('./nd') if nd.attrib.has_key('ref')]


class OSMBounds :
    
    def __init__ (self, min_location, max_location) :
        if min_location.lat > max_location.lat or min_location.lon > max_location.lon :
            self.min_location = None
            self.max_location = None
        else :
            self.min_location = min_location
            self.max_location = max_location

    def __str__ (self) :
        return 'OSMBounds(min={0}, max={1})'.format(self.min_location, self.max_location)
        

class OSMLocation :
    
    def __init__ (self, lat, lon) :
        self.lat = lat
        self.lon = lon

    def __str__ (self) :
        return 'OSMLocation(lat={0}, lon={0})'.format(self.lat, self.lon)


class OSMNode :
    
    def __init__ (self) :
        self.id = 0
        self.visible = False
        self.version = 0
        self.changeset = 0
        self.timestamp = '1970-01-01T00:00:00Z' # datetime.min
        self.user = ''
        self.uid = 0
        self.lat = 0
        self.lon = 0
        self.tags = {}

    def fromXMLNode (self, node) :
        a = node.attrib
        self.id = long(a.get('id', '0'))
        self.visible = bool(a.get('visible', 'False'))
        self.version = float(a.get('version', '0'))
        self.changeset = long(a.get('changeset', '0'))
        self.timestamp = a.get('timestamp', '1970-01-01T00:00:00Z')
        self.user = a.get('user', '')
        self.uid = long(a.get('uid', '0'))
        self.lat = float(a.get('lat', '0'))
        self.lon = float(a.get('lon', '0'))
        self.tags = OSMUtils.domToTags(node)

    def __str__ (self) :
        return 'OSMNode(lat={0}, lon={1}, visible={2})'.format(self.lat, self.lon, self.visible)


class OSMWay :
    
    def __init__ (self) :
        self.id = 0
        self.visible = False
        self.version = 0
        self.changeset = 0
        self.timestamp = '1970-01-01T00:00:00Z' # datetime.min
        self.user = ''
        self.uid = 0
        self.tags = {}
        self.nds = {}

    def fromXMLNode (self, node) :
        a = node.attrib
        self.id = long(a.get('id', '0'))
        self.visible = bool(a.get('visible', 'False'))
        self.version = float(a.get('version', '0'))
        self.changeset = long(a.get('changeset', '0'))
        self.timestamp = a.get('timestamp', '1970-01-01T00:00:00Z')
        self.user = a.get('user', '')
        self.uid = long(a.get('uid', '0'))
        self.tags = OSMUtils.domToTags(node)
        self.nds = OSMUtils.domToNds(node)
        # TODO : implements bounding box

    def __str__ (self) :
        return 'OSMWay(id={0}, len(nds)={1})'.format(self.id, len(self.nds))


class OSMRelation :
    
    def __init__ (self) :
        self.id = 0
        self.visible = False
        self.version = 0
        self.changeset = 0
        self.timestamp = '1970-01-01T00:00:00Z' # datetime.min
        self.user = ''
        self.uid = 0
        self.members = []
        self.tags = {}

    def fromXMLNode (self, node) :
        a = node.attrib
        self.id = long(a.get('id', '0'))
        self.visible = bool(a.get('visible', 'False'))
        self.version = float(a.get('version', '0'))
        self.changeset = long(a.get('changeset', '0'))
        self.timestamp = a.get('timestamp', '1970-01-01T00:00:00Z')
        self.user = a.get('user', '')
        self.uid = long(a.get('uid', '0'))
        self.members = OSMUtils.domToMembers(node)
        self.tags = OSMUtils.domToTags(node)

    def __str__ (self) :
        return 'OSMRelation(id={0}, len(members)={1})'.format(self.id, len(self.members))


class OSMMember :
    
    def __init__ (self) :
        self.type = ''
        self.ref = -1
        self.role = ''

    def fromXMLNode (self, node) :
        a = node.attrib
        self.type = a.get('type', '')
        self.ref = long(a.get('ref', '-1'))
        self.role = a.get('role', '')

    def __str__ (self) :
        return 'OSMMember(type={0}, ref={1}, role={2})'.format(self.type, self.ref, self.role)


if __name__ == '__main__' :
    
    # read xml
    with open('../data/map.osm.xml') as f :
        xml = f.read()

    osm = OpenStreetMap()
    osm.fromXML(xml)

