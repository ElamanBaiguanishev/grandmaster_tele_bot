from typing import List, Optional
from pydantic import BaseModel


class StudyMode(BaseModel):
    id: int
    name: str
    courses: Optional[List['Course']] = None  # Обратите внимание на строковую аннотацию


class Course(BaseModel):
    id: int
    name: str
    studyMode: Optional[StudyMode] = None
    semesters: Optional[List['Semester']] = None


class Semester(BaseModel):
    id: int
    name: str
    course: Optional[Course] = None
    groups: Optional[List['Group']] = None  # Предположим, что Group будет также определён


class Group(BaseModel):
    id: int
    name: str
    semester: Optional[Semester] = None
    lessons: Optional[List['Lesson']] = None


class Lesson(BaseModel):
    id: int
    name: str
    group: Optional[Group] = None
