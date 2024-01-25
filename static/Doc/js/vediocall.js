$(document).ready(function() {
    var isDragging = false;
    var offsetX, offsetY;
    var initialWidth, initialHeight;
    var videoBox = document.getElementById('video-Box');
    var videoBox1 = document.getElementById('video-box-User');
    let vedioCheck=false

    let video
    function vedio() {
        $('#video-Box').show();
        $('#video-box-User').show();                  
    }
   let mediaStream
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
  


    $('#vedioButton').on('click', function() {
        console.log('Video button clicked');
        if(!vedioCheck){
          videoBox.style.display='block';
          videoBox1.style.display='block';
          navigator.mediaDevices.getUserMedia({ video: true, audio: true })
                .then(function(stream) {
                    mediaStream = stream; 
                    video = document.createElement('video');
                    video.srcObject = stream;
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
                    var serv='stun:stun.1.google.com:19302';
                    const config = {iceServers:[{urls:serv}] };
                    // let peerConnection = new RTCPeerConnection(config)
                    // stream.getTracks.forEach(track => peerConnection.addTrack(track,stream));
                    // peerConnection.onicecandidate = handleIceCandidate;
                    // peerConnection.ontrack = handleTrack;

                    // const offer = peerConnection.createAnswer()
                    // peerConnection.setLocalDescription(offer)
                    
                    // sendSignal('offer',offer);

                })
                .catch(function(err) {
                    console.error('Error accessing media devices:', err);
                }); 
        }
        
    });

    $('#closeButton').on('click', function() {
                console.log('Close button clicked');
                videoBox.style.display='none';
                videoBox1.style.display='none';
                vedioCheck=false
                stop()
                // $('#video-Box').hide();
            });
    $('#stopvedioButton').on('click', function() {
      console.log('click stop')
      if (video.autoplay==true){
        console.log('click stop you')
        video.autoplay=false

      }
      else{
        console.log('click stop me')
        video.autoplay=true


      }

    });

    function startDrag(e) {
        isDragging = true;
        offsetX = e.clientX - videoBox.getBoundingClientRect().left;
        offsetY = e.clientY - videoBox.getBoundingClientRect().top;
        initialWidth = videoBox.offsetWidth;
        initialHeight = videoBox.offsetHeight;
    }

    function stopDrag() {
        isDragging = false;
    }

    function drag(e) {
        if (isDragging) {
            videoBox.style.top = (e.clientY - offsetY) + 'px';
            videoBox.style.left = (e.clientX - offsetX) + 'px';
        }
    }

    videoBox.addEventListener('mousedown', startDrag);
    videoBox.addEventListener('mouseup', stopDrag);
    videoBox.addEventListener('mousemove', drag);
}); 


  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });