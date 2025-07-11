import os;
import phylib;
import sqlite3;
import math;
import json;
import random;

import time


HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="700" height="1375" viewBox="-25 -25 1400 2750"
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink">
<rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />"""

FOOTER = """</svg>\n"""

#const for A3
FRAME_RATE = 0.01

################################################################################
# import constants from phylib to global varaibles
BALL_RADIUS   = phylib.PHYLIB_BALL_RADIUS; 
BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER; 
HOLE_RADIUS = phylib.PHYLIB_HOLE_RADIUS; 
TABLE_LENGTH = phylib.PHYLIB_TABLE_LENGTH; 
TABLE_WIDTH = phylib.PHYLIB_TABLE_WIDTH; 
SIM_RATE = phylib.PHYLIB_SIM_RATE; 
VEL_EPSILON = phylib.PHYLIB_VEL_EPSILON; 
DRAG = phylib.PHYLIB_DRAG; 
MAX_TIME = phylib.PHYLIB_MAX_TIME; 
MAX_OBJECTS = phylib.PHYLIB_MAX_OBJECTS; 

################################################################################
# the standard colours of pool balls
# if you are curious check this out:  
# https://billiards.colostate.edu/faq/ball/colors/

BALL_COLOURS = [ 
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",             # no LIGHTRED
    "MEDIUMPURPLE",     # no LIGHTPURPLE
    "LIGHTSALMON",      # no LIGHTORANGE
    "LIGHTGREEN",
    "SANDYBROWN",       # no LIGHTBROWN 
    ];
BALL_POS = [
    [675, 2025], #WHITE
    [674, 885], #YELLOW
    [644, 833], #BLUE
    [704, 832], #RED
    [736, 781], #PURPLE
    [674, 675], #ORANGE
    [613, 781], #GREEN
    [583, 728], #BROWN
    [675, 781], #BLACK
    [704, 728], #LIGHTYELLOW
    [766, 727], #LIGHTBLUE
    [795, 675], #PINK
    [737, 673], #MEDIUMPURPLE
    [643, 727], #LIGHTSALMON
    [613, 673], #LIGHTGREEN
    [553, 676], #SANDYBROWN
]

class Coordinate( phylib.phylib_coord ):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass;



class StillBall( phylib.phylib_object ):
    """
    Python StillBall class.
    """

    def __init__( self, number, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_STILL_BALL, 
                                       number, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = StillBall;

    def svg(self):
        fill = BALL_COLOURS[self.obj.rolling_ball.number]
        x = self.obj.rolling_ball.pos.x
        y = self.obj.rolling_ball.pos.y
        if fill == "WHITE":
            return """ <circle id = "cueball" cx="%d" cy="%d" r="%d" fill="%s" />\n<line id="line" x1="" y1="" x2="" y2="" stroke="white"/>""" % (x, y, BALL_RADIUS, fill)
        else:
            return """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (x, y, BALL_RADIUS, fill)

class RollingBall (phylib.phylib_object):
 
    def __init__( self, number, pos, vel, acc ):
    
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_ROLLING_BALL, 
                                       number, 
                                       pos, vel, acc, 
                                       0.0, 0.0 );
    
        self.__class__ = RollingBall;

    def svg(self):
        fill = BALL_COLOURS[self.obj.rolling_ball.number]
        x = self.obj.rolling_ball.pos.x
        y = self.obj.rolling_ball.pos.y
        if fill == "WHITE":
            return """ <circle id = "cueball" cx="%d" cy="%d" r="%d" fill="%s" />\n<line id="line" x1="" y1="" x2="" y2="" stroke="white"/>""" % (x, y, BALL_RADIUS, fill)
        else:
            return """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (x, y, BALL_RADIUS, fill)
        #return """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (x_pos, y_pos, BALL_RADIUS, fill_colour)
    
class Hole( phylib.phylib_object ):

    def __init__( self, pos ):

        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HOLE,
                                       0,  
                                       pos, None, None, 
                                       0.0, 0.0 );

        self.__class__ = Hole;

    def svg(self):
        return """ <circle cx="%d" cy="%d" r="%d" fill="rgb(32, 32, 32)" />\n""" % (self.obj.hole.pos.x, self.obj.hole.pos.y, HOLE_RADIUS)

