class MessageAndClientData(object):
    """
       The Class building the whole Server gui procedure the server methods.

       Attributes
       ----------
       user: None
       message: None
       type : str
       recipient: None
       command : None

    """

    def __init__(self):
        self.user = None
        self.message = None
        self.type = 'text'
        self.recipient = None
        self.command = None
