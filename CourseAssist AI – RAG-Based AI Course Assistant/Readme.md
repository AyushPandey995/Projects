# 🎓 CourseAssist AI – RAG-Based AI Course Assistant

A Retrieval-Augmented Generation (RAG) system that helps learners find **exactly where a topic is taught** inside a library of video lectures. Ask a question in plain language, and CourseAssist AI returns the **lecture, topic title, and start/end timestamps** of the most relevant part of the video. It runs entirely on local models: Whisper for speech-to-text, `bge-m3` for embeddings, and an Ollama-hosted LLM for answers.

---

## 📌 Project Overview

Searching through hours of video for one concept is slow. This project converts lecture videos into a searchable knowledge base:

1. Extract audio from every lecture video.
2. Transcribe and translate the audio into timestamped text chunks with Whisper.
3. Convert every chunk into a vector embedding with `bge-m3`.
4. For a user question, retrieve the most similar chunks using cosine similarity.
5. Pass those chunks to an LLM, which answers with the lecture, title, and MM:SS timestamps.

The pipeline is currently set up on a **Quantitative Aptitude** video playlist (Hindi lectures, translated to English) and can be extended to any course library.

---

## 🎯 Objective

Turn hours of unstructured lecture video into a question-answering system that points learners to the exact lecture and timestamp covering their topic, without sending any data to external APIs.

---

## 🔄 Workflow

```text
Lecture videos (.mp4)
        │
        ▼
 01  FFmpeg: extract audio (.mp3)
        │
        ▼
 03  Whisper large-v2: transcribe + translate (Hindi → English)
        │      → timestamped chunks saved as JSON
        ▼
 05  bge-m3 (via Ollama): embed every chunk
        │      → embeddings.csv
        ▼
 06  User question → embed → cosine similarity → top matching chunks
        │
        ▼
 07  Build a prompt from the top 5 chunks
        │
        ▼
 08  Ollama LLM (deepseek-r1) → lecture, title, start/end time
```

---

## 🗂️ Scripts

| Script                                      | Purpose                                                                 |
| ------------------------------------------- | ----------------------------------------------------------------------- |
| `01_Video_to_Audio.py`                      | Converts each video in `videos/` to an `.mp3` in `audios/` using FFmpeg |
| `02_Speech_to_Text.py`                      | Test script: transcribes a single audio file with Whisper               |
| `03_Create_Chunks.py`                       | Transcribes all audio and saves timestamped chunks as JSON in `json/`   |
| `04_Creating_Embeddings.py`                 | Test script: creates embeddings for sample text with `bge-m3`           |
| `EmbeddingModule.py`                        | Reusable `create_embedding()` function used by scripts 06 to 08         |
| `05_Bulk_Embedding.py`                      | Embeds every chunk from `json/` and builds the embeddings dataset       |
| `06_Pulling_top_matching_chunk.py`          | Retrieves the top 3 most similar chunks for a question                  |
| `07_Introspecting_top_results_and_Creating_prompt.py` | Retrieves the top 5 chunks and writes the LLM prompt to `prompt.txt` |
| `08_Getting_response_from_LLM.py`           | Full pipeline: retrieval, prompt, and LLM answer                        |

---

## ⚙️ How It Works

### 1. Video to audio

`01_Video_to_Audio.py` reads each filename to get the lecture number and title, then runs FFmpeg. Video files are expected to follow this pattern:

```text
<prefix> #<lecture number>_<Title>-<suffix>.mp4
```

Output is saved as `audios/<lecture number>_<Title>.mp3`.

### 2. Transcription and chunking

Whisper `large-v2` transcribes each lecture, translating Hindi speech to English. Every Whisper segment becomes one chunk:

```python
result = model.transcribe(audio=f"audios/{audio}", language="hi",
                          task="translate", word_timestamps=False)

chunks.append({"Lecture": title_no, "Title": title,
               "Start": segment["start"], "End": segment["end"],
               "Text": segment["text"]})
```

Each lecture is saved as `json/<lecture><title>.json`.

### 3. Embeddings

Chunk texts are embedded in batches with the `bge-m3` model through Ollama's `/api/embed` endpoint. Every chunk gets a unique `chunk_id` and its embedding vector, and the result is stored in `embeddings.csv`.

```python
r = requests.post("http://localhost:11434/api/embed",
                  json={"model": "bge-m3", "input": text_list})
embedding = r.json()["embeddings"]
```

### 4. Retrieval

