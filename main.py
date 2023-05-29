import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api_openai import create_completion
from model.task_model import Base, Task

engine = create_engine('sqlite:///tasks.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def generate_chapters():
    print("Enter the subject of the story:")
    subject = input("> ")
    generate_chapters_list(subject)


def generate_chapters_list(subject):
    print("Generating chapters...")
    query = f"Generate list of chapters for a story. Subject of the story is {subject}. " \
            f"Return the list as JSON array. Every item in the list should be chapter's name and short description. " \
            f"Make it interesting and captivating. Try to make it a cautionary tale." \
            f"Item structure is:" \
            '{' + f"\"name\": \"example name\",\"description\": \"example description.\"" + '}' \
                                                                                            "Return JSON and nothing more."

    completion = create_completion(
        [
            {
                "role": "user",
                "content": query
            },
        ]
    )

    parsed_tasks = json.loads(completion)
    tasks_db = [Task(info='"' + x["name"] + '" ' + x["description"], status="todo", answer="") for x in parsed_tasks]

    session.add_all(tasks_db)
    session.commit()
    print("Chapters saved!")
    input("..")


def generate_paragraphs():
    tasks = session.query(Task).where(Task.status == "todo").all()
    if len(tasks) == 0:
        print("No tasks found")
    else:
        for index, row in enumerate(tasks):
            print(f"Running... ({index + 1}/{len(tasks)})")
            story = ""
            finished_paragraphs = session.query(Task).where(Task.status == "done").all()
            for paragraph in finished_paragraphs:
                story += paragraph.answer
            completion = create_completion(
                [
                    {
                        "role": "user",
                        "content": story + "Write a paragraph. Here is title and description of the paragraph: " + row.info
                    },
                ],
            )
            row.status = "done"
            row.answer = completion
            session.commit()
        input("Done!")


def show_saved_chapters():
    tasks = session.query(Task).all()
    if len(tasks) == 0:
        print("No tasks found")
    else:
        for row in tasks:
            print("ID:", row.id, "\nStatus:", row.status, "\nInfo:", row.info, "\nHas paragraph:",
                  "Yes" if (row.answer != "") else "No", "\n")
    input("..")


def clear_saved_chapters():
    tasks = session.query(Task).all()
    for row in tasks:
        session.delete(row)
    session.commit()
    print("Tasks cleared!")
    input("..")


def export_to_txt():
    ready_chapters = session.query(Task).where(Task.status == "done").all()
    unfinished_chapters = session.query(Task).where(Task.status == "todo").all()

    if len(unfinished_chapters) != 0:
        print("There are unfinished chapters!")
        input("..")
        return

    text = ""
    for row in ready_chapters:
        text += row.answer + "\n\n"
    with open("output.txt", "w", encoding='utf-8') as file:
        file.write(text)

    print("Output saved to output.txt")
    input("..")


def print_menu():
    print("\nPlease choose an option:")
    print("1. Generate list of chapters for a story")
    print("2. Generate paragraphs for each chapter")
    print("3. Show saved chapters")
    print("4. Clear saved chapters")
    print("5. Export to txt")
    print("0. Quit")


def handle_user_choice(user_choice):
    if user_choice == "1":
        generate_chapters()
    elif user_choice == "2":
        generate_paragraphs()
    elif user_choice == "3":
        show_saved_chapters()
    elif user_choice == "4":
        clear_saved_chapters()
    elif user_choice == "5":
        export_to_txt()
    else:
        print("Invalid choice!")


def main():
    while True:
        print_menu()
        user_choice = input("> ")
        if user_choice == "0":
            print("Goodbye!")
            session.close()
            break
        else:
            handle_user_choice(user_choice)


if __name__ == "__main__":
    main()
