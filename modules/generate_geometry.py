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

        # generate rectangle using overall height and width
        output["lining"]["outer"] = self.rectangle(OverallWidth, OverallHeight)

        # generate inner rectangle from outer rectangle using lining thickness 
        output["lining"]["inner"] = self.offset_rectangle(self, offset=LiningProps["LiningThickness"], outer_rect=output["lining"]["outer"])

        # generates outer rectangle for frame given the offset from the lining
        output["panels"]["frame"]["outer"] = self.offset_rectangle(self, offset=LiningProps["LiningToPanelOffsetX"], outer_rect=output["lining"]["outer"])

        # generate inner rectangle from outer rectangle using frame thickness 
        output["panels"]["frame"]["inner"] = self.offset_rectangle(self, offset=PanelProps["FrameThickness"], outer_rect=output["panels"]["frame"]["outer"])

        return output

    # ===================================================
    # TODO: create functions for remaining window types
    # ===================================================
    @classmethod
    def double_panel_horizontal():
        pass

    @classmethod
    def double_panel_vertical():
        pass

    @classmethod
    def triple_panel_bottom():
        pass

    @classmethod
    def triple_panel_horizontal():
        pass

    @classmethod
    def triple_panel_left():
        pass

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