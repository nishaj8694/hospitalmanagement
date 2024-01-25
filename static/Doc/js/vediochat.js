let roomName=undefined;
let currentSocket;
let dataInfo;
const chatLog = document.querySelector('#chat-content');
const chat1 = document.querySelector('.chat1');
const chat2 = document.querySelector('.chat2');
const userProfile = document.getElementById('userData');
const userProfileData = JSON.parse(userProfile.textContent);

const chat2defaultnone = document.querySelector('.chat2defaultnone');
const chat2default = document.querySelector('.chat2default');

var videoBox = document.getElementById('video-Box');
var videoBox1 = document.getElementById('video-box-User');

var isDragging = false;
var offsetX, offsetY;
var initialWidth, initialHeight;

let vedioCheck=false
var serv='stun:stun.1.google.com:19302';
const config = {iceServers:[{urls:serv}] };
let peerConnection = new RTCPeerConnection(config)


window.addEventListener('load', function() {      
      
      if (window.innerWidth < 578) {
         if (!chat2.classList.contains('d-none') && chat1.classList.contains('d-none')){
      
         }
         else{
              chat2.classList.add('d-none');    
            }
      }
      else {
              chat1.classList.remove('d-none');
              chat2.classList.remove('d-none');
          }
  });


window.addEventListener('resize', function() {      
      if (window.innerWidth < 578) {
         if (!chat2.classList.contains('d-none') && chat1.classList.contains('d-none')){
      
         }
         else{
              chat2.classList.add('d-none');    
            }
      }
      else {
              chat1.classList.remove('d-none');
              chat2.classList.remove('d-none');
          }
  });

document.addEventListener('DOMContentLoaded',function(){
  const bt=document.querySelectorAll('.open-chat-btn');
  bt.forEach(function(a){
    a.addEventListener('click',function(){
      const id=a.dataset.userId;
      bt.forEach(function(a) {
          a.classList.remove('act');
      });
      openChat(id)
    })
  })
})


