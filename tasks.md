# Telegram / ChatGPT Bot

A Telegram bot integrated with OpenAI ChatGPT, providing multiple interactive features such as quizzes, conversations, translations, and more.

---

## 📋 Project Requirements

The project must implement **6 features** described below.

### 📦 How to Submit
- Provide a link to a **public GitHub repository**, or
- Send a **ZIP archive via Pumble**

### ⏰ Deadline
**23:59:59 — November 1, 2024**

If you have any questions, contact via **Pumble**.

---

## 🚀 Features

### 1️⃣ Echo Bot
A Telegram bot that receives a user message and replies with **the same text**.

---

### 2️⃣ Random Fact
Command: `/random`

The bot:
- Sends a predefined image
- Sends a predefined prompt to ChatGPT
- Returns the ChatGPT response to the user

---

### 3️⃣ ChatGPT Interface
Command: `/gpt`

The bot:
- Sends a predefined image
- Sends the user's message to ChatGPT
- Returns ChatGPT’s response as a text message

---

### 4️⃣ Dialogue with a Famous Personality
Command: `/talk`

The bot:
- Sends a predefined image
- Offers a selection of famous personalities via buttons
- Sets a persona-specific prompt after selection
- Forwards all subsequent user messages to ChatGPT
- Returns ChatGPT responses to the user

---

### 5️⃣ Quiz
Command: `/quiz`

The bot:
- Sends a predefined image
- Offers quiz topics via buttons
- Requests a quiz question from ChatGPT
- Treats the next user message as the answer
- Sends the answer to ChatGPT for evaluation
