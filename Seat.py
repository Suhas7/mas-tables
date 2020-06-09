class Seat:
    def __init__(self,ID,x,y,theta):
        self.x=x
        self.y=y
        self.theta=theta
        self.ID=ID
        self.degVal=dict()
    def __compute_view_value__(self,ang,seat):
        from math import sqrt, sin, cos, atan, radians, degrees
        other_theta = (seat.theta + ang+90)%360
        #Rotate based on self perspective
        ang = radians((90-ang)%360)
        deltX   = seat.x-self.x
        deltY   = seat.y-self.y
        other_x = cos(ang)*deltX-sin(ang)*deltY
        other_y = sin(ang)*deltX+cos(ang)*deltY
        #If they're behind you, ignore.
        if other_y<-.01: return 0
        #Distance from self to other. Subtracts to simulate depth of field.
        other_dist=max(1,5-sqrt(deltX**2+deltY**2))
        #Find abs angle from direct line of sight
        try: peerAng = degrees(atan(abs(other_y/other_x)))-90
        except: peerAng=0
        #Normalize abs angle into a scaling factor
        minfact=.25
        maxAng=90/(1-minfact)
        deltang = (maxAng-abs(peerAng))/maxAng
        return other_dist*deltang
    def gradePosition(self,Seats):
        score = 0
        for deg in range(-80,81):
            currScore=0
            for seat in Seats.values():
                if seat.ID!=self.ID:
                    currScore += (self.__compute_view_value__((self.theta+deg)%360,seat))
            self.degVal[deg]=currScore
            score+=currScore*(150-abs(deg))/150
        return score/160
    def plotFOVVals(self,scale=False):
        points = sorted(((k,v) for k,v in self.degVal.items()),key=lambda x: x[0])
        x=list()
        y=list()
        for p in points:
            x.append(p[0])
            if not scale: y.append(p[1])
            else: y.append(p[1]*(250-abs(p[0])))
        import matplotlib
        matplotlib.pyplot.plot(x,y)