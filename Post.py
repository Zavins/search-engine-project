class Post():
    def __init__(self,docid,tfs):
        self.docid=docid
        self.tfs=tfs

    def __str__(self):
        return f"[{self.docid},{self.tfs}]"