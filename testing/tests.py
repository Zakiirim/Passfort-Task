"""Collection of testcases for the app.

Generally the tests are performed on a testing DB, however because of the time constraints
given with the take-home task I'm performing the test on the same DB since most of endpoints
accepts only GET requests.
"""

import unittest
from datetime import datetime

from factory import make_revision, make_string

from app import app
from src.connection import session
from src.documents.models import RevisionModel, TitleModel


class BaseTestCase(unittest.TestCase):
    """Base class that other Test classes should inherit from."""
    tester = app.test_client()

    def tearDown(self) -> None:
        """Overrides tearDown() to clean session after each test."""
        super().tearDown()
        session.rollback()

    @staticmethod
    def clean_objects(uuid) -> None:
        """An util function to delete object created from post requests.

        :param uuid: The uuid of the object to delete.
        """
        to_delete = session.query(RevisionModel).filter_by(revision=uuid)
        id_ = to_delete.first().title_id
        to_delete.delete()
        session.query(TitleModel).filter_by(id=id_).delete()
        session.commit()


class DocumentsAPIResponseTestCases(BaseTestCase):
    """Collection of methods to test API endpoints json response."""

    def test_get_list_all_revisions(self) -> None:
        """Test if GET /documents endpoint returns all the revisions available."""
        previous = len(self.tester.get("/documents").json)
        expected = [make_revision() for _ in range(5)]
        response = self.tester.get("/documents").json
        self.assertEqual(len(expected), len(response)-previous)

    def test_get_list_revisions_by_title(self) -> None:
        """Test if GET /documents/{title} endpoint returns all the revisions for that title."""
        title = make_string(length=20)
        expected = [make_revision(title=title) for _ in range(5)]
        for _ in range(5):
            make_revision()

        response = self.tester.get(f"/documents/{title}").json
        self.assertEqual(len(expected), len(response))

    def test_get_revision_by_timestamp(self) -> None:
        """Test if GET /documents/{title}/{timestamp} returns the latest revision for a given timestamp."""
        title = make_string(length=20)
        date_time = datetime.max
        expected = [make_revision(title=title) for _ in range(5)]
        for _ in range(5):
            make_revision()

        expected.sort(key=lambda revision: revision.timestamp)
        response = self.tester.get(f"/documents/{title}/{date_time}").json
        self.assertEqual(str(expected[-1].revision), response["revision"])

    def test_get_latest_revision(self) -> None:
        """Test if GET /documents/latest returns the latest revision."""
        title = make_string(length=20)
        expected = [make_revision(title=title) for _ in range(5)]
        for _ in range(5):
            make_revision()

        expected.sort(key=lambda revision: revision.timestamp)
        response = self.tester.get(f"/documents/{title}/latest").json
        self.assertEqual(str(expected[-1].revision), response["revision"])

    def test_post_create_new_revision(self) -> None:
        """Test if POST /documents/{title}/latest creates the new revision."""
        title = make_string(length=20)
        new_revision = self.tester.post(f"/documents/{title}", json={
            "content": make_string(length=5)
        }).json
        response = self.tester.get(f"/documents/{title}/latest").json
        self.clean_objects(response["revision"])
        self.assertEqual(new_revision["revision"], response["revision"])


class DocumentsResponseCodeTestCases(BaseTestCase):

    def test_return_200_all_revisions(self) -> None:
        """Test if GET /documents endpoint returns response code 200."""
        response = self.tester.get("/documents")
        self.assertEqual(response.status_code, 200)

    def test_return_200_all_revisions_by_title(self) -> None:
        """Test if GET /documents/{title} endpoint returns response code 200."""
        title = make_string(length=20)
        response = self.tester.get(f"/documents/{title}")
        self.assertEqual(response.status_code, 200)

    def test_return_200_all_revisions_by_timestamp(self) -> None:
        """Test if GET /documents/{title}{timestamp} endpoint returns response code 200."""
        title = make_string(length=20)
        timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        response = self.tester.get(f"/documents/{title}/{timestamp}")
        self.assertEqual(response.status_code, 200)

    def test_return_200_latest_revision(self) -> None:
        """Test if GET /documents/{title}/latest endpoint returns response code 200."""
        title = make_string(length=20)
        response = self.tester.get(f"/documents/{title}/latest")
        self.assertEqual(response.status_code, 200)

    def test_return_201_create_new_revision(self) -> None:
        """Test if POST /documents/{title} endpoint returns response code 201."""
        title = make_string(length=20)
        response = self.tester.post(f"/documents/{title}", json={"content": title})
        self.assertEqual(response.status_code, 201)
