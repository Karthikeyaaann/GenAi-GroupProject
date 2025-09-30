# 🚀 GenAI Training Projects  

This repository showcases a collection of projects developed as part of the **Generative AI Training Program** conducted in our college.  
The projects explore **Large Language Models (LLMs), Computer Vision, Gesture Control, and Vision–Language Model integrations**.  

---

## 👨‍💻 Team Members  
- 👤 Jeeva  
- 👤 Jaizil Antony  
- 👤 Sajan  
- 👤 Kavin  
- 👤 Karthikeyan  

---

## 📂 Projects Overview  

### 🤖 1. AI Chatbot (Groq API)  
A console-based chatbot powered by **Groq’s LLMs**.  

🔹 **Features**  
- Real-time interactive Q&A.  
- Uses Groq API for intelligent responses.  
- Minimal and simple terminal interface.  

📌 **Use Case**: Ideal for experimenting with large language models, quick Q&A assistance, and educational demonstrations.  

---

### ✋ 2. Hand Gesture Recognition for Driving Simulation  
A **gesture-based driving control system** using **computer vision**.  

🔹 **Features**  
- Tracks **left-hand finger counts** using a webcam.  
- Controls a driving simulator with gestures:  
  - ✋ 5 fingers → **Accelerate**  
  - ✊ 0 fingers → **Brake**  
  - 🤟 3 fingers → **Neutral**  
- Built with **OpenCV + cvzone + PyAutoGUI**.  

📌 **Use Case**: Can be used in simulators, training modules, or accessibility-focused applications where physical controls are limited.  

---

### 👁️ 3. Live Vision → LLM (Ollama Integration)  
Connects a **live camera feed** with a **vision-enabled LLM** to enable real-time scene understanding.  

🔹 **Features**  
- Captures frames at **24 FPS**.  
- Users can ask context-based questions such as:  
  - *“What do you see?”*  
  - *“What dish can I make with these ingredients?”*  
- Supports **Ollama Python Client** and **REST API fallback**.  

📌 **Use Case**: Useful in real-time analysis, object detection, cooking assistance, and AI-based perception tasks.  

---

## 🛠️ Tech Stack  
- 🐍 **Language**: Python  
- ⚡ **APIs & Libraries**: Groq API, Ollama, OpenCV, cvzone, PyAutoGUI, Requests, NumPy  

---

## ⚙️ Installation & Setup  

### 🔽 1. Clone the Repository  
```bash
git clone https://github.com/<your-username>/GenAI-Training-Projects.git
cd GenAI-Training-Projects
```

### 🌱 2. Create a Virtual Environment *(Optional but Recommended)*  
```bash
python -m venv env
```
- **Linux/Mac:** `source env/bin/activate`  
- **Windows:** `env\Scripts\activate`  

### 📦 3. Install Dependencies  
```bash
pip install -r requirements.txt
```

### 🔑 4. Additional Setup  
- **AI Chatbot:** Obtain a **Groq API Key** from [Groq Console](https://console.groq.com/) and update the configuration.  
- **Live Vision → LLM:** Install and run [Ollama](https://ollama.ai), then download the vision model:  
  ```bash
  ollama pull llama3.2-vision
  ```  

---

## ▶️ Running the Projects  

- 🤖 **AI Chatbot** → Start the chatbot script and interact with the LLM in your terminal.  
- ✋ **Hand Gesture Driving Control** → Run the gesture recognition script and control a simulation with hand signs.  
- 👁️ **Live Vision → LLM** → Launch the live vision script and ask the model about what the camera sees.  

---

## 📘 Report  
A detailed project report is available in [`REPORT.md`](./REPORT.md).  

---

## 📜 License  
This repository is for **educational purposes only** as part of the Generative AI training program.  
Feel free to use and adapt it with proper attribution.  