The question is embedded with the same model, and cosine similarity is computed against every stored chunk. The highest-scoring chunks are selected (top 3 in script 06, top 5 in scripts 07 and 08).

```python
similarities = cosine_similarity(np.vstack(df["embedding"]), [Query_Embedding]).flatten()
top_indices = similarities.argsort()[::-1][:5]
```

### 5. Prompt and answer generation

The retrieved chunks (Lecture, Title, Start, End, Text) are placed into a structured prompt that instructs the LLM to:

- identify the most relevant chunk,
- report the lecture, title, and start/end timestamps converted to **MM:SS**,
- list multiple matches from most to least relevant,
- never invent lectures, titles, or timestamps,
- reply `No data found for this question.` when nothing relevant is retrieved.

The prompt is sent to a local model through Ollama's `/api/generate` endpoint (`deepseek-r1`).

---

## 💬 Example (Illustrative)

**Question:** `How do I find the combined time when A takes 12 hours and B takes 15 hours?`

**Expected answer format:**

| Lecture | Topic         | Start | End   |
| ------- | ------------- | ----- | ----- |
| 1       | Time and Work | 01:30 | 01:46 |

---

## 🛠️ Tech Stack

| Component         | Tool                                        |
| ----------------- | ------------------------------------------- |
| Language          | Python                                      |
| Audio extraction  | FFmpeg                                      |
| Speech-to-text    | OpenAI Whisper (`large-v2`)                 |
| Embedding model   | `bge-m3` via Ollama                         |
| Similarity search | scikit-learn (cosine similarity), NumPy     |
| Data handling     | Pandas                                      |
| LLM               | `deepseek-r1` via Ollama (`llama3.2` also tried) |
| HTTP client       | Requests                                    |

---

## 🚀 How to Run

### Prerequisites

- Python 3.9+
- [FFmpeg](https://ffmpeg.org/) installed and available on your PATH
- [Ollama](https://ollama.com/) installed and running locally (`http://localhost:11434`)
- A GPU is recommended for Whisper `large-v2`

### 1. Install dependencies

```bash
pip install openai-whisper requests pandas numpy scikit-learn
```

### 2. Pull the Ollama models

```bash
ollama pull bge-m3
ollama pull deepseek-r1
```

### 3. Create the working folders and add your videos

```bash
mkdir videos audios json
```

Place your lecture videos in `videos/`.

### 4. Run the pipeline in order

```bash
python 01_Video_to_Audio.py         # videos  → audios/
python 03_Create_Chunks.py          # audios  → json/ (timestamped chunks)
python 05_Bulk_Embedding.py         # json/   → embeddings.csv
python 08_Getting_response_from_LLM.py   # ask a question, get lecture + timestamps
```

Scripts `02`, `04`, `06`, and `07` are step-by-step test scripts used while building the pipeline. Script `08` combines their logic into the final flow.

---

## 📂 Project Structure

```text
CourseAssist-AI/
│
├── videos/                 # Input lecture videos
├── audios/                 # Extracted audio (.mp3)
├── json/                   # Timestamped transcript chunks per lecture
├── embeddings.csv          # Chunks with their embedding vectors
├── prompt.txt              # Latest generated LLM prompt
│
├── 01_Video_to_Audio.py
├── 02_Speech_to_Text.py
├── 03_Create_Chunks.py
├── 04_Creating_Embeddings.py
├── 05_Bulk_Embedding.py
├── 06_Pulling_top_matching_chunk.py
├── 07_Introspecting_top_results_and_Creating_prompt.py
├── 08_Getting_response_from_LLM.py
├── EmbeddingModule.py
└── README.md
```

---

## 🔭 Roadmap

- Build a web interface: a course-platform style UI with a "My Courses" section and an embedded video player
- Add an AI agent that answers questions about video content and recommends which course to take for a given topic
- Support multiple courses (Python, Flask, SQL, Data Science, and more) in one knowledge base, and return the course name with each result
- Merge short Whisper segments into larger, overlapping chunks for better retrieval context
- Store embeddings in a vector database (FAISS or ChromaDB) instead of a CSV file
- Move the repeated retrieval code into shared functions instead of duplicating it in scripts 06 to 08
- Strip the reasoning (`<think>`) block from `deepseek-r1` responses so only the final answer is shown
- Link each result directly to the video at the returned timestamp

---

## 👨‍💻 About

Built as my final-year project to explore how Retrieval-Augmented Generation can make video learning searchable, using only local, open-source models.
