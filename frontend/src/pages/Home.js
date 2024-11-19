import React from 'react';
import '../styles/Home.css';

const Home = () => {
  return (
    <div className="home">
      <section className="hero">
        <h1>Welcome to ShopWise</h1>
        <p>Compare prices and get personalized product recommendations</p>
      </section>
      <section className="features">
        <h2>Our Features</h2>
        <div className="features-grid">
          <div className="feature">
            <h3>Price Comparison</h3>
            <p>Compare prices across multiple stores</p>
          </div>
          <div className="feature">
            <h3>Smart Recommendations</h3>
            <p>Get personalized product suggestions</p>
          </div>
          <div className="feature">
            <h3>Real-time Updates</h3>
            <p>Stay updated with latest prices</p>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;