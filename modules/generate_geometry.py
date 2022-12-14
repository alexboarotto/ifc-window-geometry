import numpy

class generate_geometry:
    # creates a rectangle given starting point, width and height
    def rectangle(width, height, starting_point = numpy.array([0,0,0])):
        # creates array of coordinates
        # order of creation -> bottom_left, bottom_right, top_right, top_left
        rectangle = numpy.array([starting_point for i in range(0,5)])

        # sets bottom right point
        rectangle[1][0]+=width

        # sets top right point
        rectangle[2][0]+=width
        rectangle[2][2]+=height

        # sets top left point
        rectangle[3][2]+=height

        return rectangle

    # get height from a rectangle
    def get_rect_height(rect):
        return rect[3][2] - rect[0][2]

    # get width from a rectangle
    def get_rect_width(rect):
        return rect[1][0] - rect[0][0]
    
    # creates concentric inner rectangle given an offset
    def offset_rectangle(self, offset, outer_rect):
        sp = outer_rect[0].copy()
        sp[0] += offset
        sp[2] += offset
        return self.rectangle(starting_point=sp, width=self.get_rect_width(outer_rect)-offset*2, height=self.get_rect_height(outer_rect)-offset*2)

    """
    GENERATES AND RETURNS SCHEMA FOR 'SINGLE_PANEL' WINDOW TYPE
    Lining contains an inner and outer rectangle
    There is only 1 panel with an inner an outer rectangle
    """
    @classmethod
    def single_panel(self, OverallHeight, OverallWidth, LiningProps, PanelProps):
        # schema for SINGLE_PANEL geometry
        output = {"lining":
                    {
                        "outer": [],
                        "inner": []
                    },
                    "panels":
                    {
                        "frame":
                        {
                            "outer": [],
                            "inner": []
                        }
                    }
                 }

        #==============================================================
        # LINING
        #==============================================================
        Lthickness = LiningProps["LiningThickness"]
        POffset = LiningProps["LiningToPanelOffsetX"]

        # generate rectangle using overall height and width
        output["lining"]["outer"] = self.rectangle(OverallWidth, OverallHeight)

        # generate inner rectangle from outer rectangle using lining thickness 
        output["lining"]["inner"] = self.offset_rectangle(self, offset=Lthickness, outer_rect=output["lining"]["outer"])

        #==============================================================
        # PANELS
        #==============================================================
        Fthickness = PanelProps["FrameThickness"]

        # generates outer rectangle for frame given the offset from the lining
        output["panels"]["frame"]["outer"] = self.offset_rectangle(self, offset=POffset, outer_rect=output["lining"]["outer"])

        # generate inner rectangle from outer rectangle using frame thickness 
        output["panels"]["frame"]["inner"] = self.offset_rectangle(self, offset=Fthickness, outer_rect=output["panels"]["frame"]["outer"])

        return output

    """
    GENERATES AND RETURNS SCHEMA FOR 'DOUBLE_PANEL_HORIZONTAL' WINDOW TYPE
    Lining contains 2 inner rectangles (one for each frame) separated by a transom
    There are 2 panels:
    The fisrt starts offsetted from the bottom left corner of the lining
    The second one starts offsetted from the intersection between the lining's left side and transom centerline
    """
    @classmethod
    def double_panel_horizontal(self, OverallHeight, OverallWidth, LiningProps, BottomPanelProps, TopPanelProps):
        # schema for DOUBLE_PANEL_HORIZONTAL geometry
        output = {"lining":
                    {
                        "outer": [],
                        "inner": {
                            "inner_bottom": [],
                            "inner_top": []  
                        }
                    },
                    "panels":
                    {
                        "frame_bottom":
                        {
                            "outer": [],
                            "inner": []
                        },
                        "frame_top":
                        {
                            "outer": [],
                            "inner": []
                        }
                    }
                }
        

        # Handle to props
        Lthickness = LiningProps["LiningThickness"]
        TransomOffset = LiningProps["FirstTransomOffset"] 
        TransomThickness = LiningProps["TransomThickness"]

        #==============================================================
        # LINING
        #==============================================================

        # generate rectangle using overall height and width
        output["lining"]["outer"] = self.rectangle(OverallWidth, OverallHeight)

        # calculate bottom rectangle parameters
        LBottomSP = numpy.array([Lthickness, 0, Lthickness])
        LBottomHeight = TransomOffset - Lthickness - TransomThickness/2
        LBottomWidth = OverallWidth - Lthickness*2 

        # generate bottom inner rectangle for lining
        output["lining"]["inner"]["inner_bottom"] = self.rectangle(starting_point=LBottomSP, height=LBottomHeight, width=LBottomWidth)

        # calculate top rectangle parameters
        LTopSP = numpy.array([Lthickness, 0, TransomOffset+TransomThickness/2])
        LTopHeight = OverallHeight-TransomOffset+TransomThickness/2-Lthickness*2
        LTopWidth = OverallWidth - Lthickness*2 

        # generate top inner rectangle for lining
        output["lining"]["inner"]["inner_top"] = self.rectangle(starting_point=LTopSP, height=LTopHeight, width=LTopWidth)

        #==============================================================
        # PANELS
        #==============================================================
        LTFoffsetX = LiningProps["LiningToPanelOffsetX"]
        FBottomThickness = BottomPanelProps["FrameThickness"]
        FTopThickness = TopPanelProps["FrameThickness"]

        # generates outer rectangle for frame given the offset from the lining inner rect
        output["panels"]["frame_bottom"]["outer"] = self.offset_rectangle(self, offset=-(Lthickness-LTFoffsetX), outer_rect=output["lining"]["inner"]["inner_bottom"])

        # generate inner rectangle from outer rectangle using frame thickness
        output["panels"]["frame_bottom"]["inner"] = self.offset_rectangle(self, offset=FBottomThickness, outer_rect=output["panels"]["frame_bottom"]["outer"])

        # generates outer rectangle for frame given the offset from the lining inner rect
        output["panels"]["frame_top"]["outer"] = self.offset_rectangle(self, offset=-(Lthickness-LTFoffsetX), outer_rect=output["lining"]["inner"]["inner_top"])

        # generate inner rectangle from outer rectangle using frame thickness 
        output["panels"]["frame_top"]["inner"] = self.offset_rectangle(self, offset=FTopThickness, outer_rect=output["panels"]["frame_top"]["outer"])

        return output 



    """
    GENERATES AND RETURNS SCHEMA FOR 'DOUBLE_PANEL_VERTICAL' WINDOW TYPE
    Lining contains 2 inner rectangles (one for each frame) separated by a mulliojn
    There are 2 panels:
    The first starts offsetted from the bottom left corner of the lining
    The second one starts offsetted from the intersection between the lining's bottom side and mullion centerline
    """
    @classmethod
    def double_panel_vertical(self, OverallHeight, OverallWidth, LiningProps, LeftPanelProps, RightPanelProps):
        # schema for DOUBLE_PANEL_VERTICAL geometry
        output = {"lining":
                    {
                        "outer": [],
                        "inner": {
                            "inner_left": [],
                            "inner_right": []  
                        }
                    },
                    "panels":
                    {
                        "frame_left":
                        {
                            "outer": [],
                            "inner": []
                        },
                        "frame_right":
                        {
                            "outer": [],
                            "inner": []
                        }
                    }
                }
        

        # Handle to props
        Lthickness = LiningProps["LiningThickness"]
        MullionOffset = LiningProps["FirstMullionOffset"] 
        MullionThickness = LiningProps["MullionThickness"]

        #==============================================================
        # LINING
        #==============================================================

        # generate rectangle using overall height and width
        output["lining"]["outer"] = self.rectangle(OverallWidth, OverallHeight)

        # calculate left rectangle parameters
        LLeftSP = numpy.array([Lthickness, 0, Lthickness])
        LLeftWidth = MullionOffset - Lthickness - MullionThickness/2
        LLeftHeight = OverallHeight - Lthickness*2 

        # generate left inner rectangle for lining
        output["lining"]["inner"]["inner_left"] = self.rectangle(starting_point=LLeftSP, height=LLeftHeight, width=LLeftWidth)

        # calculate right rectangle parameters
        LRightSP = numpy.array([MullionOffset+MullionThickness/2, 0, Lthickness])
        LRightWidth = OverallWidth-MullionOffset+MullionThickness/2-Lthickness*2
        LRightHeight = OverallHeight - Lthickness*2 

        # generate right inner rectangle for lining
        output["lining"]["inner"]["inner_right"] = self.rectangle(starting_point=LRightSP, height=LRightHeight, width=LRightWidth)

        #==============================================================
        # PANELS
        #==============================================================
        LTFoffsetX = LiningProps["LiningToPanelOffsetX"]
        FLeftThickness = LeftPanelProps["FrameThickness"]
        FRightThickness = RightPanelProps["FrameThickness"]

        # generates outer rectangle for frame given the offset from the lining inner rect
        output["panels"]["frame_left"]["outer"] = self.offset_rectangle(self, offset=-(Lthickness-LTFoffsetX), outer_rect=output["lining"]["inner"]["inner_left"])

        # generate inner rectangle from outer rectangle using frame thickness 
        output["panels"]["frame_left"]["inner"] = self.offset_rectangle(self, offset=FLeftThickness, outer_rect=output["panels"]["frame_left"]["outer"])

        # generates outer rectangle for frame given the offset from the lining inner rect
        output["panels"]["frame_right"]["outer"] = self.offset_rectangle(self, offset=-(Lthickness-LTFoffsetX), outer_rect=output["lining"]["inner"]["inner_right"])

        # generate inner rectangle from outer rectangle using frame thickness 
        output["panels"]["frame_right"]["inner"] = self.offset_rectangle(self, offset=FRightThickness, outer_rect=output["panels"]["frame_right"]["outer"])

        return output 

    """
    GENERATES AND RETURNS SCHEMA FOR 'TRIPLE_PANEL_BOTTOM' WINDOW TYPE
    Lining contains 3 inner rectangles (one for each frame)
    There are 3 panels:
    The first starts offsetted from the bottom left corner of the lining and extends horizontally to the other end of the lining
    but extends vertically until the transom
    The second and third start above the bottom one and are separated by a mullion
    """
    @classmethod
    def triple_panel_bottom(self, OverallHeight, OverallWidth, LiningProps, LeftPanelProps, RightPanelProps, BottomPanelProps):
        # schema for TRIPLE_PANEL_BOTTOM geometry
        output = {"lining":
                    {
                        "outer": [],
                        "inner": {
                            "inner_left": [],
                            "inner_right": [], 
                            "inner_bottom": [] 
                        }
                    },
                    "panels":
                    {
                        "frame_left":
                        {
                            "outer": [],
                            "inner": []
                        },
                        "frame_right":
                        {
                            "outer": [],
                            "inner": []
                        },
                        "frame_bottom":
                        {
                            "outer": [],
                            "inner": []
                        }
                    }
                }
        

        # Handle to props
        Lthickness = LiningProps["LiningThickness"]
        TransomOffset = LiningProps["FirstTransomOffset"] 
        TransomThickness = LiningProps["TransomThickness"]
        MullionOffset = LiningProps["FirstMullionOffset"] 
        MullionThickness = LiningProps["MullionThickness"]

        #==============================================================
        # LINING
        #==============================================================

        # generate rectangle using overall height and width
        output["lining"]["outer"] = self.rectangle(OverallWidth, OverallHeight)

        # calculate bottom rectangle parameters
        LBottomSP = numpy.array([Lthickness, 0, Lthickness])
        LBottomHeight = TransomOffset - Lthickness - TransomThickness/2
        LBottomWidth = OverallWidth - Lthickness*2 

        # generate bottom inner rectangle for lining 
        output["lining"]["inner"]["inner_bottom"] = self.rectangle(starting_point=LBottomSP, height=LBottomHeight, width=LBottomWidth)

        # calculate Left rectangle parameters
        LLeftSP = numpy.array([Lthickness, 0, TransomOffset+TransomThickness/2])
        LLeftWidth = MullionOffset - Lthickness - MullionThickness/2
        LLeftHeight = OverallHeight-TransomOffset-TransomThickness/2-Lthickness

        # generate right inner rectangle for lining
        output["lining"]["inner"]["inner_left"] = self.rectangle(starting_point=LLeftSP, height=LLeftHeight, width=LLeftWidth)

        # calculate right rectangle parameters
        LRightSP = numpy.array([MullionOffset+MullionThickness/2, 0, TransomOffset+TransomThickness/2])
        LRightWidth = OverallWidth-MullionOffset-MullionThickness/2-Lthickness
        LRightHeight = OverallHeight-TransomOffset-TransomThickness/2-Lthickness 

        # generate right inner rectangle for lining
        output["lining"]["inner"]["inner_right"] = self.rectangle(starting_point=LRightSP, height=LRightHeight, width=LRightWidth)

        #==============================================================
        # PANELS
        #==============================================================
        LTFoffsetX = LiningProps["LiningToPanelOffsetX"]
        FLeftThickness = LeftPanelProps["FrameThickness"]
        FRightThickness = RightPanelProps["FrameThickness"]
        FBottomThickness = BottomPanelProps["FrameThickness"]

        # generates outer rectangle for frame given the offset from the lining inner rect
        output["panels"]["frame_bottom"]["outer"] = self.offset_rectangle(self, offset=-(Lthickness-LTFoffsetX), outer_rect=output["lining"]["inner"]["inner_bottom"])

        # generate inner rectangle from outer rectangle using frame thickness 
        output["panels"]["frame_bottom"]["inner"] = self.offset_rectangle(self, offset=FLeftThickness, outer_rect=output["panels"]["frame_bottom"]["outer"])

        # generates outer rectangle for frame given the offset from the lining inner rect
        output["panels"]["frame_left"]["outer"] = self.offset_rectangle(self, offset=-(Lthickness-LTFoffsetX), outer_rect=output["lining"]["inner"]["inner_left"])

        # generate inner rectangle from outer rectangle using frame thickness 
        output["panels"]["frame_left"]["inner"] = self.offset_rectangle(self, offset=FLeftThickness, outer_rect=output["panels"]["frame_left"]["outer"])

        # generates outer rectangle for frame given the offset from the lining inner rect
        output["panels"]["frame_right"]["outer"] = self.offset_rectangle(self, offset=-(Lthickness-LTFoffsetX), outer_rect=output["lining"]["inner"]["inner_right"])

        # generate inner rectangle from outer rectangle using frame thickness 
        output["panels"]["frame_right"]["inner"] = self.offset_rectangle(self, offset=FRightThickness, outer_rect=output["panels"]["frame_right"]["outer"])

        return output 

    """
    GENERATES AND RETURNS SCHEMA FOR 'TRIPLE_PANEL_HORIZONTAL' WINDOW TYPE
    Lining contains 3 inner rectangles (one for each frame)
    There are 3 panels:
    Top, middle and bottom. Divided by 2 transoms
    """
    @classmethod
    def triple_panel_horizontal(self, OverallHeight, OverallWidth, LiningProps, TopPanelProps, MiddlePanelProps, BottomPanelProps):
        # schema for TRIPLE_PANEL_BOTTOM geometry
        output = {"lining":
                    {
                        "outer": [],
                        "inner": {
                            "inner_top": [],
                            "inner_middle": [], 
                            "inner_bottom": [] 
                        }
                    },
                    "panels":
                    {
                        "frame_top":
                        {
                            "outer": [],
                            "inner": []
                        },
                        "frame_middle":
                        {
                            "outer": [],
                            "inner": []
                        },
                        "frame_bottom":
                        {
                            "outer": [],
                            "inner": []
                        }
                    }
                }
        

        # Handle to props
        Lthickness = LiningProps["LiningThickness"]
        FirstTransomOffset = LiningProps["FirstTransomOffset"] 
        SecondTransomOffset = LiningProps["SecondTransomOffset"] 
        TransomThickness = LiningProps["TransomThickness"]


        #==============================================================
        # LINING
        #==============================================================

        # generate rectangle using overall height and width
        output["lining"]["outer"] = self.rectangle(OverallWidth, OverallHeight)

        # calculate bottom rectangle parameters
        LBottomSP = numpy.array([Lthickness, 0, Lthickness])
        LBottomHeight = FirstTransomOffset - Lthickness - TransomThickness/2
        LBottomWidth = OverallWidth - Lthickness*2 

        # generate bottom inner rectangle for lining 
        output["lining"]["inner"]["inner_bottom"] = self.rectangle(starting_point=LBottomSP, height=LBottomHeight, width=LBottomWidth)

        # calculate Middle rectangle parameters
        LMiddleSP = numpy.array([Lthickness, 0, FirstTransomOffset+TransomThickness/2])
        LMiddleWidth = LBottomWidth
        LMiddleHeight = SecondTransomOffset-FirstTransomOffset-TransomThickness

        # generate right inner rectangle for lining
        output["lining"]["inner"]["inner_middle"] = self.rectangle(starting_point=LMiddleSP, height=LMiddleHeight, width=LMiddleWidth)

        # calculate Top rectangle parameters
        LTopSP = numpy.array([Lthickness, 0, SecondTransomOffset+TransomThickness/2])
        LTopWidth = LBottomWidth
        LTopHeight = OverallHeight-SecondTransomOffset-TransomThickness/2-Lthickness 

        # generate Top inner rectangle for lining
        output["lining"]["inner"]["inner_top"] = self.rectangle(starting_point=LTopSP, height=LTopHeight, width=LTopWidth)

        #==============================================================
        # PANELS
        #==============================================================
        LTFoffsetX = LiningProps["LiningToPanelOffsetX"]
        FTopThickness = TopPanelProps["FrameThickness"]
        FMiddleThickness = MiddlePanelProps["FrameThickness"]
        FBottomThickness = BottomPanelProps["FrameThickness"]

        # generates outer rectangle for frame given the offset from the lining inner rect
        output["panels"]["frame_bottom"]["outer"] = self.offset_rectangle(self, offset=-(Lthickness-LTFoffsetX), outer_rect=output["lining"]["inner"]["inner_bottom"])

        # generate inner rectangle from outer rectangle using frame thickness 
        output["panels"]["frame_bottom"]["inner"] = self.offset_rectangle(self, offset=FBottomThickness, outer_rect=output["panels"]["frame_bottom"]["outer"])

        # generates outer rectangle for frame given the offset from the lining inner rect
        output["panels"]["frame_middle"]["outer"] = self.offset_rectangle(self, offset=-(Lthickness-LTFoffsetX), outer_rect=output["lining"]["inner"]["inner_middle"])

        # generate inner rectangle from outer rectangle using frame thickness 
        output["panels"]["frame_middle"]["inner"] = self.offset_rectangle(self, offset=FMiddleThickness, outer_rect=output["panels"]["frame_middle"]["outer"])

        # generates outer rectangle for frame given the offset from the lining inner rect
        output["panels"]["frame_top"]["outer"] = self.offset_rectangle(self, offset=-(Lthickness-LTFoffsetX), outer_rect=output["lining"]["inner"]["inner_top"])

        # generate inner rectangle from outer rectangle using frame thickness 
        output["panels"]["frame_top"]["inner"] = self.offset_rectangle(self, offset=FTopThickness, outer_rect=output["panels"]["frame_top"]["outer"])

        return output 

    @classmethod
    def triple_panel_left(self, OverallHeight, OverallWidth, LiningProps, LeftPanelProps, TopRightPanelProps, BottomRightPanelProps):
        # schema for TRIPLE_PANEL_BOTTOM geometry
        output = {"lining":
                    {
                        "outer": [],
                        "inner": {
                            "inner_left": [],
                            "inner_right_top": [], 
                            "inner_right_bottom": [] 
                        }
                    },
                    "panels":
                    {
                        "frame_left":
                        {
                            "outer": [],
                            "inner": []
                        },
                        "frame_right_top":
                        {
                            "outer": [],
                            "inner": []
                        },
                        "frame_right_bottom":
                        {
                            "outer": [],
                            "inner": []
                        }
                    }
                }
        

        # Handle to props
        Lthickness = LiningProps["LiningThickness"]
        TransomOffset = LiningProps["FirstTransomOffset"] 
        TransomThickness = LiningProps["TransomThickness"]
        MullionOffset = LiningProps["FirstMullionOffset"] 
        MullionThickness = LiningProps["MullionThickness"]

        #==============================================================
        # LINING
        #==============================================================

        # generate rectangle using overall height and width
        output["lining"]["outer"] = self.rectangle(OverallWidth, OverallHeight)

        # calculate Left rectangle parameters
        LLeftSP = numpy.array([Lthickness, 0, Lthickness])
        LLeftHeight = OverallHeight - Lthickness*2
        LLeftWidth = MullionOffset - Lthickness - MullionThickness/2

        # generate Left inner rectangle for lining 
        output["lining"]["inner"]["inner_left"] = self.rectangle(starting_point=LLeftSP, height=LLeftHeight, width=LLeftWidth)

        # calculate bottom right rectangle parameters
        LRightBSP = numpy.array([MullionOffset+MullionThickness/2, 0, Lthickness])
        LRightBWidth = OverallWidth-MullionOffset-Lthickness - MullionThickness/2
        LRightBHeight = TransomOffset-Lthickness-TransomThickness/2

        # generate right inner rectangle for lining
        output["lining"]["inner"]["inner_right_bottom"] = self.rectangle(starting_point=LRightBSP, height=LRightBHeight, width=LRightBWidth)

        # calculate right rectangle parameters
        LRightTSP = numpy.array([TransomOffset+TransomThickness/2, 0, MullionOffset+MullionThickness/2])
        LRightTWidth = OverallWidth-MullionOffset-MullionThickness/2-Lthickness
        LRightTHeight = OverallHeight-TransomOffset-TransomThickness/2-Lthickness 

        # generate top right inner rectangle for lining
        output["lining"]["inner"]["inner_right_top"] = self.rectangle(starting_point=LRightTSP, height=LRightTHeight, width=LRightTWidth)

        #==============================================================
        # PANELS
        #==============================================================
        LTFoffsetX = LiningProps["LiningToPanelOffsetX"]
        FLeftThickness = LeftPanelProps["FrameThickness"]
        FRightBThickness = BottomRightPanelProps["FrameThickness"]
        FRightTThickness = TopRightPanelProps["FrameThickness"]

        # generates outer rectangle for frame given the offset from the lining inner rect
        output["panels"]["frame_left"]["outer"] = self.offset_rectangle(self, offset=-(Lthickness-LTFoffsetX), outer_rect=output["lining"]["inner"]["inner_left"])

        # generate inner rectangle from outer rectangle using frame thickness 
        output["panels"]["frame_left"]["inner"] = self.offset_rectangle(self, offset=FLeftThickness, outer_rect=output["panels"]["frame_left"]["outer"])

        # generates outer rectangle for frame given the offset from the lining inner rect
        output["panels"]["frame_right_top"]["outer"] = self.offset_rectangle(self, offset=-(Lthickness-LTFoffsetX), outer_rect=output["lining"]["inner"]["inner_right_top"])

        # generate inner rectangle from outer rectangle using frame thickness 
        output["panels"]["frame_right_top"]["inner"] = self.offset_rectangle(self, offset=FRightTThickness, outer_rect=output["panels"]["frame_right_top"]["outer"])

        # generates outer rectangle for frame given the offset from the lining inner rect
        output["panels"]["frame_right_bottom"]["outer"] = self.offset_rectangle(self, offset=-(Lthickness-LTFoffsetX), outer_rect=output["lining"]["inner"]["inner_right_bottom"])

        # generate inner rectangle from outer rectangle using frame thickness 
        output["panels"]["frame_right_bottom"]["inner"] = self.offset_rectangle(self, offset=FRightBThickness, outer_rect=output["panels"]["frame_right_bottom"]["outer"])

        return output 

    @classmethod
    def triple_panel_right():
        pass

    @classmethod
    def triple_panel_top():
        pass

    @classmethod
    def triple_panel_vertical():
        pass

    @classmethod
    def userdefined():
        pass

    @classmethod
    def undefined():
        pass