class HCushion( phylib.phylib_object ):

    def __init__( self, y ):

        #pos = phylib.phylib_coord(0, y); 
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_STILL_BALL,  
                                       0, 
                                       None, None, None, 
                                       0.0, y );
    
        self.__class__ = HCushion;

    def svg(self):
        if self.obj.hcushion.y == 0:
            return """ <rect width="1400" height="25" x="-25" y="%d" fill="rgb(76, 113, 72)" />\n""" % (-25)
        else: 
            return """ <rect width="1400" height="25" x="-25" y="%d" fill="rgb(76, 113, 72)" />\n""" % (2700)

class VCushion( phylib.phylib_object ):

    def __init__( self, x ):

        #pos = phylib.phylib_coord(x, 0); 
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_STILL_BALL,  
                                       0, 
                                       None, None, None, 
                                       x, 0.0 );
    
        self.__class__ = VCushion;

    def svg(self):
        if (self.obj.vcushion.x == 0):
            return """ <rect width="25" height="2750" x="%d" y="-25" fill="rgb(76, 113, 72)" />\n""" % (-25)
        else:
            return """ <rect width="25" height="2750" x="%d" y="-25" fill="rgb(76, 113, 72)" />\n""" % (1350)
        

class Table( phylib.phylib_table ):
    """
    Pool table class.
    """

    def __init__( self, setup=False, gameName=None, plyr1Name=None, plyr2Name=None):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__( self );
        #self.phylib_table_instance = phylib.phylib_table()
        self.current = -1;
        # super().__init__()
        # self.current = -1
        if setup == True:
            self.setupTable(gameName, plyr1Name, plyr2Name)

    def __iadd__( self, other ):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object( other );
        return self;

    def __iter__( self ):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        self.current = -1
        return self

    def __next__( self ):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1;  # increment the index to the next object
        if self.current < MAX_OBJECTS:   # check if there are no more objects
            return self[ self.current ]; # return the latest object

        # if we get there then we have gone through all the objects
        #self.current = -1;    # reset the index counter
        raise StopIteration;  # raise StopIteration to tell for loop to stop

    def __getitem__( self, index ):
        """
        This method adds item retreivel support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object( index ); 
        if result==None:
            return None;
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall;
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall;
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole;
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion;
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion;
        return result;

    def __str__( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = "";    # create empty string
        result += "time = %6.1f;\n" % self.time;    # append time
        for i,obj in enumerate(self): # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i,obj);  # append object description
        return result;  # return the string

    def segment( self ):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """

        result = phylib.phylib_table.segment( self );
        if result:
            result.__class__ = Table;
            result.current = -1;
        return result;

    def svg(self):
        svg_content = HEADER
        for obj in (self):
            if obj is not None:
                svg_content += obj.svg()
        svg_content += """<line id="line" x1="" y1="" x2="" y2="" stroke="white"/>"""
        svg_content += FOOTER
        
        return svg_content
    
    #A3 FUNCTIONS
    def roll( self, t ):
        new = Table();
        for ball in self:
            if isinstance( ball, RollingBall ):
                # create4 a new ball with the same number as the old ball
                new_ball = RollingBall( ball.obj.rolling_ball.number, Coordinate(0,0), Coordinate(0,0), Coordinate(0,0) );
                
                # compute where it rolls to
                phylib.phylib_roll( new_ball, ball, t );
                
                # add ball to table
                new += new_ball;
            if isinstance( ball, StillBall ):
                # create a new ball with the same number and pos as the old ball
                new_ball = StillBall( ball.obj.still_ball.number, Coordinate( ball.obj.still_ball.pos.x, ball.obj.still_ball.pos.y ) );
                
                # add ball to table
                new += new_ball;
        # return table
        return new;

    def cueBall(self):
        for ball in self:
            if ball is not None:
                if ball.type == phylib.PHYLIB_STILL_BALL or ball.type == phylib.PHYLIB_ROLLING_BALL:
                    if ball.obj.still_ball.number == 0:  
                        return ball
        return None
    
    def setupTable(self, gameName=None, player1Name=None, player2Name=None):
        for i in range(0, len(BALL_POS)):
            self += StillBall(i, Coordinate(BALL_POS[i][0], BALL_POS[i][1]))
        return self

