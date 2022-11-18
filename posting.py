
class Posting():
    def __init__(self,doc_id,tfs):
        self.doc_id=doc_id
        self.tfs=tfs

    def __str__(self):
        return f"[{self.doc_id},{self.tfs}]"
        
    def __repr__(self):
        return f"Posting({self.doc_id},{self.tfs})"