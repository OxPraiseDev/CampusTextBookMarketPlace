# Campus Textbook Exchange

A localized, student-to-student bulletin board application where students on the same campus can list, buy, sell, or trade used textbooks. Built to make textbook discovery easier, more affordable, and accessible for university students.

## Live Demo
*Deployment in progress on Render (https://campustextbookmarketplace.onrender.com)*

---

## Key Features

### For Students
*   **Authentication:** Secure registration and login restricted to official university emails (e.g., `@funaab.edu.ng`).
*   **Buy & Sell:** List textbooks with descriptions, condition, and asking price.
*   **Trade System:** Propose a direct swap with another student by offering one of your own listed books.
*   **Real-Time Chat:** Instant messaging (WebSockets) with the ability to send text, images, and live voice notes.
*   **Transaction Confirmation:** A dual-confirmation system where both the buyer and seller must click "Confirm" to mark a book as SOLD/TRADED.
*   **Live Notifications:** Top-right toast pop-ups and inbox badges for unread messages.
*   **Report System:** Ability to report a user directly to the Admin if a transaction goes wrong, attaching the chat logs as evidence.

### For Moderators (Admins)
*   **Modern Sidebar Dashboard:** Clean, responsive interface to manage the platform.
*   **User Management:** Search, edit, or delete user accounts.
*   **Listing Moderation:** Flag suspicious listings (hides them instantly from the public) or delete them permanently.
*   **Report Center:** View reported users, read the specific chat logs, and ban scammers.

---

## Technology Stack

*   **Backend:** Python 3.12+, Django 5.x, Django Channels (ASGI WebSockets)
*   **Database:** SQLite (Local), PostgreSQL (Production)
*   **Real-time Infrastructure:** Redis (Production Channel Layer)
*   **Frontend:** HTML5, Custom CSS3 (Glassmorphism), Vanilla JavaScript
*   **Server:** Daphne (ASGI), WhiteNoise (Static files)

---

## Local Installation & Setup (From Scratch)

Follow these steps exactly to get the application running on your local machine. 
*(Note: These commands are for Windows PowerShell. Mac/Linux users can use `source venv/bin/activate` instead of `venv\Scripts\activate`).*

**1. Clone the repository**
```bash
git clone https://github.com/OxPraiseDev/CampusTextBookMarketPlace.git
cd CampusTextBookMarketPlace