class Database():
    def __init__(self, reset=False):
        if reset == True:
            if os.path.exists("phylib.db"):
                os.remove("phylib.db")
        self.connection = sqlite3.connect("phylib.db")
        self.conn = self.connection
    
    def createDB(self):
        current = self.connection.cursor()
        # * on the condition the tables do not already exist!
        x = 0
        if (current.execute("""
                            SELECT count(*) FROM sqlite_master WHERE type = 'table' AND name = 'Ball'
                            """).fetchall()[0][0] == 0):  
            #print("Creating Ball")
            current.execute("""
                            CREATE TABLE Ball (
                            BALLID  INTEGER PRIMARY KEY AUTOINCREMENT,
                            BALLNO  INTEGER NOT NULL,
                            XPOS    FLOAT NOT NULL,
                            YPOS    FLOAT NOT NULL,
                            XVEL    FLOAT,
                            YVEL    FLOAT
                            );
                            """) #BALL -> A ball at a specific instance in time. Still balls have null velocity
            x += 1
        if (current.execute("""
                            SELECT count(*) FROM sqlite_master WHERE type = 'table' AND name = 'TTable'
                            """).fetchall()[0][0] == 0):
            #print("Creating TTable") 
            current.execute("""
                            CREATE TABLE TTable (
                            TABLEID INTEGER PRIMARY KEY AUTOINCREMENT,
                            TIME    FLOAT NOT NULL
                            );
                            """) # TTABLE -> Represents a table at a specific instance in time.
                                # the same table at different points in time, during different shots and games will have multiple rows in this table
                                # time is the length of time since the current shot was initiated
            x += 1
        if (current.execute("""
                            SELECT count(*) FROM sqlite_master WHERE type = 'table' AND name = 'BallTable'
                            """).fetchall()[0][0] == 0):  
            #print("Creating BallTable")
            current.execute("""
                            CREATE TABLE BallTable (
                            BALLID INTEGER NOT NULL,
                            TABLEID INTEGER NOT NULL,
                            FOREIGN KEY (BALLID) REFERENCES BALLID,
                            FOREIGN KEY (TABLEID) REFERENCES TABLEID
                            );
                            """) #BALLTABLE -> connects balls to their tables by joining the ID of TTable with the ID of Ball
            x += 1
        if (current.execute("""
                            SELECT count(*) FROM sqlite_master WHERE type = 'table' AND name = 'Shot'
                            """).fetchall()[0][0] == 0):  
            #print("Creating Shot")
            current.execute("""
                            CREATE TABLE Shot (
                            SHOTID  INTEGER PRIMARY KEY AUTOINCREMENT,
                            PLAYERID INTEGER NOT NULL,
                            GAMEID  INTEGER NOT NULL,
                            FOREIGN KEY (PLAYERID) REFERENCES PLAYERID,
                            FOREIGN KEY (GAMEID) REFERENCES GAMEID
                            );
                            """) #SHOT -> Represents a shot in a game of pool
                                #PLAYERID is the id of the player that shot the ball, referencing the Player table
                                #GAMEID is the id of the game during which the shot was made, referencing the Game table
                                #Shots are assumed to occur in order of increasing SHOTID
            x += 1
        if (current.execute("""
                            SELECT count(*) FROM sqlite_master WHERE type = 'table' AND name = 'TableShot'
                            """).fetchall()[0][0] == 0):  
            #print("Creating TableShot")
            current.execute("""
                            CREATE TABLE TableShot (
                            TABLEID  INTEGER NOT NULL,
                            SHOTID   INTEGER NOT NULL,
                            FOREIGN KEY (TABLEID) REFERENCES TABLEID,
                            FOREIGN KEY (SHOTID) REFERENCES SHOTID
                            );
                            """) #TABLESHOT -> connects table snapshots to tables by
                                # joining the TABLEID of TTable with the SHOTID of Shot
                                #TABLEIDs are assumed to be in chronological order
                                #(i.e. the smallest TABLEID represents the table at the beginning of the shot)
            x += 1
        if (current.execute("""
                            SELECT count(*) FROM sqlite_master WHERE type = 'table' AND name = 'Game'
                            """).fetchall()[0][0] == 0):  
            #print("Creating Game")
            current.execute("""
                            CREATE TABLE Game (
                            GAMEID      INTEGER PRIMARY KEY AUTOINCREMENT,
                            GAMENAME    VARCHAR(64) NOT NULL
                            );
                            """) #GAME -> connects GAMEIDs to GAMENAMES
        if (current.execute("""
                            SELECT count(*) FROM sqlite_master WHERE type = 'table' AND name = 'Player'
                            """).fetchall()[0][0] == 0):  
            #print("Creating Player")
            current.execute("""
                            CREATE TABLE Player (
                            PLAYERID INTEGER PRIMARY KEY AUTOINCREMENT,
                            GAMEID  INTEGER NOT NULL,
                            PLAYERNAME  VARCHAR(64) NOT NULL,
                            FOREIGN KEY (GAMEID) REFERENCES GAMEID
                            );
                            """) #PLAYER -> connects PLAYERIDs to GAMEIDs and PLAYERNAMEs
                                #the player with the smallest ID is assumed to go first
            x += 1
        #close and commit
        current.close()
        self.connection.commit()
    
    def readTable(self, tableID):
        current = self.connection.cursor()
        # we do tableID + 1, not tableID, because SQL likes to start at 1, but we like to start at 0
        if (current.execute(f"""
                            SELECT COUNT(TABLEID) FROM BallTable
                            WHERE TABLEID = {tableID + 1};
                            """) == 0):
            #return early
            return None
        balls = current.execute(f"""
                                SELECT Ball.BALLID, BALLNO, XPOS, YPOS, XVEL, YVEL 
                                FROM (BallTable INNER JOIN Ball ON BallTable.BALLID = Ball.BALLID)
                                WHERE BallTable.TABLEID = {tableID + 1};
                                """).fetchall()
        #print(f"BALLS: {balls}")
        time = current.execute(f"""
                               SELECT TIME FROM TTable
                               WHERE TABLEID = {tableID + 1};
                               """).fetchall()
        if (len(time) == 0):
            return None
        time = time[0][0]
        #print(f"TIME: {time}")
        table = Table()
        table.time = time
        for ball in balls:
            #list stores tuples of every row
            #tuple is as follows: (ballid, ballno, xpos, ypos, xvel, yvel)
            if ball[4] == None and ball[5] == None:
                #still ball
                ballObj = StillBall(ball[1], Coordinate(ball[2], ball[3]))
            else:
                #padding
                if (ball[4] == None):
                    ball[4] = 0
                if (ball[5] == None):
                    ball[5] = 0
                vel = Coordinate(ball[4], ball[5])
                velSpeed = phylib.phylib_length(vel)
                ballObj = RollingBall(ball[1], Coordinate(ball[2], ball[3]), Coordinate(ball[4], ball[5]),
                                      Coordinate(((ball[4] * -1.0) / velSpeed) * DRAG, ((ball[5] * -1.0) / velSpeed) * DRAG))
            table += ballObj
        #table.printTable()
        current.close()
        self.connection.commit()
        return table
    
    def writeTable(self, table):
        current = self.connection.cursor()
        current.execute(f"""
        INSERT INTO TTable
        VALUES(NULL, {table.time});
        """)
        id = current.lastrowid #guaranteed to have an ID
        for object in table:
            if object.__class__ == RollingBall:
                current.execute(f"""
                                INSERT INTO Ball
                                VALUES(
                                    NULL,
                                    {object.obj.rolling_ball.number},
                                    {object.obj.rolling_ball.pos.x},
                                    {object.obj.rolling_ball.pos.y},
                                    {object.obj.rolling_ball.vel.x},
                                    {object.obj.rolling_ball.vel.y}
                                );
                                """)
                ballid = current.lastrowid
                current.execute(f"""
                                INSERT INTO BallTable
                                VALUES({ballid}, {id});
                                """)
            elif object.__class__ == StillBall:
                current.execute(f"""
                                INSERT INTO Ball
                                VALUES(
                                    NULL,
                                    {object.obj.rolling_ball.number},
                                    {object.obj.rolling_ball.pos.x},
                                    {object.obj.rolling_ball.pos.y},
                                    NULL,
                                    NULL
                                );
                                """)
                ballid = current.lastrowid
                current.execute(f"""
                                INSERT INTO BallTable
                                VALUES({ballid}, {id});
                                """)
        current.close()
        self.connection.commit()
        #print(f"Submitted Table {id}")
        return id - 1
    
    def setTableShot(self, tableID, shotID):
        current = self.connection.cursor()
        current.execute(f"""
                        INSERT INTO TableShot
                        VALUES({tableID + 1}, {shotID + 1});
                        """)
    
    def close(self):
        self.connection.commit()
        self.connection.close()
    
    def getGame(self, gameId): #return the list (table, tuples and all)
        current = self.connection.cursor()
        
        ret = current.execute(f"""
                        SELECT PLAYERID, GAMENAME, PLAYERNAME FROM (Game INNER JOIN Player ON Game.GAMEID = Player.GAMEID)
                        WHERE Game.GAMEID = {gameId};
                        """) 
        #assume the first player is the first entry of ret
        #print(ret)
        current.close()
        return ret
    
    def setGame(self, gameName, player1Name, player2Name):
        current = self.connection.cursor()
        #print(gameName + " " + player1Name + " " + player2Name)
        #game
        gameId = current.execute(f"""
                        INSERT INTO Game (GAMEID, GAMENAME)
                        VALUES(NULL, '{gameName}');
                        """).lastrowid #no need to decrement gameID since we're just working in sql
        #player
        current.execute(f"""
                        INSERT INTO Player (PLAYERID, GAMEID, PLAYERNAME)
                        VALUES(NULL, {gameId}, '{player1Name}');
                        """)
        current.execute(f"""
                        INSERT INTO Player (PLAYERID, GAMEID, PLAYERNAME)
                        VALUES(NULL, {gameId}, '{player2Name}');
                        """)
        current.close()
        self.connection.commit()
        return gameId - 1
        
    def newShot(self, playerName, table, xvel, yvel, gameId):
        current = self.connection.cursor()
        
        #get player id from player name
        playerGame = current.execute(f"""
                                   SELECT PLAYERID, GAMEID FROM Player
                                   WHERE  PLAYERNAME = '{playerName}' AND GAMEID = {gameId + 1};
                                   """).fetchall()
        
        #print(playerGame)
        #insert our shot now that we have player and game id
        shotId = current.execute(f"""
                                 INSERT INTO Shot (SHOTID, PLAYERID, GAMEID)
                                 VALUES(NULL, {playerGame[0][0]}, {playerGame[0][1]});
                                 """).lastrowid
        #print(shotId)
        current.close()
        self.connection.commit()
        return shotId - 1

    
