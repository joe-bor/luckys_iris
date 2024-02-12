# IRIS Order Helper v1

This project simplifies the process for Department Managers at Lucky Stores Supermarket to view and edit their IRIS-recommended orders by generating barcodes for each item in their current list. Instead of hand-typing in the order codes of each item in the hand-held gun, we simply just have to scan it.

## Table of Contents

- [Demo](#demo)
- [Lessons Learned](#lessons-learned)
- [How to Run on Your Local Machine](#how-to-run-on-your-local-machine)
- [FAQ](#faq)
- [Feedback](#feedback)
- [Used By](#used-by)

## Demo

Insert gif or link to demo

<!-- ![Demo GIF](URL_OF_THE_GIF) -->

## Lessons Learned

What did you learn while building this project?

- Building backend with Python using FastApi 🐍
- Table manipulation using pandas! 🐼
- Jinja Templates 🥷🏼
- Practice with Python's built-in modules:
  - os
  - asyncio
  - logging
  - shutil

What challenges did you face and how did you overcome them?

- It took a lot of printing and debugging to get used to pandas' Series and DataFrame types. However, it was very well worth it, as I now see how powerful it is and its potential.

## How to Run on Your Local Machine

To run this project on your local machine, follow these steps:

1. Install [Python](https://www.python.org/downloads/) and [Java](https://www.oracle.com/java/technologies/javase-jdk11-downloads.html) on your machine.

2. Clone the repository:

```bash
git clone https://github.com/joe-bor/luckys_iris.git
```

3. Navigate to the project directory:

```bash
cd luckys_iris
```

4. Create a `.env` file in the root directory of the project and add the following environment variables, adjust to your needs:

```bash
PORT=8000 # where to serve run your app
DELAY=30  # seconds before clean up function runs
```

5. Install the required dependencies:

```bash
pip install -r requirements.txt
```

6. Run the application:

```bash
uvicorn main:app --reload
```

This command will start a local server, typically accessible at `http://127.0.0.1:8000`.

7. To interact with the application, use the provided URLs in your web browser or through a tool like Postman.

## FAQ

#### Were you paid for this?

No, I wanted to add a piece to my portfolio that is actually being used by people.

#### How did you come up with this?

I saw an opportunity to make my life and my coworkers' easier by solving a problem we all faced.

## Feedback

If you have any feedback, please reach out to me at bor.joezari@gmail.com

## Used By

This project is used by the following companies:

- Lucky Stores
