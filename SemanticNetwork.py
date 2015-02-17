class Frame:
    def __init__(self,frameName):
        self.name = frameName
        self.nodes = []
        self.transformations = {}

    def getName(self):
        return self.name

class Node:
    def __init__(self,objectName):
        self.name = objectName
        self.attributes = []
        self.relationships = []

    def getName(self):
        return self.name




