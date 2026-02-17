![Python](https://img.shields.io/badge/Python-3.10-blue)
![Kafka](https://img.shields.io/badge/Apache-Kafka-black)
![Spark](https://img.shields.io/badge/Apache-Spark-orange)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED)
![Power BI](https://img.shields.io/badge/PowerBI-Dashboard-yellow)
![Prometheus](https://img.shields.io/badge/Monitoring-Prometheus-red)
![License](https://img.shields.io/badge/License-MIT-green)

## Project Name: Real Time Stock Market Analysis
Project Overview
This project implements an end-to-end real-time stock market data pipeline that collects stock price data from an external API, streams it through Kafka, processes it using Spark Streaming, stores it in PostgreSQL, and visualises insights using Power BI.
All services are containerised with Docker to ensure portability, reproducibility, and easy deployment.
The goal of this project is to demonstrate real-time data engineering concepts, including streaming pipelines, distributed processing, database storage, monitoring, and visualisation.
 All components are containerized with Docker for easy deployment.

 ### Data Pipeline Architecture
 ![Data Pipeline Architecture](_img/Real-Time Stock Data Pipeline Architecture.png)


 
Project Tech Stack and Flow
  - `Kafka UI → inspect topics/messages.`
  - `API → produces JSON events into Kafka.`
  - `Spark → consumes from Kafka, writes to Postgres.`
  - `Postgres → stores results for analytics.`
  - `pgAdmin → manage Postgres visually.`
  - `Power BI → external (connects to Postgres database).`
  Testing GitHub commit
  