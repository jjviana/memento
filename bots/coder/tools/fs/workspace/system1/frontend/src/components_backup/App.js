import React, { useState, useEffect } from 'react';
import './App.css';
import axios from 'axios';

function App() {
const [username, setUsername] = useState('');
const [password, setPassword] = useState('');
const [message, setMessage] = useState('');

const handleLogin = () => {
axios.post('/login', { username, password })
.then(response => setMessage(response.data.message))
.catch(error => setMessage(error.response.data.message));
};

const handleRegister = () => {
axios.post('/register', { username, password })
.then(response => setMessage(response.data.message))
.catch(error => setMessage(error.response.data.message));
};

return (
<div className="App" style={{backgroundColor: "white"}}>
<header className="App-header">
{message && <p>{message}</p>}
<form style={{padding: "20px", border: "1px solid black"}}>
<label style={{marginBottom: "10px"}}>
Username:
<input type="text" value={username} onChange={e => setUsername(e.target.value)} style={{fontSize: "16px", color: "black", padding: "5px", border: "1px solid black"}} />
</label>
<label style={{marginBottom: "10px"}}>
Password:
<input type="password" value={password} onChange={e => setPassword(e.target.value)} style={{fontSize: "16px", color: "black", padding: "5px", border: "1px solid black"}} />
</label>
<button type="button" onClick={handleLogin} style={{fontSize: "16px", color: "white", backgroundColor: "blue", padding: "5px", border: "none", marginRight: "10px"}}>Login</button>
<button type="button" onClick={handleRegister} style={{fontSize: "16px", color: "white", backgroundColor: "green", padding: "5px", border: "none"}}>Register</button>
</form>
</header>
</div>
);
}

export default App;
