import itertools

def getTransformations(AFrame,BFrame,matchWith):
        #generates a dictionary of lists of relations between each object A->B
        #examines each possible mapping of objects from A->B and picks best mapping based on weight
        #renames Nodes in BFrame to reflect new mapping
        A_Objs = AFrame.nodes
        B_Objs = BFrame.nodes
        
        A_names = [A_Obj.getName() for A_Obj in A_Objs]
        B_names = [B_Obj.getName() for B_Obj in B_Objs]
        
        while len(A_names) != len(B_names):
            if len(A_names) > len(B_names):
                B_names.append(None)
            if len(B_names) > len(A_names):
                A_names.append(None)
        B_permutations = list(itertools.permutations(B_names))

        bestweight = 0
        bestTransforms = {}
        bestMapping = []
        for B_names in B_permutations:
            weight = 0
            transforms = {}
            
            for A_name,B_name in zip(A_names,B_names):
                
                for obj in A_Objs:
                    if obj.getName() == A_name:
                        A_Obj = obj
                for obj in B_Objs:
                    if obj.getName() == B_name:
                        B_Obj = obj
                if not A_name:
                    #obj was added to b
                    transforms[B_name] = []
                    transforms[B_name].append("added")
                elif not B_name:
                    #obj was deleted from a
                    transforms[A_name] = []
                    transforms[A_name].append("deleted")
                else:
                    transforms[B_name] = []
                    A_atts = {}
                    B_atts = {}
                    for A_att,B_att in zip(A_Obj.attributes,B_Obj.attributes):
                        A_atts[A_att.getName()] = A_att.getValue()
                        B_atts[B_att.getName()] = B_att.getValue()

                    #now for some attribute rules:
                    #shape
                    try:
                        if A_atts["shape"] == B_atts["shape"]:
                            transforms[B_name].append("shapeSame")
                            weight += 5
                        else:
                            transforms[B_name].append("shapeDiff")
                    except KeyError:
                        pass

                    #size
                    try:
                        if A_atts["size"] == B_atts["size"]:
                            transforms[B_name].append("sizeSame")
                            weight += 5
                        else:
                            transforms[B_name].append("sizeDiff")
                            weight += 2
                    except KeyError:
                        pass

                    #fill
                    try:
                        A_atts["fill"]
                    except KeyError:
                        A_atts["fill"] = "no"

                    try:
                        B_atts["fill"]
                    except KeyError:
                        B_atts["fill"] = "no"
                    
                    if A_atts["fill"] == B_atts["fill"]:
                        transforms[B_name].append("fillSame")
                        weight += 5
                    else:
                        transforms[B_name].append("fill:" + A_atts["fill"] + B_atts["fill"])
                        weight += 2
                    
                    #angle
                    try:
                        A_atts["angle"]
                    except KeyError:
                        A_atts["angle"] = 0
                    try:
                        B_atts["angle"]
                    except KeyError:
                        B_atts["angle"] = 0
                     
                    if A_atts["shape"] == "circle" and B_atts["shape"] == "circle": #ignore angle changes for circle
                        if matchWith:
                            for obj in matchWith.iterkeys():
                                if 'angleDiff' in matchWith[obj]:
                                    transforms[B_name].append('angleDiff')
                                    transforms[B_name].append([n for n in matchWith[obj] if type(n) == type(1)][0]) #copy angle value
                                    break
                                if 'angleSame' in matchWith[obj]:
                                    transforms[B_name].append('angleSame')
                                    break
                        elif A_atts["angle"] == B_atts["angle"]:
                            transforms[B_name].append("angleSame")
                            weight += 4
                        
                    elif A_atts["angle"] == B_atts["angle"]:
                        transforms[B_name].append("angleSame")
                        weight += 4
                    else:
                        transforms[B_name].append("angleDiff")
                        transforms[B_name].append(abs(int(A_atts["angle"]) - int(B_atts["angle"])))
                        weight +=3

                    #vertical-flip
                    try:
                        A_atts["vertical-flip"]
                    except KeyError:
                        A_atts["vertical-flip"] = "no"
                    try:
                        B_atts["vertical-flip"]
                    except KeyError:
                        B_atts["vertical-flip"] = "no"

                    if A_atts["vertical-flip"] == B_atts["vertical-flip"]:
                        transforms[B_name].append("vertflipSame")
                        
                    else:
                        transforms[B_name].append("vertflipDiff")

            if transforms == matchWith:
                weight += 100
            if weight > bestweight:
                bestTransforms = transforms
                bestweight = weight
                bestMapping = B_names
        
        for obj,newname in zip(BFrame.nodes,B_names):
              obj.name = newname 
        
        return bestTransforms

def getPositions(obj):
        #get relationships between objects
        for att in obj.attributes: 
                try:
                    if att.getName() == "inside":
                        obj.relationships.append("inside")
                except KeyError:
                    pass

                try:
                    if att.getName() == "above":
                        obj.relationships.append("above")
                except KeyError:
                    pass

                try:
                    if att.getName() == "left-of":
                        obj.relationships.append("left-of")
                except KeyError:
                    pass
                try:
                    if att.getName() == "overlaps":
                        obj.relationships.append("overlaps")
                except KeyError:
                    pass
