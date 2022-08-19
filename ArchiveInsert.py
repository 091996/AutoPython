import IDNumDef
from ArchiveSelect import FindArchive
from Login import login

headers = login()
history = 1
ID = 0


while history == 1:
    ID = IDNumDef.IdBuild()
    history = FindArchive(headers, ID)

print(ID)




