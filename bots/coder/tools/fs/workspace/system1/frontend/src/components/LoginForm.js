import React, { useState } from 'react';
import axios from 'axios';

function LoginForm() {
const [username, setUsername] = useState('');
const [password, setPassword] = useState('');
const [message, setMessage] = useState('');

const handleLogin = () => {
axios.post('/api/login', { username, password })
.then(response => setMessage(response.data.message))
.catch(error => setMessage(error.response.data.message));
};

return (
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
{message && <p>{message}</p>}
</form>
);
}

export default LoginForm;
