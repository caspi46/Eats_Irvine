import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Signup.css";

function Signup() {
    const [formData, setFormData] = useState({
        id: "",
        password: "",
        email: "",
    });

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log("Signup submitted", formData);
    }

    const navigate = useNavigate();

    return (
        <div className="signup-container">
            <form onSubmit={handleSubmit} className="signup-form">
                <h2>Sign Up</h2>

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

                <div className="form-group">
                    <label>Email:</label>
                    <input
                        type="email"
                        name="email"
                        value={formData.email}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div className="btn-group">
                    <button type="submit" className="signup-btn">
                        Sign Up
                    </button>
                    <button type="button" onClick={() => navigate("/login")} className="login-btn">
                        Back To Login
                    </button>
                </div>
            </form>
        </div>
    );
}

export default Signup;