function openChat(id) {
  chat2defaultnone.classList.remove('d-none')
  chat2default.classList.add('d-none')
  if (window.innerWidth < 578) {
    chat1.classList.add('d-none');
    chat2.classList.remove('d-none');
  }

  if (currentSocket && currentSocket.readyState === WebSocket.OPEN) {
      while (chatLog.firstChild) {
           chatLog.removeChild(chatLog.firstChild);
      }
      currentSocket.close();
    }
    var roomName=id
    const socket = new WebSocket('ws://'+ window.location.host+ '/ws/'+ roomName + '/');

    socket.onopen = function (event) {
      // console.log(WebSocket connection opened for ${userId}:, event);
    };

    socket.onmessage = function(e) {
              const data = JSON.parse(e.data);
              const onoff = document.getElementById("profilename");
              const onimage = document.getElementById("profileimage");
              const onOnline = document.getElementById("profileonline");
              console.log(data)
              if (data.message !=undefined){
                  // console.log(data);                 
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
              if (data.username == userProfileData.username){ 
              if(data.profile !=undefined){
               
               onoff.innerHTML=data.profile      
             }
             if (data.images !=undefined){
              onimage.src=data.images 
             } 
             if (data.is_online ==true){
                onOnline.innerHTML='online'
             }
             if (data.is_online ==false){
                onOnline.innerHTML='offline'
             }
            }
            
            if (data.me_online !=undefined && data.username != userProfileData.username){ 
             if (data.me_online ==true){
                onOnline.innerHTML='online'
             }
             if (data.me_online ==false){
                onOnline.innerHTML='offline'
             }
            }
          
            if (data.icecandidate && data.username != userProfileData.username) {
                console.log('icecandidate added');
        
                if (peerConnection.remoteDescription) {
                    if (
                        data.icecandidate.candidate &&
                        data.icecandidate.sdpMid !== undefined &&
                        data.icecandidate.sdpMLineIndex !== undefined
                    ) {
                        peerConnection.addIceCandidate(new RTCIceCandidate(data.icecandidate))
                            .catch((error) => {
                                console.error('Failed to add ICE candidate:', error);
                            });
                    } else {
                        console.error('Invalid iceCandidate :', data.icecandidate);
                    }
                } else {
                    console.warn('Remote description is not set yet.');
                }
            }

            

            if (data.sdp && data.username != userProfileData.username) {
                  console.log('sdp type',data.sdp.type)
                    if(data.sdp.type === 'answer'){
                      peerConnection.setRemoteDescription(new RTCSessionDescription(data.sdp))
                                .then(() => {
                                    console.log('remote secription added')
                                })
                    }

                    if(data.sdp.type === 'offer'){
                       console.log('offer created above')
                      //  dataInfo=data 
                       const vd=document.getElementById('vedioAnswercall')
                       vd.style.display='block';
                       document.getElementById('callerPerson').innerHTML=data.username
                       var ring=document.getElementById('caller')
                       ring.play();

                      //  vd.classList.add('show');
                       document.getElementById('callAnswer').addEventListener('click',function(){
                        attenedCall(data);
                       });

                     
              }
            }            
    };
    
   

    document.getElementById('callDecline').addEventListener('click',()=>{
      console.log('click decline')
      document.getElementById('vedioAnswercall').style.display='none'
      var ring=document.getElementById('caller')
      ring.pause();

    })

    document.getElementById('vedioAnswercall').addEventListener('load',()=>{
      var ring=document.getElementById('caller')
      if (ring.paused) {
        ring.play();
    }
      
    })

    function attenedCall(dataInfo){
      console.log('click answer',dataInfo)
      var ring=document.getElementById('caller')
      ring.pause();
      videoBox.style.display='block';
      videoBox1.style.display='block';
      navigator.mediaDevices.getUserMedia({ video: true, audio: true })
            .then(function(stream) {
                mediaStream = stream; 
                video = document.createElement('video');
                // video.srcObject = stream;
                video.autoplay = true;
                video.setAttribute('id', 'videoElement');
                video.style.width = '100%'; 
                video.style.height = '100%';              
                video2 = document.createElement('video');
                video2.srcObject = stream;
                video2.autoplay = true;
                video2.setAttribute('id', 'videoElement2');
                video2.style.width = '100%'; 
                video2.style.height = '100%';
                // video.style.overflow='hidden';
                videoBox.appendChild(video);
                videoBox1.appendChild(video2);
                vedioCheck=true
                
                stream.getTracks().forEach(track => peerConnection.addTrack(track,stream));
                peerConnection.setRemoteDescription(new RTCSessionDescription(dataInfo.sdp))
                .then(() => {
                    if (dataInfo.sdp.type === 'offer') {
                      return peerConnection.createAnswer();
                    }
                })
                .then(answer =>{
                peerConnection.setLocalDescription(answer)
                // console.log('sdp answer by',data.username, 'answer is',answer)
                // console.log('remoted des',peerConnection.remoteDescription)

                sendSignal('sdp',answer);

                })
                .then(() => {
                    console.log('sdp answer send')

                })
                .catch(error => console.error('Error handling SDP:', error));
                peerConnection.ontrack =(event)=>{
                  const remoteVideoElement = document.getElementById('videoElement');
                  remoteVideoElement.srcObject = event.streams[0];
                }
                  
                peerConnection.onicecandidate = (event)=> {
  
                  if (event.candidate) {
                      sendSignal('icecandidate', event.candidate);
                  }
                }    
            })
            .catch(function(err) {
                console.error('Error accessing media devices:', err);
            }); 
               
      document.getElementById('vedioAnswercall').style.display='none'
    }

    socket.onerror = function (error) {
      // console.error(WebSocket error for ${userId}:, error);
    };

    socket.onclose = function (event) {
      // console.log(WebSocket connection closed for ${userId}:, event);
    };

    // Set the currentSocket to the new WebSocket connection
    currentSocket = socket;
}


  document.querySelector('#chat-submit').addEventListener('click', function(e) {
              e.preventDefault() 
              if (currentSocket && currentSocket.readyState === WebSocket.OPEN) { 
              const messageInputDom = document.querySelector('#chat-input');
              const message = messageInputDom.value;
              // console.log(message)
              currentSocket.send(JSON.stringify({
                  'message': message
              }));
              messageInputDom.value = '';
            }
          });


function closeChat(event) {
  event.preventDefault(); 
  if (chat1 && chat2) {
    chat2.classList.add('d-none');
    chat1.classList.remove('d-none');
  }
  if (currentSocket && currentSocket.readyState === WebSocket.OPEN) {
      console.log('currentSocket is on')
      while (chatLog.firstChild) {
           chatLog.removeChild(chatLog.firstChild);
      }
      currentSocket.close();
    }

}
 



var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));

