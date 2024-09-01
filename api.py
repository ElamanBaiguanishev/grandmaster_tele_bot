import requests
from typing import List

from models import StudyMode, Course, Semester, Group, Lesson


class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_study_modes(self) -> List[StudyMode]:
        response = requests.get(f"{self.base_url}/studymodes")
        response.raise_for_status()
        return [StudyMode(**item) for item in response.json()]

    def get_study_mode_by_id(self, study_mode_id: int) -> StudyMode:
        response = requests.get(f"{self.base_url}/studymodes/{study_mode_id}")
        response.raise_for_status()
        return StudyMode(**response.json())

    def get_course_by_id(self, course_id: int) -> Course:
        response = requests.get(f"{self.base_url}/courses/{course_id}")
        response.raise_for_status()
        return Course(**response.json())

    def get_semester_by_id(self, semester_id: int) -> Semester:
        response = requests.get(f"{self.base_url}/semesters/{semester_id}")
        response.raise_for_status()
        return Semester(**response.json())

    def get_group_by_id(self, group_id: int) -> Group:
        response = requests.get(f"{self.base_url}/groups/{group_id}")
        response.raise_for_status()
        return Group(**response.json())

    def get_lesson_by_id(self, lesson_id: int) -> Lesson:
        response = requests.get(f"{self.base_url}/lessons/{lesson_id}")
        response.raise_for_status()
        return Lesson(**response.json())
