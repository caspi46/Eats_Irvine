import { useState } from "react";
import "./Home.css";

function Home() {
    const [query, setQuery] = useState("");

    const handleChange = (e) => {
        setQuery(e.target.value);
    }
    const items = ["rest1", "rest2", "rest3"];

    const filteredItems = items.filter((item) =>
        item.toLowerCase().includes(query.toLowerCase())
    );

    return (
        <div className="search-container">
            {/* <input
                type="text"
                placeholder="Search Restaurant..."
                value={query}
                onChange={handleChange}
                className="search-input"
            /> */}
            <input
                style={{ border: "2px solid red", padding: "10px" }}
                type="text"
                placeholder="Search Restaurant..."
                value={query}
                onChange={handleChange}
            />
            <ul className="search-results">
                {filteredItems.map((item, index) => (
                    <li key={index} className="search-item">
                        {item}
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default Home;