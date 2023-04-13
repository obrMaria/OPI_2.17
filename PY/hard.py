#!/usr/bin/env python3
# _*_ coding: utf-8 _*_


import json
import click
import os


@click.group()
@click.argument("filename")
@click.pass_context
def main(ctx, filename):
    ctx.obj = {
        'filename': filename
    }


@main.command('add')
@click.pass_context
@click.option("-n", "--name")
@click.option("-g", "--group")
@click.option("-m", "--marks")
def get_student(ctx, name, group, marks):
    """
    Добавить данные о студенте.
    """
    filename = ctx.obj['filename']
    students = load_students(filename)
    students.append(
        {
            'name': name,
            'group': group,
            'marks': [int(i) for i in marks.split()]
        }
    )

    with open(filename, "w", encoding="utf-8") as fout:
        json.dump(students, fout, ensure_ascii=False, indent=4)
    click.secho("Студент добавлен")


@main.command("display")
@click.pass_obj
@click.option("--display", "-d", is_flag=True)
def display_students(filename, find):
    """
    Вывести данные о студентах.
    """
    students = load_students(filename)
    if find:
        students = find(students)

    # Заголовок таблицы.
    line = '+-{}-+-{}-+-{}-+-{}-+'.format(
        '-' * 4,
        '-' * 30,
        '-' * 20,
        '-' * 15
    )
    print(line)
    print(
        '| {:^4} | {:^30} | {:^20} | {:^15} |'.format(
            "№",
            "Ф.И.О.",
            "Группа",
            "Оценки"
        )
    )
    print(line)
    # Вывести данные о всех студентах.
    for idx, student in enumerate(students, 1):
        print(
            '| {:>4} | {:<30} | {:<20} | {:>15} |'.format(
                idx,
                student.get('name', ''),
                student.get('group', ''),
                ','.join(map(str, student['marks']))
            )
        )
    print(line)


@main.command("find")
@click.pass_obj
@click.option("--find", "-f", is_flag=True)
def find_students(students):
    """
    Выбрать студентов со ср ариф успеваемости >4.
    """
    result = []
    count = 0
    for student in students:
        marks = student.get('marks', '')
        if sum(marks) / (len(marks)) >= 4.0:
            result.append(student)
            count += 1

    return result


def load_students(filename):
    """
    Загрузить всех студентов из файла JSON.
    """
    result = []
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as fin:
            result = json.load(fin)
    return result


if __name__ == "__main__":
    main()
