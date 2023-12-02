

var openChatBtn = document.getElementsByClassName("open-chat-btn");
var chatPopup = document.getElementById("chat-popup");



    var closeChatBtn = document.getElementById("close-chat-btn");

    // When the user clicks the close button, close the chat popup
    closeChatBtn.onclick = function() {

        chatPopup.style.display = "none";
        chatSocket.close();

    }

// var onoff = document.getElementById("user-onoff");

var userList = document.getElementById('user-list').children;        
const user = JSON.parse(document.getElementById('username').textContent);
const roomName = JSON.parse(document.getElementById('id').textContent);
                const chatSocket = new WebSocket(
                    'ws://'
                    + window.location.host
                    + '/ws/'
                    + roomName
                    + '/'
                );

                chatSocket.onmessage = function(e) {
                    const data = JSON.parse(e.data);
                    console.log(data.message)
                    const chatLog = document.querySelector('#chat-log');
                    const onoff = document.getElementById("user-onoff");
                    // const chat = document.querySelector('#chat-message-input');

                    if (data.message !=undefined){
                        console.log(data.message);                 
                        const msge = document.createElement('p');
                        msge.innerText = data.message;
                        if (data.css_class === "current-user") {
                            msge.style.textAlign = 'right';
                            msge.style.color = 'blue';
                        } else {
                            msge.style.textAlign = 'left';
                            msge.style.color = 'red';

                          
                        }
                    chatLog.appendChild(msge);
                   
                    }
                    if(data.is_online !=undefined){
                        console.log(data.username);  
                        console.log(user);  
                        
                        if (data.username != user){
                            console.log(data.username);  
                            if (data.is_online) {
                                onoff.innerHTML = 'online';
                                onoff.style.color = 'rgb(7, 74, 7)';
                            } else {
                                console.log('userrr')
                                console.log(data.is_online);
                                onoff.innerHTML = 'offline';
                                onoff.style.color = 'rgb(108, 2, 2)';
                            } 
                        }
                    }  
                    
                };
                chatSocket.onopen = function(e){
                    console.log("CONNECTION ESTABLISHED");
                }
                
                chatSocket.onerror = function(e){
                    console.log("ERROR OCCURED");
                }   
                chatSocket.onclose = function(e) {
                    console.error('Chat socket closed unexpectedly');
                };
                window.addEventListener('beforeunload', function () {
                    chatSocket.close();
                });

                
                
                
                
                

                document.querySelector('#chat-message-input').focus();

                document.querySelector('#chat-message-input').addEventListener('keyup', function(e) {
                    if (e.keyCode === 13) {  
                        document.querySelector('#chat-message-submit').click();
                    }
                });

                document.querySelector('#chat-message-submit').addEventListener('click', function(e) {
                    const messageInputDom = document.querySelector('#chat-message-input');
                    const message = messageInputDom.value;
                    chatSocket.send(JSON.stringify({
                        'message': message
                    }));
                    messageInputDom.value = '';
                });
                