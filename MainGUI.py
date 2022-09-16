import tkinter
from tkinter import *


class GUIHelper:
    """
          The Class building the whole Client and Server GUI

    Methods
    -------

     ServerChatWindow(self, CloseServer)
     ServerLog(window, title, height=10)
     ServerConnectionArea(window, title)
     ServerButtonsGUI(window, run, clear, restore)
     ClearTextGUI(TextArea)
     RestoreText(TextArea)
     LogsInsertToTextArea(TextArea, message)
     ClientChatWindow(closeClient)
     ClientMessageArea(window, title, height=23)
     ClientConnectionsArea(window, title, height=18)
     EntryAreaClient(window, title)
     ClientButtonsGUI(window, SendOption, LogoutOption, LoginAction)
     LoginWindow(window, title, OpenWindow, CloseWindow)
     LoginWindowBuild(ClientWindowConnect, title, LoginProcedure)
     NickNameLabel(window)
     ChangeButtonStatesToEnable(ButtonsClientList)
     ChangeButtonStatesToDisable(ButtonsClientList)

    """
    def __init__(self):
        pass

    ####################################################
    # Server GUI #
    ####################################################

    """ The function building The Server GUI main Window.
       :param self: the function get self as a parameter
       :param CloseServer: Manage closing server window.  
       :type CloseServer: function 
       :returns: the function return the server window. 
    """

    @staticmethod
    def ServerChatWindow(self, CloseServer):
        # Main Window
        self.ServerChatWindow = Tk()
        self.ServerChatWindow.title('---ITalk---')
        self.ServerChatWindow.geometry('700x600')
        self.backGroundImage = PhotoImage(file="Pictures/MainBG.png")
        self.BackGroundLabel = Label(self.ServerChatWindow, image=self.backGroundImage)
        self.BackGroundLabel.place(x=0, y=0)
        # Main Window Title
        Title = Label(self.ServerChatWindow, text="Welcome To Server Management")
        Title.config(font=("Courier", 25))
        Title.place(relx=0.5, rely=0.05, anchor="center")
        self.ServerChatWindow.attributes('-topmost', True)
        self.ServerChatWindow.protocol('WM_DELETE_WINDOW', CloseServer)
        return self.ServerChatWindow

    """ The function building The Server log area.
       :param window: the function get tkinter window of the server.
       :type window: tkinter object
       :param title: Server log title.  
       :type title: str 
       :param height: height of server log text area.
       :param type: int 
       :returns: the function return the server log text area. 
    """

    @staticmethod
    def ServerLog(window, title, height=10):
        Title = Label(window, text="Server Logs")
        Title.config(font=("Courier", 15))
        Title.place(relx=0.25, rely=0.18, anchor="center")
        ServerLogTextArea = Text(window, height=height, width=45, background='#FFFAFA',
                                 font=('Courier', 10))
        ServerLogTextArea.configure(state='disabled')
        ServerLogTextArea.place(relx=0.26, rely=0.6, anchor="center")
        return ServerLogTextArea

    """ The function building Server connections area.
       :param window: the function get tkinter window of the server.
       :type window: tkinter object
       :param title: connections title.  
       :type title: str 
       :returns: the function return listbox of connections. 
    """

    @staticmethod
    def ServerConnectionArea(window, title):
        Title = Label(window, text=title)
        Title.config(font=("Courier", 15))
        Title.place(relx=0.65, rely=0.18, anchor="center")
        ListBoxOfConnections = Listbox(window, height=20, width=15, background='#FFFAFA',
                                       font=("Courier", 14))
        ListBoxOfConnections.place(relx=0.65, rely=0.59, anchor="center")
        return ListBoxOfConnections

    """ The function building Server gui buttons.
       :param window: the function get tkinter window of the server.
       :type window: tkinter object
       :param run: running client from server.  
       :type run: function
       :param clear: clear the server log area.  
       :type clear: function
       :param clear: restore the server log data.  
       :type clear: function
       :returns: the function return list of the server buttons attributes. 
    """

    @staticmethod
    def ServerButtonsGUI(window, run, clear, restore):
        RunClientButton = Button(window, text='Run Client', width=10, command=run, background='#FF0000',
                                 font=('Courier', 12), fg='black', cursor='hand2')
        RunClientButton.place(relx=0.9, rely=0.2, anchor="center")

        ClearText = Button(window, text='Clear', width=10, command=clear, background='#FF0000',
                           font=('Courier', 12), fg='black', cursor='hand2')
        ClearText.place(relx=0.9, rely=0.3, anchor="center")

        RestoreText = Button(window, text='Restore', width=10, command=restore, background='#FF0000',
                             font=('Courier', 12), fg='black', cursor='hand2')
        RestoreText.place(relx=0.9, rely=0.4, anchor="center")

        return [RestoreText, ClearText, RunClientButton]

    """ The function clear the server log area.
       :param TextArea: server text area.
       :type TextArea: tkinter object.
       :returns: the function return the text data. 
    """

    @staticmethod
    def ClearTextGUI(TextArea):
        global textData
        TextArea.configure(state='normal')
        textData = TextArea.get(1.0, "end-1c")
        TextArea.delete("1.0", END)
        TextArea.configure(state='disabled')
        return textData

    """ The function restore the server log data.
        :param TextArea: server text area.
        :type TextArea: tkinter object.
        :returns: the function do not return any value.
    """

    @staticmethod
    def RestoreText(TextArea):
        TextArea.configure(state='normal')
        TextArea.insert('end', textData)
        TextArea.configure(state='disabled')

    """ The function insert data to the server log.
        :param TextArea: server text area.
        :type TextArea: tkinter object.
        :param message: message to write into the log server.
        :type message: str
        :returns: the function do not return any value.
    """

    @staticmethod
    def LogsInsertToTextArea(TextArea, message):
        TextArea.configure(state='normal')
        TextArea.insert(INSERT, f'{message} \n')
        TextArea.see(END)
        TextArea.configure(state='disabled')

    ##########################################################
    # Client GUI #
    ##########################################################

    """ The function building The Client GUI main Window.
       :param self: the function get self as a parameter
       :returns: the function return the Client window. 
    """

    @staticmethod
    def ClientChatWindow(closeClient):
        # Main Window
        ClientChatWindow = Tk()
        ClientChatWindow.title('---ITalk---')
        ClientChatWindow.geometry('410x700')
        ClientChatWindow.configure(background='#12273A', pady=30)
        # Main Window Title
        Title = Label(ClientChatWindow, text="Lets Talk:")
        Title.config(font=("Courier", 20))
        Title.place(relx=0.3, rely=0.001, anchor="center")
        ClientChatWindow.attributes('-topmost', True)
        ClientChatWindow.protocol('WM_DELETE_WINDOW', closeClient)
        return ClientChatWindow

    """ The function building The client log text area.
       :param window: the function get tkinter window of the server.
       :type window: tkinter object
       :param title: Client log title.  
       :type title: str 
       :param height: height of client log text area.
       :param type: int 
       :returns: the function return the client log text area. 
    """

    @staticmethod
    def ClientMessageArea(window, title, height=23):
        textAreaClient = Text(window, height=height, width=35, background='#FFFAFA', font=("Courier", 10))
        textAreaClient.configure(state='disabled')
        textAreaClient.place(relx=0.35, rely=0.40, anchor="center")
        return textAreaClient

    """ The function building Client connections area.
        :param window: the function get tkinter window of the Client.
        :type window: tkinter object
        :param title: connections title.  
        :type title: str 
        :param height: height of client log text area.
        :param type: int 
        :returns: the function return listbox of connections. 
     """

    @staticmethod
    def ClientConnectionsArea(window, title, height=18):
        Title = Label(window, text=title)
        Title.config(font=("Courier", 8))
        Title.place(relx=0.8, rely=0.07, anchor="center")
        ClientConnections = Listbox(window, height=height, width=10, background='#FFFAFA', font=("Courier", 14),
                                    selectmode="multiple")
        ClientConnections.place(relx=0.85, rely=0.41, anchor="center")
        return ClientConnections

    """ The function building The Client entry area.
       :param window: the function get tkinter window of the Client.
       :type window: tkinter object
       :param title: Client log title.  
       :type title: str 
       :returns: the function return the Client entry area.
    """

    @staticmethod
    def EntryAreaClient(window, title):
        Title = Label(window, text=title)
        Title.config(font=("Courier", 10))
        Title.place(relx=0.25, rely=0.73, anchor="center")
        # ClientEntry = Entry(window, width=60, font=("Courier", 10))
        # ClientEntry.place(relx=0.44, rely=0.82, anchor="center", width=350, height=50)
        ClientEntry = Text(window, width=60, font=("Courier", 10))
        ClientEntry.config(state=tkinter.NORMAL)
        ClientEntry.place(relx=0.44, rely=0.82, anchor="center", width=350, height=50)
        ScrollbarText = Scrollbar(ClientEntry, orient='vertical')
        ScrollbarText.pack(side=RIGHT, fill=Y)
        ScrollbarText.config(command=ClientEntry.yview)
        # ClientEntry['yscroll'] = ScrollbarText.set
        # ScrollbarText.place(relx=0.87, rely=0.78)
        return ClientEntry

    """ The function building Client gui buttons.
       :param window: the function get tkinter window of the client.
       :type window: tkinter object
       :param sendOption: doing the sending procedure.
       :type sendOption: function
       :param LogoutOption: doing the logout procedure.
       :type LogoutOption: function
       :param LoginAction: doing the loging procedure. 
       :type LoginAction: function
       :returns: the function return list of the client buttons attributes. 
    """

    @staticmethod
    def ClientButtonsGUI(window, SendOption, LogoutOption, LoginAction):
        JoinUsButton = Button(window, text='Join us!', width=10, command=LoginAction, background='#00FF00',
                              font=('Courier', 12), fg='black', cursor='hand2')
        JoinUsButton.place(relx=0.13, rely=0.07, anchor="center")

        SendButton = Button(window, text='Send', width=10, command=SendOption, background='#FF0000',
                            font=('Courier', 12), fg='black', cursor='hand2')
        SendButton.place(relx=0.13, rely=0.90, anchor="center")

        LogoutButton = Button(window, text='Logout', width=10, command=LogoutOption, background='#FF0000',
                              font=('Courier', 12), fg='black', cursor='hand2')
        LogoutButton.place(relx=0.85, rely=0.75, anchor="center")

        return [SendButton, LogoutButton, JoinUsButton]

    """ The function building the main client login window
       :param window: the function get tkinter window of the client.
       :type window: tkinter object
       :param title: ---Italk--- title.  
       :type title: str 
       :param OpenWindow: doing the open window client procedure.
       :type OpenWindow: function
       :param CloseWindow: doing the close window client procedure. 
       :type  CloseWindow: function
       :returns: the function return the enter nick name window.
    """

    @staticmethod
    def LoginWindow(window, title, OpenWindow, CloseWindow):
        EnterNickNameWindow = Tk()
        EnterNickNameWindow.configure(background='#12273A', pady=100, padx=150)
        EnterNickNameWindow.title(title)
        EnterNickNameWindow.protocol('WM_DELETE_WINDOW', CloseWindow)
        EnterNickNameWindow.attributes('-topmost', True)
        OpenWindow(EnterNickNameWindow)
        return EnterNickNameWindow

    """ The function building the client login window gui design. 
       :param ClientWindowConnect: the function get tkinter window of the client connection.
       :type ClientWindowConnect: tkinter object
       :param title: Client Enter nick name title. 
       :type title: str 
       :param LoginProcedure: doing the login client procedure.
       :type LoginProcedure: function
       :returns: the function return list of login window build and his attributes. 
    """

    @staticmethod
    def LoginWindowBuild(ClientWindowConnect, title, LoginProcedure):
        EnterNickNameTitle = Label(ClientWindowConnect, text=title, fg='black', font=('Courier', 15))
        EnterNickNameTitle.grid(row=0, column=0)
        EnterNickNameEntry = Entry(ClientWindowConnect, width=30, background='#FFFAFA', font=('Courier', 14))
        EnterNickNameEntry.grid(row=1, column=0, sticky='we', padx=10, ipady=6, pady=10)
        EnterNickNameButton = Button(ClientWindowConnect, text='Lets Talk!', width=10, command=LoginProcedure,
                                     background='#FF0000',
                                     font=('Courier', 12), fg='black', cursor='hand2')
        EnterNickNameButton.grid(row=1, column=1, sticky='we', padx=10, ipady=6, pady=10)
        ErrorEnterNickName = Label(ClientWindowConnect, text='', fg='#ef233c', background='#2b2d42',
                                   font=('Courier', 12))
        return [EnterNickNameEntry, EnterNickNameButton, ErrorEnterNickName]

    """ The function building the nickname label.
          :param TextArea: server text area.
          :type TextArea: tkinter object.
          :returns: the function do not return any value.
      """

    @staticmethod
    def NickNameLabel(window):
        NickNameLabelClient = Label(window, text='', fg='black', font=('Courier', 12), padx=30)
        NickNameLabelClient.place(relx=0.7, rely=0.001, anchor="center")
        return NickNameLabelClient

    """ The function change the client buttons state to enable mode.
       :param ButtonsClientList: List of client Buttons.
       :type: List       
       :returns: the function do not return any value.
    """

    @staticmethod
    def ChangeButtonStatesToEnable(ButtonsClientList):
        ButtonsClientList.SendButton['state'] = NORMAL
        ButtonsClientList.JoinUsButton['state'] = DISABLED
        ButtonsClientList.LogoutButton['state'] = NORMAL

    """ The function change the client buttons state to disable mode.
       :param ButtonsClientList: List of client Buttons.
       :type: List       
       :returns: the function do not return any value.
    """

    @staticmethod
    def ChangeButtonStatesToDisable(ButtonsClientList):
        ButtonsClientList.SendButton['state'] = DISABLED
        ButtonsClientList.JoinUsButton['state'] = NORMAL
        ButtonsClientList.LogoutButton['state'] = DISABLED
