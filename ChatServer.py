import atexit
import logging
import os
import os.path
import socket
import subprocess
import threading
import time
import uuid
from datetime import datetime
from DataConvertHelper import *
from MainGUI import *
from MessageClass import *

flag_if_already_send = False


class ServerChat:
    """
    The Class building the whole Server gui procedure the server methods.
    
    Attributes
    ----------
    textData: str
    The data was written into log server.
    RestoreTextButton: button
    Restore the text into the log server.
    ClearTextButton : button
    Clear the text into the log server.
    RunClientButton : button
    run client button from server.
    server: server type
    Server that we define.
    ConnectionsArea: List box.
    list box of the connections' client.
    LogArea: Text Area
    Thext area of the server
    clientsList: List.
    List of Clients
    ConnectionsList: List.
    List of connections client.
    
    Methods
    -------
    MainServerScreen(self)
    LogsArea(self)
    ServerConnectionsArea(self)
    ServerButtons(self)
    ClearText(self)
    RestoreText(self)
    RunClientFromServer()
    InsertLogsToTextArea(self, message)
    UsersUpdateScreen(self)
    broadcast(self, current_client, message)
    UpdateUsers(self, client)
    ChoosingClientToSendMessage(self, message)
    LogOutFromServer(self, client)
    ClientConnection(self, client, data, message)
    ApproveClientConnection(client, command)
    AddClientToConnectionsList(self, client)
    InsertLogsToServerArea(self, client, MessageOptions, recipient=None)
    handle(self, client, threadId)
    receive(self)
    CloseServer(self)
    run(self)
    """

    def __init__(self):

        self.LogOutBySelect = None
        self.UserToSend = None
        self.subClient = None
        self.subProcess = None
        self.textData = None
        self.RestoreTextButton = None
        self.ClearTextButton = None
        self.RunClientButton = None
        self.server = None
        self.ConnectionsArea = None
        self.LogArea = None
        self.clientsList = []
        self.ConnectionsList = []

        self.GUIServer = GUIHelper()
        self.window = self.GUIServer.ServerChatWindow(self, self.CloseServer)
        self.MainServerScreen()

    # Create the file. If it already exists (the server is already running), then
    # this fails and the program stops here.
    lock = open('chatserver.lock', 'x')
    lock.close()

    """ The function remove the lock, to check if server is running before we running client..
        :param: the function not getting any parameters.
        :returns: the function do not return any value.
    """

    # Function to delete the lock.
    @staticmethod
    def removeLock():
        os.remove('chatserver.lock')

    atexit.register(removeLock)

    """ The function building The Server GUI with MainGUI.py.
    :param self: the function get self as a parameter
    :returns: the function do not return any value.
    """

    def MainServerScreen(self):
        self.LogsArea()
        self.ServerConnectionsArea()
        self.ServerButtons()

    """ The function building The Server GUI log area and its attributes.
     :param self: the function get self as a parameter
     :returns: the function do not return any value.
    """

    def LogsArea(self):
        self.LogArea = self.GUIServer.ServerLog(self.window, 'Server Logs', height=28)

    """ The function building The Server GUI clients connections area and its attributes.
      :param self: the function get self as a parameter
      :returns: the function do not return any value.
    """

    def ServerConnectionsArea(self):
        self.ConnectionsArea = self.GUIServer.ServerConnectionArea(self.window, 'Connected Users')

    """ The function building The Server GUI buttons.
       :param self: the function get self as a parameter
       :returns: the function do not return any value.
    """

    def ServerButtons(self):
        actions = self.GUIServer.ServerButtonsGUI(self.window, self.RunClientFromServer, self.ClearText,
                                                  self.RestoreText)
        self.RunClientButton, self.ClearTextButton, self.RestoreTextButton = actions

    """ The function clear the server log text area.
       :param self: the function get self as a parameter
       :returns: the function do not return any value.
    """

    def ClearText(self):
        self.GUIServer.ClearTextGUI(self.LogArea)

    """ The function restore the data that we clear from the log server.
       :param self: the function get self as a parameter
       :returns: the function do not return any value.
    """

    def RestoreText(self):
        self.GUIServer.RestoreText(self.LogArea)

    """ The function give us the option to run a client from the server.
        :param: the function not getting any parameters.
        :returns: the function do not return any value.
    """

    def RunClientFromServer(self):
        self.subClient = subprocess.Popen(['ChatClient.py'], shell=True, creationflags=subprocess.SW_HIDE)

    """ The function insert data to the server text area.
       :param self: the function get self as a parameter
       :param message: message to write in the server log
       :type message: str
       :returns: the function do not return any value.
    """

    def InsertLogsToTextArea(self, message):
        self.GUIServer.LogsInsertToTextArea(self.LogArea, message)

    """ The function updates the users connections area and 
        can also counting number of valid connections.
       :param self: the function get self as a parameter
       :returns: the function do not return any value.
    """

    def UsersUpdateScreen(self):
        self.ConnectionsArea.delete(0, END)
        NickNamesCounter = 0
        for NickNameConnection in self.ConnectionsList:
            self.ConnectionsArea.insert(NickNamesCounter, NickNameConnection)
            NickNamesCounter += 1

    """ The function dealing with different types of sending option, 
    broadcast, group of clients or only one client 
    :param self: the function get self as a parameter
    :param message: message to send
    :type message: str
    :param TalkingCurrentClient: client that's wanna talk with all clients or specific one. 
    :type TalkingCurrentClient: client 
    :returns: the function do not return any value.
    """

    def SendingMessageManager(self, TalkingCurrentClient, message, recipient):
        global flag_if_already_send
        if recipient is not None:
            index = self.ConnectionsList.index(recipient)
            recipient_socket = self.clientsList[index]
            if not flag_if_already_send:
                SerializedDataToBytes(TalkingCurrentClient, message)
                flag_if_already_send = True

            if recipient_socket is not None:
                if TalkingCurrentClient != recipient_socket:
                    SerializedDataToBytes(recipient_socket, message)
        else:
            for client in self.clientsList:
                if client != TalkingCurrentClient:
                    SerializedDataToBytes(client, message)
                else:
                    SerializedDataToBytes(client, message)

    """ The function doing the update users procedure. 
    :param self: the function get self as a parameter
    :param client: client that's connected to the server.
    :type client: client
    :returns: the function do not return any value.
    """

    def UpdateUsers(self, client):
        time.sleep(.1)
        message = MessageAndClientData()
        message.command = 'UPDATE_USERS'
        message.message = '$$$'.join(self.ConnectionsList)
        self.SendingMessageManager(client, message, None)
        message.command = None

    """ The function doing the choosing specific client sending user procedure. 
    :param self: the function get self as a parameter
    :param message: message to send
    :type message: str
    :returns: the function return the client that's we wanna send the message else None
    """

    def ChoosingClientToSendMessage(self, message):
        if message.recipient is not None and message.recipient != 'None':
            # if message.recipient is not isinstance(message.recipient, list):
            index = self.ConnectionsList.index(message.recipient)
            ClientThatWhomMessage = self.clientsList[index]
            if ClientThatWhomMessage:
                return ClientThatWhomMessage
        return None

    """ The function doing the logout procedure from server. 
    :param self: the function get self as a parameter
    :param client: client that's connected to the server.
    :type client: client
    :returns: the function do not return any value.
    """

    def LogOutFromServer(self, client):
        try:
            index = self.clientsList.index(client)
            ConnectionToLogOut = self.ConnectionsList[index]
            self.InsertLogsToServerArea(client, 'Logout')
            self.clientsList.remove(client)
            self.ConnectionsList.remove(ConnectionToLogOut)
            self.UpdateUsers(client)
            self.UsersUpdateScreen()
        finally:
            client.close()

    """ The function manage the client connections procedure. 
    :param self: the function get self as a parameter
    :param client: client that's connected to the server.
    :type client: client
    :param data: whole information about whole process of sending message 
    :type data: MessageClass
    :returns: the function do not return any value.
    """

    def ClientConnection(self, client, data, message):
        if data.user in self.ConnectionsList:
            self.ApproveClientConnection(client, 'LOGIN_INVALID')
        else:
            self.ConnectionsList.append(data.user)
            self.clientsList.append(client)
            self.ApproveClientConnection(client, 'LOGIN_VALID')
            self.UpdateUsers(client)
            self.UsersUpdateScreen()
            self.InsertLogsToServerArea(client, 'Login')

    """ The function approved connections to the server. 
    :param self: the function get self as a parameter
    :param client: client that's wanna connected to the server.
    :type client: client
    :param StateOfClient: state of client while try to connect to the server.
    :type StateOfClient: str
    :returns: the function do not return any value.
    """

    @staticmethod
    def ApproveClientConnection(client, StateOfClient):
        message = MessageAndClientData()
        message.command = StateOfClient
        SerializedDataToBytes(client, message)
        message.command = None

    """ The function add client connections to the list. 
    :param self: the function get self as a parameter
    :param client: client that's wanna connected to the server.
    :type client: client
    :returns: the function do not return any value.
    """

    def AddClientToConnectionsList(self, client):
        index = self.clientsList.index(client)
        return self.ConnectionsList[index]

    """ The function add client connections to the list. 
    :param self: the function get self as a parameter
    :param client: client that's wanna connected to the server.
    :type client: client
    :param MessageOptions: Message options, log,logout etc....
    :type MessageOptions: str
    :returns: the function do not return any value.
    """

    def InsertLogsToServerArea(self, client, MessageOptions, recipient=None):
        CurrentTime = datetime.now().strftime('%H:%M:%S')
        ClientIP = client.getsockname()[0]
        ClientNickName = self.AddClientToConnectionsList(client)
        if recipient is None:
            TextToServerLog = f'{"[" + CurrentTime + "]"} - {ClientNickName + ":"}\n{MessageOptions}'
        else:
            # ClientIPThatWhomMessage = recipient.getsockname()[0]
            # NickNameWhomMessage = self.AddClientToConnectionsList(recipient)
            TextToServerLog = f'{"[" + CurrentTime + "]"} -  {ClientNickName} To {recipient}:\n{MessageOptions}'

        logging.basicConfig(filename='ChatLogs.log', filemode='w', format='%(message)s')
        logging.warning(TextToServerLog)
        self.InsertLogsToTextArea(TextToServerLog)

    """  The function handle all the clients are connected to the server and helping manage the sending/receive process. 
    :param self: the function get self as a parameter
    :param client: client that's wanna connected to the server.
    :type client: client
    :param threadId: Thread id
    :type threadId: int
    :returns: the function do not return any value. 
    """

    def handle(self, client, threadId):
        global flag_if_already_send
        while True:
            message = MessageAndClientData()
            try:
                DataBytes = client.recv(1024)
                if DataBytes:
                    try:
                        data = DeSerializedBytesToData(client, DataBytes)
                        if data.command == 'LOGIN':
                            self.ClientConnection(client, data, message)
                        elif data.command == 'LOGOUT':
                            message = MessageAndClientData()
                            message.command = 'LOGOUT_DONE'
                            SerializedDataToBytes(client, message)
                            message.command = None
                            time.sleep(.1)
                            self.LogOutFromServer(client)
                            break
                        elif data.command == 'MESSAGE':
                            flag_if_already_send = False
                            if data.recipient is not None and isinstance(data.recipient, list):
                                for UserToSend in data.recipient:
                                    self.InsertLogsToServerArea(client, f'Message: {data.message}', UserToSend)
                                    self.SendingMessageManager(client, data, UserToSend)
                            else:
                                self.InsertLogsToServerArea(client, f'Message: {data.message}', data.recipient)
                                self.SendingMessageManager(client, data, data.recipient)
                        else:
                            self.InsertLogsToServerArea(client, f'Message: {data.message}',
                                                        self.ChoosingClientToSendMessage(data))
                            self.SendingMessageManager(client, data, None)
                    except():
                        try:
                            pass
                        except Exception as e:
                            pass
                else:
                    self.LogOutFromServer(client)
                    break
            except Exception as e:
                self.LogOutFromServer(client)
                break

    """  The function dealing with the receiving process messages from clients/server
    :param self: the function get self as a parameter
    :returns: the function do not return any value.
    """

    def receive(self):
        while True:
            message = MessageAndClientData()
            client, address = self.server.accept()
            data = DeSerializedBytesToData(client)
            self.ClientConnection(client, data, message)
            threadId = str(uuid.uuid4())
            threading.Thread(target=self.handle, args=(client, threadId)).start()

    """ The function Closing the process via os._exit and destroy the window.
       :param self: the function get self as a parameter
       :returns: the function do not return any value.
    """

    def CloseServer(self):
        self.removeLock()
        os._exit(0)
        self.window.destroy()

    """ The function define the server and putting the server on listen mode to listen
        for new clients, then starting threads to manage the messages receiving and sending process.
       :param self: the function get self as a parameter
       :returns: the function do not return any value.
    """

    def run(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('127.0.0.1', 9092))
        self.server.listen()
        threading.Thread(target=self.receive).start()
        self.window.mainloop()

    atexit.register(removeLock)


ServerChat().run()