class Game():
    """
    Python Game class.
    """
    game_id = 0

    def __init__(self, gameID=None, gameName=None, player1Name=None, player2Name=None):
        self.database = Database(reset=True)
        #self.database.setGame(1, "Plyr1", "Plyr2")


    def shoot(self, gameName, playerName, table, xvel, yvel):
        cueball = table.cueBall()
        posx = cueball.obj.still_ball.pos.x
        posy = cueball.obj.still_ball.pos.y
        cueball.type = phylib.PHYLIB_ROLLING_BALL
        cueball.obj.rolling_ball.pos.x = posx
        cueball.obj.rolling_ball.pos.y = posy
        
        cueball.obj.rolling_ball.vel.x = xvel
        cueball.obj.rolling_ball.vel.y = yvel 
        cueVel = Coordinate(xvel, yvel)
        speed = phylib.phylib_length(cueVel)
        
        cueball.obj.rolling_ball.acc.x = ((xvel * -1.0) / speed) * DRAG
        cueball.obj.rolling_ball.acc.y = ((yvel * -1.0) / speed) * DRAG
        
        cueball.obj.rolling_ball.number = 0


        svgs = []
        segTable = table.segment()

        #while we still have table segments
        while segTable is not None:

            frames = int((segTable.time - table.time) / FRAME_RATE)
            
            for i in range(frames): #its a range of i to frames
                frameTime = i * FRAME_RATE
                newTable = table.roll(frameTime)
                newTable.time = table.time + frameTime
                svgs.append(newTable.svg())
            table = segTable #this forces our table to always grab the very last one
            segTable = table.segment() 
        
        return table, svgs