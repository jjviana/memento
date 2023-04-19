import React, { useState } from 'react';
import './App.css';
import axios from 'axios';
import LoginForm from './components/LoginForm';
import RegistrationForm from './components/RegistrationForm';
import Welcome from './components/Welcome';

function App() {
const [formType, setFormType] = useState('');

const handleFormTypeChange = (event) => {
setFormType(event.target.value);
};

return (
<div className="App" style={{backgroundColor: "white"}}>
<header className="App-header">
<select value={formType} onChange={handleFormTypeChange}>
<option value="">Welcome</option>
<option value="login">Sign In</option>
<option value="register">Register</option>
</select>
</header>
{formType === 'login' && <LoginForm />}
{formType === 'register' && <RegistrationForm />}
{formType === '' && <Welcome />}

</div>
);
}

export default App;
