// import firebase from 'node_modules/firebase/app';
// import 'node_modules/firebase/analytics';

window.onload = function() {
  
    alert("3");
}


// function aws(name, x, y){
//     return `coming from javascript ${name} ${x} ${y}`;
// }




// const firebaseConfig = {
// apiKey: "AIzaSyCxG7s_Wg6RAC4AQ5ZpkCgt0XcnSqcwt-A",
// authDomain: "nyucapstone-7c22c.firebaseapp.com",
// projectId: "nyucapstone-7c22c",
// storageBucket: "nyucapstone-7c22c.appspot.com",
// messagingSenderId: "658619789110",
// appId: "1:658619789110:web:8f198dfe92ec5ec1a74d97",
// measurementId: "G-WJEFZHTTLV"
// };


firebase.initializeApp(firebaseConfig);
const analytics = firebase.analytics();

  const byteArray = new Uint8Array(byteNumbers);
  const blob = new Blob([byteArray], {type: "image/png"});
  
  const storage = firebase.storage.getStorage(fireapp);
  const storageRef = firebase.storage.ref(storage, `images/${time_str}.png`);
  const uploadTask = firebase.storage.uploadBytesResumable(storageRef, blob);
  
  uploadTask.on("state_changed", (snapshot) => {
     
  }, (error) => {
      console.log("oh no we didn't make it to firebase");
      
  }, () => {
      console.log("to firebase");
  });
