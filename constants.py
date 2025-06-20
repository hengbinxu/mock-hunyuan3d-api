from enum import StrEnum


class SupportFileFormat(StrEnum):
    GLB = "glb"
    OBJ = "obj"
    PLY = "ply"
    STL = "stl"


class ImageProcessStatus(StrEnum):
    COMPLETED = "completed"
    PROCESSING = "processing"
