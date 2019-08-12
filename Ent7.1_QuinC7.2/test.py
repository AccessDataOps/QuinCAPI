import os

ProjectDataPath = "C:/WIN-B3VKJBVM6RQ/AccessData/ProjectData"

ProjectDataPath = os.path.normpath(ProjectDataPath)
print(ProjectDataPath.startswith(r'\\'))