import { useState } from "react";
import { useNavigate } from "react-router-dom";
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
        console.log("Login submitted:", formData);
    };

    const navigate = useNavigate();

    return (
        <div classNmae="login-container">
            <form onSubmit={handleSubmit} className="login-form">
                <h2>Log In</h2>

                <div className="form-group">
                    <label>ID:</label>
                    <input
                        type="text"
                        name="id"
                        value={formData.id}
                        onChange={handleChange}
                        required
                    />
                </div>

                <div className="form-group">
                    <label>Password:</label>
                    <input
                        type="password"
                        name="password"
                        value={formData.password}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div className="btn-group">
                    <button type="submit" className="login-btn">
                        Login
                    </button>
                    <button onClick={() => navigate("/signup")} className="signup-btn">
                        Sign up
                    </button>
                </div>
            </form>

        </div>
    );
}

export default Login;