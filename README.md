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

<div>
    <a href="https://www.loom.com/share/fbe32a7b4ad540589008d28515db4a6a" target='_blank'>
      <p>Check out this short clip of the app:</p>
    </a>
    <a href="https://www.loom.com/share/fbe32a7b4ad540589008d28515db4a6a" target='_blank'>
      <img style="max-width:300px;" src="https://cdn.loom.com/sessions/thumbnails/fbe32a7b4ad540589008d28515db4a6a-with-play.gif">
    </a>
  </div>

## Lessons Learned

What did you learn while building this project?

- Building backend with Python using FastApi 🐍
- Table manipulation using pandas: Series and DataFrame types! 🐼
- Jinja Templates 🥷🏼
- Practice with Python's built-in modules:
  - os
  - asyncio
  - logging
  - shutil

What challenges did you face and how did you overcome them?

- Understanding what pandas' Series and DataFrame types are is fairly straightforward. Manipulating them using built-in methods took some reading and a bunch of printing/debugging, this was solved by constantly referring to the pandas docs.
- Another challenge I encountered was the need to keep track of the errors that my app throws while in production. I had to re-learn how to efficiently use loggers again. This time, just logging the essential details needed to reproduce the error in development in order to fix the bug.

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

## Icebox

- Add reactivity in the front-end (search/sort/filter).
- create a database for the items/documents
- refactor backend and follow MVC architecture

## Feedback

If you have any feedback, please reach out to me at bor.joezari@gmail.com

## Used By

This project is used by the following companies:

- Lucky Stores