var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
});


peerConnection.addEventListener('iceconnectionstatechange', () => {
  console.log('ICE Connection State:', peerConnection.iceConnectionState);

  if (peerConnection.iceConnectionState === 'connected' || peerConnection.iceConnectionState === 'completed') {
      console.log('Peers are connected.');
  }
});



document.getElementById('vedioButton').addEventListener('click',()=>{
  if(!vedioCheck){
   videoBox.style.display='block';
   videoBox1.style.display='block';
   navigator.mediaDevices.getUserMedia({ video: true, audio: true })
          .then(function(stream) {
              mediaStream = stream; 
              video = document.createElement('video');
              // video.srcObject = stream;
              video.autoplay = true;
              video.setAttribute('id', 'videoElement');
              video.style.width = '100%'; 
              video.style.height = '100%';              
              video2 = document.createElement('video');
              video2.srcObject = stream;
              video2.autoplay = true;
              video2.setAttribute('id', 'videoElement2');
              video2.style.width = '100%'; 
              video2.style.height = '100%';
              // video.style.overflow='hidden';
              videoBox.appendChild(video);
              videoBox1.appendChild(video2);
              vedioCheck=true
              
              stream.getTracks().forEach(track => peerConnection.addTrack(track,stream));

              peerConnection.createOffer()
              .then(offer => peerConnection.setLocalDescription(offer))
              .then(() => {
                console.log('offer created ',peerConnection.localDescription)
                sendSignal('sdp',peerConnection.localDescription);
              })
              .catch(error => console.error('Error creating offer:', error));

             

              peerConnection.ontrack =(event)=>{
                const remoteVideoElement = document.getElementById('videoElement');
                remoteVideoElement.srcObject = event.streams[0];
              }

              peerConnection.onicecandidate = (event)=> {

                if (event.candidate) {
                    sendSignal('icecandidate', event.candidate);
                }
              }
          })
          .catch(function(err) {
              console.error('Error accessing media devices:', err);
        }); 

  }
});
         


document.getElementById('closeButton').addEventListener('click', ()=> {
         videoBox.style.display='none';
         videoBox1.style.display='none';
         vedioCheck=false
         stop()
     });

document.getElementById('stopvedioButton').addEventListener('click', function() {
   if (video2.muted==true){
     // video.muted=false
     video2.muted=false
     document.getElementById('stopvedioButton').style.backgroundColor=rgb(118, 118, 248);

   // 
   }
   else{
     // video.muted=true
     video2.muted=true
     document.getElementById('stopvedioButton').style.backgroundColor='aliceblue';

   }
});


let mediaStream;

videoBox.addEventListener('mousedown', (e)=>{
 isDragging = true;
 offsetX = e.clientX - videoBox.getBoundingClientRect().left;
 offsetY = e.clientY - videoBox.getBoundingClientRect().top;
 initialWidth = videoBox.offsetWidth;
 initialHeight = videoBox.offsetHeight;
});


videoBox.addEventListener('mouseup', ()=>{
 isDragging = false;
});


videoBox.addEventListener('mousemove', (e)=>{
 if (isDragging) {
   videoBox.style.top = (e.clientY - offsetY) + 'px';
   videoBox.style.left = (e.clientX - offsetX) + 'px';
}
});

function stop(){
     if (mediaStream) {
             mediaStream.getTracks().forEach(track => track.stop());
             const videoElement = document.getElementById('videoElement');
             const videoElement2 = document.getElementById('videoElement2');

             if (videoElement) {
               videoElement.remove(); 
             }
             if (videoElement2) {
               videoElement2.remove(); 
             }
     }
}





function sendSignal(type, data) {
  if (currentSocket && currentSocket.readyState === WebSocket.OPEN) {
    var info={[type]:data}  
    currentSocket.send(JSON.stringify(info));
  }
}
