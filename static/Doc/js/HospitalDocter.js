function openNav() {
    // document.getElementById("mySidenav").style.width = "300px";
    if (document.getElementById("mySidenav").style.width>'0px'){
            document.getElementById("mySidenav").style.width = "0";

    }
    else{
        document.getElementById("mySidenav").style.width = "300px";
    }
    

  }
  
  function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
  }
  
