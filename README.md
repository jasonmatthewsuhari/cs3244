# 🤖 Decoding Emotions: A Classification Approach to Assigning Emoticons to Text

## 📌 Project Overview

This project, completed as part of **CS3244 Machine Learning (AY24/25 Semester 2)** at the **National University of Singapore**, explores the application of machine learning to predict the most appropriate emoji for a given piece of tweet text. Our team focuses on leveraging the **Twemoji dataset**, which contains Tweet IDs annotated with their most fitting emoji label. 

While the dataset does not include tweet metadata or content directly, we intended to retrieve the full tweet text via the **Twitter v2 API** and web scraping through **Nitter**. This, however, hit us with lots of rate limits which were not overcome with any form of parallelization or self-hosted **Nitter** instances.

Therefore, we provide full credit to the original scrapers of the datasets:  

1.) https://github.com/ckcherry23/Twemoji/tree/main/Datasets  

2.) https://github.com/RussellDash332/CS3244-Twemoji/blob/main/Cleaning-1.ipynb

## 👨‍💻 Team Members

- Jason Matthew Suhari  
- Bryan Castorius Halim  
- Nigel Eng Wee Kiat  
- Muhammad Salman Al Farisi  
- Ng Jia Hao Sherwin  
- Ryan Justyn  

## 📂 Dataset Description

The **Twemoji** dataset is designed for emoji classification tasks. It consists of tweet identifiers (Tweet IDs) and corresponding emoji labels that represent the most semantically appropriate emoji for each tweet. Since direct access to tweet content is restricted due to Twitter's API limitations, we obtained the tweet text externally to enrich the dataset and enable supervised learning.

## 💡 Motivation

As digital natives, especially within Gen Z, we frequently use emojis to add emotional nuance and playfulness to our digital conversations. However, it’s not always easy to pick the emoji that best captures the sentiment or tone of a message.

While this may not be a critical problem, automating emoji suggestions can provide a **quality-of-life improvement** across platforms that support emoji reactions—such as **Twitter**, **Telegram**, or **iMessage**. Our goal is to create a machine learning model capable of suggesting the most contextually appropriate emoji for a given text input.

This project not only solves a relatable modern-day inconvenience but also allows us to gain hands-on experience with **text preprocessing**, **feature engineering**, **multi-class classification**, and the evaluation of various **machine learning models and ensembles**—all of which are integral to mastering machine learning concepts.

---

## ⚙️ Setup Instructions

Follow these steps to set up the environment and download the dataset:

### 1. Clone the repository

```bash
git clone https://github.com/jasonmatthewsuhari/cs3244.git
cd cs3244/
```

### 2. Download the Dataset  

Ensure you have a file named urls.txt containing the tweet data URLs. This is the access point for our S3 bucket which contains all of the processed .npy files,
in case you would prefer to load the dataset locally for your own testing.  

In the entry point(s) of our code--mainly the Jupyter Notebooks--we will be directly loading the numpy files into memory. **This step is optional.**

```bash
# Linux/macOS
wget -P data/ -i urls.txt
```

```bash
# Windows (PowerShell)
Get-Content urls.txt | ForEach-Object { Invoke-WebRequest -Uri $_ -OutFile ("data/" + [System.IO.Path]::GetFileName($_)) }
```
💡 If wget or PowerShell is unavailable, you may also use curl or a browser-based download method.

### 3. Set up a Python virtual environment

```bash
# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

```bash
# Windows (Command Prompt)
python -m venv venv
venv\Scripts\activate
```

```bash
# Windows (PowerShell)
python -m venv venv
venv\Scripts\Activate.ps1
```

### 4. Install required dependencies

```bash
pip install -r requirements.txt
```

### 5. (Optional) Adding a new model
If you're adding a new model to the project, please request write access for caching of the model. If not, you can also just add the train code locally

### 6. (Optional) Updatign the report PDF
To update the report PDF, you may look into `report/main.tex` and make your updates there, and if you have the `make` tool as well as `pdflatex` installed, you may do the following commands to re-generate the PDF. 

```bash
cd reports
make pdf
```

As of right now, the report PDF is in the `.gitignore` to prevent commit clogging, but will be in the final commit for submission. :)