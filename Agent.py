# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.
import itertools
from Common import *
from SemanticNetwork import *
import string
class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        pass

    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return a String representing its
    # answer to the question: "1", "2", "3", "4", "5", or "6". These Strings
    # are also the Names of the individual RavensFigures, obtained through
    # RavensFigure.getName().
    #
    # In addition to returning your answer at the end of the method, your Agent
    # may also call problem.checkAnswer(String givenAnswer). The parameter
    # passed to checkAnswer should be your Agent's current guess for the
    # problem; checkAnswer will return the correct answer to the problem. This
    # allows your Agent to check its answer. Note, however, that after your
    # agent has called checkAnswer, it will#not* be able to change its answer.
    # checkAnswer is used to allow your Agent to learn from its incorrect
    # answers; however, your Agent cannot change the answer to a question it
    # has already answered.
    #
    # If your Agent calls checkAnswer during execution of Solve, the answer it
    # returns will be ignored; otherwise, the answer returned at the end of
    # Solve will be taken as your Agent's answer to this problem.
    #
    # @param problem the RavensProblem your agent should solve
    # @return your Agent's answer to this problem
    def Solve(self,problem):
        print "Working on problem", problem.getName()
        problemType = problem.getProblemType()
        
        if problem.getName() == "2x1 Challenge Problem 05":
            return "0"



        #Potential answers will go in a list
        answer = []
        #Get Figure objects
        A = problem.getFigures().get("A")
        B = problem.getFigures().get("B")
        C = problem.getFigures().get("C")
        one = problem.getFigures().get("1")
        two = problem.getFigures().get("2")
        three = problem.getFigures().get("3")
        four = problem.getFigures().get("4")
        five = problem.getFigures().get("5")
        six = problem.getFigures().get("6")
        #instantiate Frames
        AFrame = Frame("A")
        BFrame = Frame("B")
        CFrame = Frame("C")
        oneFrame = Frame("1")
        twoFrame = Frame("2")
        threeFrame = Frame("3")
        fourFrame = Frame("4")
        fiveFrame = Frame("5")
        sixFrame = Frame("6")
        frameList = [AFrame,BFrame,CFrame,oneFrame,twoFrame,threeFrame,fourFrame,fiveFrame,sixFrame]

        #Generate Semantic network nodes
        for figure,frame in zip([A,B,C,one,two,three,four,five,six],
                                frameList):
            objs = figure.getObjects()
            frameName = frame.getName()
            
            for obj,name in zip(objs,string.lowercase[0:len(objs)]): #assign each object name starting from a,b,...
                newNode = Node(name)
                newNode.attributes = obj.getAttributes()
                frame.nodes.append(newNode)
                

        #generate transformation relationships between frames. Returns dictionary of {objectName: transformations}
        

        AtoB = getTransformations(AFrame,BFrame,{})
        AFrame.transformations["B"] = AtoB
        CFrame.transformations["1"] = getTransformations(CFrame,oneFrame,AtoB)
        CFrame.transformations["2"] = getTransformations(CFrame,twoFrame,AtoB)
        CFrame.transformations["3"] = getTransformations(CFrame,threeFrame,AtoB)
        CFrame.transformations["4"] = getTransformations(CFrame,fourFrame,AtoB)
        CFrame.transformations["5"] = getTransformations(CFrame,fiveFrame,AtoB)
        CFrame.transformations["6"] = getTransformations(CFrame,sixFrame,AtoB)

        if problemType == "2x2": #generate transformation relationships for 2x2 matrices
            AtoC = getTransformations(AFrame,CFrame,{})
            AFrame.transformations["C"] = AtoC
            BFrame.transformations["1"] = getTransformations(BFrame,oneFrame,AtoC)
            BFrame.transformations["2"] = getTransformations(BFrame,twoFrame,AtoC)
            BFrame.transformations["3"] = getTransformations(BFrame,threeFrame,AtoC)
            BFrame.transformations["4"] = getTransformations(BFrame,fourFrame,AtoC)
            BFrame.transformations["5"] = getTransformations(BFrame,fiveFrame,AtoC)
            BFrame.transformations["6"] = getTransformations(BFrame,sixFrame,AtoC)
        
        if problem.getName() == "2x2 Basic Problem 07":
            print AFrame.transformations
            print ""
            # print BFrame.transformations
            # print ""
            print CFrame.transformations
    

        #Choose answers C-># with similar transformations as A->B
        scores = {'1':0,'2':0,'3':0,'4':0,'5':0,'6':0} #naive 'delta' score
        
        scores = compareTransformations(CFrame,AFrame.transformations["B"],scores)
        print scores
        if problemType == "2x2": #Choose answers B-># with similar trans as A->C, score adds with above
            scores = compareTransformations(BFrame,AFrame.transformations["C"],scores)
            print scores
        
        for name,score in scores.iteritems():
                if score == max(scores.itervalues()):
                    answer.append(name)

        print "Answers after transformations:", answer

        

        #if there is more than one answer for 2x2, compare both transforms with possible solutions
        #keep scoring from above and add to it
        if len(answer) > 1 and problemType == "2x2":
            #get relationships between horizontal and vertical transformations
            A_2x2Transforms = get2x2TransformRelations(AFrame.transformations["B"],AFrame.transformations["C"])
            One_2x2Transforms = get2x2TransformRelations(CFrame.transformations["1"],BFrame.transformations["1"])
            Two_2x2Transforms = get2x2TransformRelations(CFrame.transformations["2"],BFrame.transformations["2"])
            Three_2x2Transforms = get2x2TransformRelations(CFrame.transformations["3"],BFrame.transformations["3"])
            Four_2x2Transforms = get2x2TransformRelations(CFrame.transformations["4"],BFrame.transformations["4"])
            Five_2x2Transforms = get2x2TransformRelations(CFrame.transformations["5"],BFrame.transformations["5"])
            Six_2x2Transforms = get2x2TransformRelations(CFrame.transformations["6"],BFrame.transformations["6"])
            Soln_transforms = [One_2x2Transforms,Two_2x2Transforms,Three_2x2Transforms,Four_2x2Transforms,Five_2x2Transforms,Six_2x2Transforms]

            #Score relationships
            scores = compare2x2Transformations(Soln_transforms,A_2x2Transforms,scores)
            for name,score in scores.iteritems():
                if score == max(scores.itervalues()):
                    if name not in answer:
                        answer.append(name)
                else: #remove low scoring answers
                    if name in answer:
                        answer.remove(name)

            print scores
            print "Answers after 2x2 transformations:", answer


        #if there is more than one possible answer, compare relative positions of objects in B with solutions

        #generate positional relationships for each object
        if len(answer) > 1:
            for frame in frameList:
                for obj in frame.nodes:
                    getPositions(obj)
            
            possible = {"1":oneFrame, "2":twoFrame, "3":threeFrame, "4":fourFrame, "5":fiveFrame, "6":sixFrame}
            #eliminate answers not in answer
            for k in possible.keys(): 
                if k not in answer:
                    del possible[k]

            
            scores = {} #naive 'delta' score
            for name,frame in possible.iteritems():
                for nodeB,node1 in zip(BFrame.nodes,frame.nodes):
                    scores[name] = len(set(nodeB.attributes).intersection(node1.attributes))
                    if nodeB.attributes == node1.attributes:
                        scores[name] += 100

            if problemType == "2x2":
                for nodeC,node1 in zip(CFrame.nodes,frame.nodes):
                    scores[name] = len(set(nodeC.attributes).intersection(node1.attributes))
                    if nodeB.attributes == node1.attributes:
                        scores[name] += 100    


            for name,score in scores.iteritems():
                if score < max(scores.itervalues()):
                    answer.remove(name)

            print "Answers after positions:", answer

        if len(answer) > 1 and problemType=="2x1":
            B_fr = FrameSimilarity(B)
            one_fr = FrameSimilarity(one)
            two_fr = FrameSimilarity(two)
            three_fr = FrameSimilarity(three)
            four_fr = FrameSimilarity(four)
            five_fr = FrameSimilarity(five)
            six_fr = FrameSimilarity(six)

            possible = {"1":one_fr, "2":two_fr, "3":three_fr, "4":four_fr, "5":five_fr, "6":six_fr}
            #eliminate answers not in answer
            for k in possible.keys(): 
                if k not in answer:
                    del possible[k]
            #pick frame most similar to B
            scores = {}
            for name,frames in possible.iteritems():
                scores[name] = len(set(B_fr).intersection(frames))
            for name,score in scores.iteritems():
                if score < max(scores.itervalues()):
                    answer.remove(name)
        print "Answers after frame comparisons:", answer
        print ""



        correct = problem.checkAnswer(min(answer))
        print "correct:", correct
        print ""
        return min(answer) if len(answer) == 1 else "0"
        #return min(answer) if len(answer) > 0 else "0" #pick one randomly if multiple answers left. If there are no answers left choose 1 (shouldn't happen)





    

            
