import React, { useState } from 'react';
import axios from 'axios';

function RegistrationForm() {
const [username, setUsername] = useState('');
const [password, setPassword] = useState('');
const [message, setMessage] = useState('');

const handleRegister = () => {
axios.post('/api/register', { username, password })
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
<button type="button" onClick={handleRegister} style={{fontSize: "16px", color: "white", backgroundColor: "green", padding: "5px", border: "none"}}>Register</button>
{message && <p>{message}</p>}
</form>
);
}

export default RegistrationForm;
