import { useState } from "react";
import "./Login.css";


function Login() {
    const [formData, setFormData] = useState({
        id: "",
        password: "",
    });

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log("Login submiteted:", formData);
    };

    return (
        <div classNmae="login-container">
            <form onSubmit={handleSubmit} className="login-form">
                <h2>Log In</h2>

                <div className="form-group">
                    <label>ID</label>
                    <input
                        type="id"
                        name="id"
                        value={formData.id}
                        onChange={handleChange}
                        required
                    />
                </div>

                <div className="form-group">
                    <label>PASSWORD</label>
                    <input
                        type="password"
                        name="password"
                        value={formData.password}
                        onChange={handleChange}
                        required
                    />
                </div>
                <button type="submit" className="login-btn">
                    Login
                </button>
            </form>
        </div>
    );
}

export default Login;