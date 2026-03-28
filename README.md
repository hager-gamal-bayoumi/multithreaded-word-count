# Multithreaded Word Count

## Project Overview
This project is a python application that counts the number of words in a large text file using multithreading.

The program divides the file into smaller parts and assigns each part to a separate thread. Each thread processes its portion of the text and counts the words. Finally, the results from all threads are combined to produce the total word count.

## Objectives
- Demonstrate the concept of multithreading .
- Process large text files efficiently.
- Compare single-threaded and multithreaded performance.

## How It Works
1. The program reads a large text file.
2. The file is divided into multiple parts.
3. Each part is processed by a separate thread.
4. Each thread counts the words in its part.
5. The results are combined to get the total word count.

## Technologies Used
- python 
- Multithreading
- File Handling

## Project Structure

Multithreaded-Word-Count
│
├── src
│   ├── Main.py
│   ├── WordCountThread.py
│
├── data
│   └── textfile.txt
│
└── README.md

## Future Improvements
- Add support for very large files
- Display the most frequent words
- Add a graphical interface

## Author
Project developed to demonstrate multithreading and parallel processing.
