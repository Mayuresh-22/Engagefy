## Leverl-SuperMind-2025
This repo contains code of online assignment for Level SuperMind Hackathon 2025
## Social Media Performance Analysis

![Project Logo](https://via.placeholder.com/150) <!-- Replace with your project logo -->

## Overview

The **Social Media Performance Analysis** project is designed to develop a basic analytics module that utilizes **Langflow** and **DataStax** to analyze engagement data from mock social media accounts. The objective is to create a workflow that can fetch, analyze, and provide insights into various types of social media posts based on user-defined metrics.

### Submission Deadline
**January 8th**

## Tools and Technologies

- **DataStax Astra DB**: For database operations and data storage.
- **Langflow**: For workflow creation and integration with GPT for generating insights.

## Project Objectives

1. **Fetch Engagement Data**:
   - Create a small dataset simulating social media engagement (e.g., likes, shares, comments, post types).
   - Store this data in DataStax Astra DB.

2. **Analyze Post Performance**:
   - Construct a simple flow using Langflow that:
     - Accepts post types (e.g., carousel, reels, static images) as input.
     - Queries the dataset in Astra DB to calculate average engagement metrics for each post type.

3. **Provide Insights**:
   - Utilize GPT integration in Langflow to generate insights based on the analyzed data.
   - Example outputs:
     - "Carousel posts have 20% higher engagement than static posts."
     - "Reels drive 2x more comments compared to other formats."

## Architecture

![Architecture Diagram](https://via.placeholder.com/600x400) <!-- Placeholder for architecture diagram -->
*Insert architecture diagram here*
