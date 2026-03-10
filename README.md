# 🔗 URL Shortener (Full Stack Project)

A full-stack URL shortening platform built using **React, Flask, and SQLite** that allows users to convert long URLs into short links, generate QR codes, and track link analytics.

This project demonstrates **REST API design, database integration, frontend development, and system design concepts similar to services like Bitly.**

---

## 🚀 Live Demo

Frontend: https://your-frontend.vercel.app  
Backend API: https://your-backend.onrender.com

---

## 📌 Features

- 🔗 **Shorten long URLs**
- ⭐ **Custom short URLs**
- ⏳ **Expiration links**
- 📊 **Click analytics dashboard**
- 🌍 **Geo-location tracking**
- 📱 **QR code generation**
- 🗑 **Delete links**
- 📦 **REST API backend**
- 🎨 **Modern React UI**

---

## 🏗 System Architecture

User → React Frontend → Flask API → SQLite Database

1. User submits a long URL  
2. Backend generates a short ID  
3. URL is stored in the database  
4. When a short link is opened, the backend:
   - Redirects the user
   - Updates click analytics
   - Tracks geo-location data

---

## 🛠 Tech Stack

### Frontend
- React
- Vite
- TailwindCSS

### Backend
- Flask
- Flask-CORS
- SQLite

### Libraries
- qrcode
- pillow
- validators
- requests

### Deployment
- Vercel (Frontend)
- Render (Backend)

---

## 📂 Project Structure
