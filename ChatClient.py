import errno
import os
import os.path
import socket
import threading
from DataConvertHelper import *
from MainGUI import *
from MessageClass import *

script_name = 'ChatServer.py'


class Client:
    """
      The Class building the whole Client gui procedure the server methods.

      Attributes
      ----------
      LabelForNickName: Label.
      label that's represent the nickname.
      ListOfUsers: List.
      list of all users connected.
      SendButton: Button.
      Button of send.
      LogoutButton: Button.
      Logout button.
      JoinUsButton: Button.
      join to the chat button.
      client: client.
      client.
      NickNameError: str
      error while problem occurs while trying to sign in.
      NickNameButton: Button
      nickname enter button.
      NickNameEntry: Entry
      nickname entry
      enterNickName: window (tkinter object)
      nickname window.
      entryAreaClient: entry
      Client Area entry.
      ConnectionsArea: listbox.
      listbox of connections users.
      MessageArea: Text
      Client text area (For Messages)

      Methods
      -------
      MainChatScreen(self)
       ClientMessageArea(self)
       ClientConnectionsArea(self)
       EntryAreaClient(self)
       NickNameLabelClient(self)
       ClientButtons(self)
       EnterNickName(self)
       OpenWindow(self, LoginWindow)
       MakeButtonWorkWhileConnect(self)
       MakeButtonDidntWorkWhileConnect(self)
       MakeButtonDidntWorkWhileConnect(self)
       Login(self)
       ClientConnection(self)
       ShowErrorNickName(self, message)
       InsertLogsToServerTextArea(self, message)
       UpdateConnectNickNames(self, message)
       ChoosingClientToSendMessage(self)
       Receive(self)
       CloseClient(self)
       SelfDisconnectedClient(self)
       CloseWindow(self)
       ResetGUIStates(self)
       runGUI(self)
      """

    def __init__(self):
        self.UserToSend = None
        self.User = None
        self.recipients = None
        self.LabelForNickName = None
        self.ListOfUsers = None
        self.SendButton = None
        self.LogoutButton = None
        self.JoinUsButton = None
        self.client = None
        self.NickNameError = None
        self.NickNameButton = None
        self.NickNameEntry = None
        self.enterNickName = None
        self.entryAreaClient = None
        self.ConnectionsArea = None
        self.MessageArea = None

        # #####################
        # self.index = 0
        # #####################

        self.GUIChat = GUIHelper()
        self.window = self.GUIChat.ClientChatWindow(self.CloseClient)
        self.MainChatScreen()
        self.message = MessageAndClientData()

    """ The function building The Client GUI with MainGUI.py.
    :param self: the function get self as a parameter
    :returns: the function do not return any value
    """

    def MainChatScreen(self):
        self.ClientMessageArea()
        self.ClientConnectionsArea()
        self.EntryAreaClient()
        self.NickNameLabelClient()
        self.ClientButtons()

    """ The function building The Client Message Area with MainGUI.py.
    :param self: the function get self as a parameter
    :returns: the function do not return any value
    """

    def ClientMessageArea(self):
        self.MessageArea = self.GUIChat.ClientMessageArea(self.window, 'Lets Talk!:')

    """ The function building The Client GUI clients connections area and its attributes.
      :param self: the function get self as a parameter
      :returns: the function do not return any value.
    """

    def ClientConnectionsArea(self):
        self.ConnectionsArea = self.GUIChat.ClientConnectionsArea(self.window, 'Who I wanna talk with?')

    """ The function building The Entry Area clients GUI.
       :param self: the function get self as a parameter
       :returns: the function do not return any value.
     """

    def EntryAreaClient(self):
        self.entryAreaClient = self.GUIChat.EntryAreaClient(self.window, 'Please Enter Message:')

    """ The function building The Nick name label Area in the client GUI.
       :param self: the function get self as a parameter
       :returns: the function do not return any value.
     """

    def NickNameLabelClient(self):
        self.LabelForNickName = self.GUIChat.NickNameLabel(self.window)

    """ The function building The Client GUI buttons.
       :param self: the function get self as a parameter
       :returns: the function do not return any value.
    """

    def ClientButtons(self):
        actions = self.GUIChat.ClientButtonsGUI(self.window, self.SendMessageToServer, self.SelfDisconnectedClient,
                                                self.EnterNickName)
        self.SendButton, self.LogoutButton, self.JoinUsButton = actions

    """ The function building the entry nick name for the client and popup window.
       :param self: the function get self as a parameter
       :returns: the function do not return any value.
    """

    def EnterNickName(self):
        self.enterNickName = self.GUIChat.LoginWindow(self.window, '---ITalk---', self.OpenWindow, self.CloseWindow)
        self.enterNickName.mainloop()

    """ The function building the client popup window.
       :param self: the function get self as a parameter
       :param loginWindow: Client login window
       :type: window
       :returns: the function do not return any value.
    """

    def OpenWindow(self, LoginWindow):
        self.NickNameEntry, self.NickNameButton, self.NickNameError = self.GUIChat.LoginWindowBuild(LoginWindow,
                                                                                                    'Hi you,Whats '
                                                                                                    'your name?',
                                                                                                    self.Login)
        self.JoinUsButton['state'] = DISABLED
        self.JoinUsButton['background'] = '#FF0000'

    """ The function change the connect button state to enable mode.
       :param self: the function get self as a parameter
       :returns: the function do not return any value.
    """

    def MakeButtonWorkWhileConnect(self):
        self.GUIChat.ChangeButtonStatesToEnable(self)

    """ The function change the connect button state to disable mode.
       :param self: the function get self as a parameter
       :returns: the function do not return any value.
    """

    def MakeButtonDidntWorkWhileConnect(self):
        self.GUIChat.ChangeButtonStatesToDisable(self)

    """ The function Manage the login process of new client.
       :param self: the function get self as a parameter
       :returns: the function do not return any value.
    """

    def Login(self):
        if not self.NickNameEntry.get():
            self.ShowErrorNickName("You have to enter nick name!")
        else:
            self.message.user = self.NickNameEntry.get()
            self.message.command = 'LOGIN'
            if not self.ClientConnection():
                self.ShowErrorNickName('There is no server Running!')
                self.CloseClient()
            else:
                self.LabelForNickName['text'] = self.message.user

    """ The function Manage the new connection process of new client to the server.
       :param self: the function get self as a parameter
       :returns: the function return true for successful connect, and false if that was Exception while errors. 
    """

    def ClientConnection(self):
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if self.client.connect_ex(('127.0.0.1', 9092)) == 0:
                SerializedDataToBytes(self.client, self.message)
                threading.Thread(target=self.Receive).start()
            else:
                SerializedDataToBytes(self.client, self.message)
            return True
        except Exception as e:
            return False

    """ The function Manage the nick name entry process. 
       :param self: the function get self as a parameter
       :param message: message for the client depends of the situation. 
       :type message: str
       :returns: the function do not return any value.
    """

    def ShowErrorNickName(self, message):
        self.NickNameError['text'] = message
        self.NickNameError.grid(row=2, column=0)

    """ The function insert data to the Client text area.
       :param self: the function get self as a parameter
       :param message: message to write in the client chat text area.
       :type message: str
       :returns: the function do not return any value.
    """

    def InsertLogsToClientTextArea(self, message):
        self.GUIChat.LogsInsertToTextArea(self.MessageArea, message)

    """ The function manage and update the connections Client Area. 
       :param self: the function get self as a parameter
       :param message: message to indication new user process. 
       :type message: str
       :returns: the function do not return any value.
    """

    def UpdateConnectNickNames(self, message):
        users = message.split('$$$')
        self.ListOfUsers = []
        self.ConnectionsArea.delete(0, END)
        self.ConnectionsArea.insert(0, 'All Users')
        NumberOfConnections = 1
        for UserConnection in users:
            # if UserConnection != self.message.user:
            self.ConnectionsArea.insert(NumberOfConnections, UserConnection)
            self.ListOfUsers.append(UserConnection)
            NumberOfConnections = NumberOfConnections + 1
        self.ConnectionsArea.select_set(0)

    """ The function Manage the sending message to specific client. 
       :param self: the function get self as a parameter
       :returns: the function do not return any value.
    """

    def ChoosingClientToSendMessage(self):
        selected = self.ConnectionsArea.curselection()
        if len(selected) == 1:
            if selected and selected[0] != 0:
                self.message.recipient = self.ListOfUsers[selected[0] - 1]
            else:
                self.message.recipient = None
        elif len(selected) > 1:
            ###########################
            if selected[0] == 0:
                self.message.recipient = None
            else:
                ###########################
                listOfUsersToSendMessage = []
                for selectUser in selected:
                    listOfUsersToSendMessage.append(self.ListOfUsers[selectUser - 1])
                self.message.recipient = listOfUsersToSendMessage

    def SendMessageToServer(self):
        textToSend = self.entryAreaClient.get(1.0, 'end-1c')
        if textToSend:
            self.ChoosingClientToSendMessage()
            self.message.message = textToSend
            self.message.command = 'MESSAGE'
            SerializedDataToBytes(self.client, self.message)
            self.message.command = None
            self.entryAreaClient.delete(1.0, 'end-1c')
            self.entryAreaClient.insert(1.0, '')

    """ The function manage the receiving and communication procedure between the client-server. 
       :param self: the function get self as a parameter
       :returns: the function do not return any value.
    """

    def Receive(self):
        while True:
            try:
                BytesDataReceive = self.client.recv(1024)
                if BytesDataReceive:
                    try:
                        DataObject = DeSerializedBytesToData(self.client, BytesDataReceive)
                        if DataObject.command == 'LOGIN_INVALID':
                            self.MakeButtonDidntWorkWhileConnect()
                            self.ShowErrorNickName('Nick Name already Exits, Please Choose Another name')

                        elif DataObject.command == 'LOGIN_VALID':
                            self.message.command = None
                            self.MakeButtonWorkWhileConnect()
                            self.enterNickName.destroy()

                        elif DataObject.command == 'UPDATE_USERS':
                            self.message.command = None
                            self.UpdateConnectNickNames(DataObject.message)

                        elif DataObject.command == 'MESSAGE':
                            self.InsertLogsToClientTextArea(f'{DataObject.user}: {DataObject.message}')

                        elif DataObject.command == 'LOGOUT_DONE':
                            self.ResetGUIStates()
                            self.client.close()
                            break
                    except():
                        pass
                else:
                    self.client.close()
                    break
            except Exception as e:
                self.CloseClient()
            except IOError as e:
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    self.CloseClient()
                continue
            except Exception as e:
                self.CloseClient()
                break

    """ The function manage the closing client procedure. 
       :param self: the function get self as a parameter
       :returns: the function do not return any value.
    """

    def CloseClient(self):
        os._exit(0)
        self.window.destroy()
        self.client.close()
        try:
            self.enterNickName.destroy()
        except Exception as e:
            pass

    """ The function manage the disconnected client procedure from the client window. 
       :param self: the function get self as a parameter
       :returns: the function do not return any value.
    """

    def SelfDisconnectedClient(self):
        self.message.command = 'LOGOUT'
        SerializedDataToBytes(self.client, self.message)
        self.message.command = None

    """ The function closing window while enter nick name aND change 'join us' button state. 
        :param self: the function get self as a parameter
        :returns: the function do not return any value.
     """

    def CloseWindow(self):
        self.enterNickName.destroy()
        self.JoinUsButton['state'] = NORMAL
        self.JoinUsButton['background'] = '#64a6bd'

    """ The function reset the gui states to default. 
        :param self: the function get self as a parameter
        :returns: the function do not return any value.
     """

    def ResetGUIStates(self):
        self.MakeButtonDidntWorkWhileConnect()
        self.LabelForNickName['text'] = ''
        self.ConnectionsArea.delete(0, END)
        self.MessageArea.configure(state='normal')
        self.MessageArea.delete('1.0', END)
        self.MessageArea.configure(state='disabled')

    """ The function run the main GUI loop. 
        :param self: the function get self as a parameter
        :returns: the function do not return any value.
     """

    def runGUI(self):
        self.window.mainloop()


if os.path.exists('chatserver.lock'):
    Client().runGUI()
else:
    print('Server is not running - You cant run Client without Server')
