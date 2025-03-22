# Engagefy - Social Media Performance Analysis Tool
#### Level SuperMind Hackathon 2025 OA Submission

![image](https://github.com/user-attachments/assets/94aea794-db5d-4640-908b-f5a4e0d120b9)


## Overview
**Engagefy** is an AI-powered tool designed to evaluate and generate insights into social media engagement. Focusing on user experience, our platform empowers users to analyze their profiles and specific post types with precision and ease. 

### Key Features:
- **Frontend**: Developed using React for a seamless and interactive user interface.
- **Database**: DataStax Astra DB powers distributed and efficient data storage and retrieval.
- **Workflow Creation**: Langflow integrates to manage workflows and GPT integration for insight generation.
- **Generative Model**: GPT provides advanced insights by evaluating engagement metrics.
- **Third-Party Integration**: Anonymous Instagram data scraping using a [secure API](https://rapidapi.com/social-api1-instagram/api/instagram-scraper-api2) for profile and post-type analysis.

---

## Modified Features
We enhanced the original assignment with the following functionalities:
- **Profile Analysis**: Users can only analyse their overall performance with their Instagram account username/link.
- **Post-Specific Analysis**: Get performance insights for a particular post type (carousel, reels, static images).

---

## Project Architecture
<img width="500" alt="Instagram Analysis - Sample flow" src="https://github.com/user-attachments/assets/be288578-49e2-48d3-90c6-a6f304b6b240" />

- The architecture connects the React frontend, DataStax DB, Langflow workflows, and OpenAI's GPT for insights generation.

---

## Technologies Used

| Component        | Technology/Tool       |
|------------------|-----------------------|
| **Frontend**     | React                |
| **Database**     | DataStax Astra DB    |
| **Workflow**     | Langflow             |
| **Insights**     | OpenAI's GPT Model         |
| **API**          | [Third-party Instagram Data Scraper](https://rapidapi.com/social-api1-instagram/api/instagram-scraper-api2) |

---

## How It Works ✨

### Step-by-Step Process:
1. **Data Collection**:
   - The platform uses a [third-party API](https://rapidapi.com/social-api1-instagram/api/instagram-scraper-api2) to scrape the Instagram Profile Posts of the User.
   - Engagement data such as likes, comments, and shares are fetched.

2. **Data Storage**:
   - The scraped data is stored securely in **DataStax Astra DB (Non-Vector based)**, ensuring scalability and reliability.

3. **Workflow Management**:
   - **Langflow** is responsible for the workflows, including data processing and integration with the GPT model.

4. **Insights Generation**:
   - The **OpenAI's GPT model** evaluates the metrics and generates actionable insights based on post types and user profiles.

5. **User Interaction**:
   - Users can upload their profile name as well as choose specific post types for analysis.
   - The platform displays engagement metrics and insights in an easy-to-read format.

---

## Example Insights 📊
- **Carousel Engagement**: Carousel posts have 20% higher engagement than static images.
- **Reels Performance**: Reels generate twice the comments compared to other post types.

---

## Working Illustration 🛠️

```mermaid
graph TD;
    A[User] --> B[React Frontend];
    B --> C[Langflow Workflow];
    C --> D[DataStax Astra DB];
    C --> E[OpenAI's GPT Model];
    E --> F[Insights]
```

---

## Contact 📬
For inquiries or support, contact:
- **Email**: mayureshchoudhary22@gmail.com
- **GitHub Issues**: https://github.com/Mayuresh-22/Engagefy

---

## Acknowledgments 🙌
- **Langflow** for workflow management.
- **DataStax** for robust database solutions.
- **OpenAI's GPT** for generative insights.
- **Third-Party API** for enabling anonymous Instagram data scraping.

---
