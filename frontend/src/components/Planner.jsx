import React, { useState } from 'react';

const Planner = () => {
    const [query, setQuery] = useState({ city: "", interest: "" });
    const [itinerary, setItinerary] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    //const API_BASE_URL = "http://localhost:5000";
    const API_BASE_URL = window.location.origin;
    const handleSubmit = async (e) => {
        e.preventDefault();
        
        if (!query.city.trim() || !query.interest.trim()) {
            setError("Please fill in both city and interests");
            return;
        }

        setLoading(true);
        setError("");
        setItinerary("");

        try {
            const response = await fetch(`${API_BASE_URL}/aiplanner`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ city: query.city, interest: query.interest })
            });
            
            const json = await response.json();
            
            if (json.status === "success") {
                setItinerary(json.response);
            } else {
                setError(json.message || "Failed to generate itinerary");
            }
        } catch (err) {
            setError("Error connecting to server. Please try again.");
            console.error("Error:", err);
        } finally {
            setLoading(false);
        }
    };

    const handleReset = () => {
        setQuery({ city: "", interest: "" });
        setItinerary("");
        setError("");
    };

    const onChange = (e) => {
        setQuery({ ...query, [e.target.name]: e.target.value });
        setError("");
    };

    return (
        <div className="planner-container">
            <div className="container">
                <div className="row justify-content-center">
                    <div className="col-lg-8">
                        <div className="planner-header text-center mb-5">
                            <h1 className="display-4 mb-3">
                                <i className="bi bi-airplane-fill me-3"></i>
                                AI Travel Planner
                            </h1>
                            <p className="lead text-muted">
                                Plan your perfect day trip with AI-powered recommendations
                            </p>
                        </div>

                        <div className="card shadow-lg border-0 mb-4">
                            <div className="card-body p-4">
                                <form onSubmit={handleSubmit}>
                                    <div className="mb-4">
                                        <label htmlFor="city" className="form-label fw-bold">
                                            <i className="bi bi-geo-alt-fill me-2 text-primary"></i>
                                            Destination City
                                        </label>
                                        <input 
                                            type="text" 
                                            className="form-control form-control-lg" 
                                            id="city" 
                                            value={query.city} 
                                            onChange={onChange} 
                                            name="city" 
                                            placeholder="e.g., Paris, Tokyo, New York"
                                            disabled={loading}
                                        />
                                    </div>
                                    
                                    <div className="mb-4">
                                        <label htmlFor="interest" className="form-label fw-bold">
                                            <i className="bi bi-heart-fill me-2 text-danger"></i>
                                            Your Interests
                                        </label>
                                        <input 
                                            type="text" 
                                            className="form-control form-control-lg" 
                                            id="interest" 
                                            value={query.interest} 
                                            onChange={onChange} 
                                            name="interest" 
                                            placeholder="e.g., Coffee, art, food, museums"
                                            disabled={loading}
                                        />
                                        <div className="form-text">
                                            Separate multiple interests with commas
                                        </div>
                                    </div>

                                    {error && (
                                        <div className="alert alert-danger alert-dismissible fade show" role="alert">
                                            <i className="bi bi-exclamation-triangle-fill me-2"></i>
                                            {error}
                                        </div>
                                    )}

                                    <div className="d-grid gap-2 d-md-flex justify-content-md-end">
                                        <button 
                                            type="button" 
                                            className="btn btn-outline-secondary btn-lg"
                                            onClick={handleReset}
                                            disabled={loading}
                                        >
                                            <i className="bi bi-arrow-counterclockwise me-2"></i>
                                            Reset
                                        </button>
                                        <button 
                                            type="submit" 
                                            className="btn btn-primary btn-lg"
                                            disabled={loading}
                                        >
                                            {loading ? (
                                                <>
                                                    <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                                                    Generating...
                                                </>
                                            ) : (
                                                <>
                                                    <i className="bi bi-magic me-2"></i>
                                                    Generate Itinerary
                                                </>
                                            )}
                                        </button>
                                    </div>
                                </form>
                            </div>
                        </div>

                        {itinerary && (
                            <div className="card shadow-lg border-0 itinerary-result">
                                <div className="card-header bg-gradient text-white py-3">
                                    <h4 className="mb-0">
                                        <i className="bi bi-map-fill me-2"></i>
                                        Your Personalized Itinerary
                                    </h4>
                                </div>
                                <div className="card-body p-4">
                                    <div className="itinerary-content">
                                        {itinerary.split('\n').map((line, index) => (
                                            <p key={index} className="mb-2">
                                                {line}
                                            </p>
                                        ))}
                                    </div>
                                    <div className="mt-4 pt-3 border-top">
                                        <button 
                                            className="btn btn-outline-primary"
                                            onClick={handleReset}
                                        >
                                            <i className="bi bi-plus-circle me-2"></i>
                                            Plan Another Trip
                                        </button>
                                    </div>
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Planner;