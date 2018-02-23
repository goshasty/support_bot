class Subcategory:
    name = ""
    mainID = 0
    ID = 0
    def __init__(self, text, mainID, selfID):
        self.mainID = mainID
        self.name = text
        self.ID = selfID
    def check_name(self, text):
        if(self.name==text):
            return True

    def check_mainID(self, id):
        if(self.mainID==id):
            return True
    def get_name(self):
        return self.name
    def get_id(self):
        return self.ID
