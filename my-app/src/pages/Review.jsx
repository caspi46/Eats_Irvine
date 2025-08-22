import { useState } from "react";
import { useNavigate } from "react-router-dom"
import "./Review.css"

function Review() {
    const [formData, setFormData] = useState({
        rating: "",
        comment: "",
    });

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log("Review submitted", formData);
    }

    const navigate = useNavigate(); // to navigate to the other page later (mb home page)

    const [rating, setRating] = useState(0);
    const [hover, setHover] = useState(0);
    // For future, can add the feature to upload the picture 
    return (
        <div className="review-container">
            <form onSubmit={handleSubmit} className="review-form">
                <h2>Review</h2>

                <div className="form-group">
                    <label>Comment:</label>
                    <textarea
                        name="comment"
                        value={formData.comment}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div className="star-rating">
                    <label>Rate:</label>
                    {[...Array(5)].map((_, i) => {
                        const starValue = i + 1;
                        return (
                            <span
                                key={starValue}
                                className={`star ${starValue <= (hover || rating) ? "filled" : ""}`}
                                onClick={() => setRating(starValue)}
                                onMouseEnter={() => setHover(starValue)}
                                onMouseLeave={() => setHover(0)}
                            >
                                ★
                            </span>
                        );
                    })}
                </div>

                <div className="btn-group">
                    <button type="submit" className="review-btn">
                        Submit
                    </button>
                </div>
            </form>
        </div>
    );
}

export default Review;


