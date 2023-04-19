import React from 'react';

function Welcome() {
return (
<div>
<h1>Welcome to System1</h1>
<div id="triangle" style={{transform: "rotate(0deg)"}}>
▲
</div>
</div>
);
}

setInterval(() => {
const triangle = document.getElementById("triangle");
const currentRotation = parseInt(triangle.style.transform.replace("rotate(", "").replace("deg)", ""));
triangle.style.transform = `rotate(${currentRotation + 10}deg)`;
}, 100);

export default Welcome;
