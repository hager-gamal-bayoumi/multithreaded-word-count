# Multithreaded Word Count

## Project Overview
This project is a Java application that counts the number of words in a large text file using multithreading.

The program divides the file into smaller parts and assigns each part to a separate thread. Each thread processes its portion of the text and counts the words. Finally, the results from all threads are combined to produce the total word count.

## Objectives
- Demonstrate the concept of multithreading in Java.
- Process large text files efficiently.
- Compare single-threaded and multithreaded performance.

## How It Works
1. The program reads a large text file.
2. The file is divided into multiple parts.
3. Each part is processed by a separate thread.
4. Each thread counts the words in its part.
5. The results are combined to get the total word count.

## Technologies Used
- Java
- Multithreading
- File Handling

## Project Structure

Multithreaded-Word-Count
│
├── src
│   ├── Main.java
│   ├── WordCountThread.java
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
Project developed to demonstrate multithreading and parallel processing in Java.

## Parallelism Strategy
The application uses data parallelism by splitting the input file into independent chunks.  
Each thread processes a different chunk simultaneously, which improves performance compared to sequential execution.

---

## Thread Safety
To prevent race conditions:
- Each thread maintains its own local word count (local HashMap)
- Results are combined after all threads finish execution
- This reduces contention between threads and ensures correct results

---

## Performance Benefit
Using multithreading significantly improves performance when working with large files:
- Sequential execution processes one part at a time
- Parallel execution processes multiple parts simultaneously
- This leads to faster execution time and better CPU utilization

---

## Key Concepts
- Multithreading
- Parallelism
- Data Partitioning
- Thread Safety
- Race Condition
