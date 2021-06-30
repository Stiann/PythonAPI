# IMPORTANT
To test this API:
- install Python 3.9 or later
- open terminal and move to where 'application.py' is located
- do 
```
pip install -r requirements.txt
```
- then
```
python application.py
```


# DOCUMENTATION

DB is formed by 5 tables: student, grade, course, teacher, students_courses

ACCOUNT SECTION:

- POST /register

requires:
```json
{
    "username": "",
    "password": "",
    "name": "",
    "surname": "",
    "type": "",
    "course"
}
```
note: types available are "student" and "teacher", "course" is necessary only when registering a student

possible errors on:
username: missing, longer than 16 characters
password: missing, shorter than 8 characters
name: missing, longer than 30 characters
surname: missing, longer than 30 characters
type: missing, not student nor teacher
course: missing if type=student, course ID not valid, course does not exist

returns: 
```json
{
    "id": "UUID",
    "name": "",
    "password": "HASHED PASSWORD",
    "surname": "",
    "username": ""
}
```

- POST /login

requires:
```json
{
    "username": "",
    "password": ""
}
```

possible errors on:
username: missing, longer than 16 characters
password: missing, shorter than 8 characters

if teacher: disabled, deleted before
general: login failed

response:
```json
{
    "id": "UUID",
    "name": "",
    "surname": "",
    "token": "JWT TONKEN",
    "type": "type of who logged in",
    "username": ""
}
```

COURSE SECTION:

- GET ALL /courses

response:
```json
{
    "courses": [
        {
            "id": "UUID",
            "name": "",
            "students":[
                {
                    "id": "",
                    "name": "",
                    "surname": "",
                    "username": ""
                }
            ],
            "teacher": {
                "id": "",
                "name": "",
                "surname": "",
                "username": ""
            }
        }
    ]
}
```

- GET ONE /courses/id
```json
{
    "id": "UUID",
    "name": "",
    "students":[
        {
            "id": "",
            "name": "",
            "surname": "",
            "username": ""
        }
    ],
    "teacher": {
        "id": "",
        "name": "",
        "surname": "",
        "username": ""
    }
}
```

possible errors on:
id: not valid (not long 36 char, UUID included "-"s), no course with this id found

- POST /courses

requires:
```json
{
    "name": "",
    "teacher": "id"
}
```

possible errors on:
name: missing, longer than 30 characters
teacher: missing, ID not valid, teacher does not exist

response:
```json
{
    "id": "",
    "name": "",
    "teacher": {
        "id": "",
        "name": "",
        "surname": "",
        "username": ""
    }
}
```

- PUT /courses/id

requires:
```json
{
    "name": "",
    "teacher": ""
}
```

possible errors on:
id: not valid
name: missing, longer than 30 characters
teacher: missing, id not valid, teacher does not exist

- DELETE /courses/id

requires:
```json
{
    "confirm": true
}
```

DELETE disables the course, no student can enter this course on /register

possible errors on:
id: not valid, course not found
confirm: missing or set to false

GRADES

- GET ALL /grades

response:
```json
{
    "grades": [
        {
            "course": {
                "id": "",
                "name": ""
            },
            "grade": "",
            "id": "",
            "id_student": {
                "id": "",
                "name": "",
                "surname": ""
            },
            "id_teacher": {
                "id": "",
                "name": "",
                "surname": ""
            }
        }
    ]
}
```

- GET ONE /grades/id

response:
```json
{
    "course": {
        "id": "",
        "name": ""
    },
    "grade": "",
    "id": "",
    "id_student": {
        "id": "",
        "name": "",
        "surname": "",
        "username": ""
    },
    "id_teacher": {
        "id": "",
        "name": "",
        "surname": "",
        "username": ""
    }
}
```

possible errors on:
id: not valid, grade not found

- POST /grades

requires:
```json
{
    "student": "id",
    "teacher": "id",
    "course": "id",
    "grade": 9
}
```

possible errors on:
student: missing, id not valid, student not found, student disabled
teacher: missing, id not valid, teacher not found
course: missing, id not valid, course not found
grade: missing, less than 0 and bigger than 10

response:
```json
{
    "course": {
        "id": "",
        "name": ""
    },
    "grade": "9",
    "id": "",
    "student": {
        "id": "",
        "name": "",
        "surname": ""
    },
    "teacher": {
        "id": "",
        "name": "",
        "surname": ""
    }
}
```

- PUT /grades/id

requires:
```json
{
    "student": "",
    "teacher": "",
    "course": "",
    "grade": 9
}
```

possible errors on:
student: missing, id not valid, student not found
teacher: missing, id not valid, teacher not found
course: missing, id not valid, course not found
grade: missing, less than 0 and bigger than 10

- DELETE /grades/id

requires:
```json
{
    "confirm": true
}
```

DELETE grade deletes the grade if it is confirmed

possible errors on:
confirm: missing or set to false

STUDENTS

- GET ALL /students

response:
```json
{
    "students": [
        {
            "courses": [
                {
                    "id": "",
                    "name": ""
                }
            ],
            "id": "",
            "name": "",
            "surname": "",
            "username": ""
        }
    ]
}
```

- GET ONE /students/id

response:
```json
{
    "courses": [
        {
            "id": "",
            "name": ""
        }
    ],
    "id": "",
    "name": "",
    "surname": "",
    "username": ""
}
```

possible errors on:
id: not valid, not found

- PUT /students/id

requires:
```json
{
    "username": "",
    "name": "",
    "surname": ""
}
```

possible errors on:
id: not valid, not found
username: missing, longer than 16 characters
name: missing, longer than 30 characters
surname: missing, longer than 30 characters

response:
```json
{
    "id": "",
    "name": "",
    "surname": "",
    "username": ""
}
```

- DELETE /students/id

DELETE student make him unable to receive grades

requires:
```json
{
    "confirm": true
}
```

possible errors on:
confirm: missing or set to false

TEACHERS

- GET ALL /teachers

response:
```json
{
    "teachers": [
        {
            "id": "",
            "name": "",
            "surname": "",
            "username": ""
        }
    ]
}
```

- GET ONE /teachers/id

possible errors on:
id: not valid or not found

response:
```json
{
    "id": "",
    "name": "",
    "surname": "",
    "username": ""
}
```

- PUT /teachers/id

requires:
```json
{
    "username": "",
    "name": "",
    "surname": ""
}
```

possible errors on:
id: not valid, not found
username: missing, longer than 16 characters
name: missing, longer than 30 characters
surname: missing, longer than 30 characters

- DELETE /teachers/id

DELETE teacher disables him from logging in

requires:
```json
{
    "confirm": true
}
```

possible errors on:
confirm: missing or set to false