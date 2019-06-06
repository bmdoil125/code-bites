import React from 'react';
import { Link } from 'react-router-dom';

const NavBar = (props) => (
    <nav className="navbar is-dark" role="navigation" aria-label="main navigation">
        <section className="container">
            <div className="navbar-brand">
                <strong className="navbar-item">{props.title}</strong>
                <span
                className="nav-toggle navbar-burger"
                onClick={() => {
                    let toggle = document.querySelector(".nav-toggle");
                    let menu = document.querySelector(".navbar-menu");
                    toggle.classList.toggle("is-active"); menu.classList.toggle("is-active");
                }}>
                <span></span>
                <span></span>
                <span></span>
                </span>
            </div>
            <div className="navbar-menu">
                <div className="navbar-start">
                    <Link to="/" className="navbar-item">Home</Link>
                    <Link to="/about" className="navbar-item">About</Link>
                    <Link to="/me" className="navbar-item">Profile</Link>
                </div>            
                <div className="navbar-end">
                    {!props.isAuthenticated &&
                        <Link to="/register" className="navbar-item">Register</Link>
                    }
                    {!props.isAuthenticated &&
                        <Link to="/login" className="navbar-item">Login</Link>
                    }
                    {!props.isAuthenticated &&
                        <Link to="/signout" className="navbar-item">Signout</Link>
                    }                    
                </div>
            </div>
        </section>
    </nav>
)



export default NavBar;