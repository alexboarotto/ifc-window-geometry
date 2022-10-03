
import numpy


class get_props:
    def get_lining_props(
        LiningThickness = 10,
        LiningDepth = 10,
        LiningOffset = 0,
        LiningToPanelOffsetX = 0,
        LiningToPanelOffsetY = 0,
        MullionThickness = 0,
        FirstMullionOffset = 0,
        SecondMullionOffset = 0,
        TransomThickness = 0,
        FirstTransomOffset = 0,
        SecondTransomOffset = 0):
        return {
            "LiningThickness": LiningThickness,
            "LiningOffset": LiningOffset,
            "LiningDepth": LiningDepth,
            "LiningToPanelOffsetX": LiningToPanelOffsetX,
            "LiningToPanelOffsetY": LiningToPanelOffsetY,
            "MullionThickness": MullionThickness,
            "FirstMullionOffset": FirstMullionOffset,
            "SecondMullionOffset": SecondMullionOffset,
            "TransomThickness": TransomThickness,
            "FirstTransomOffset": FirstTransomOffset,
            "SecondTransomOffset": SecondTransomOffset
        }

    def get_panel_props(PanelPosition = numpy.array([0,0,0]), FrameDepth = 10, FrameThickness = 10):
        return {
            "PanelPosition": PanelPosition,
            "FrameDepth": FrameDepth,
            "FrameThickness": FrameThickness,
        }