from io import BytesIO

USER = {
    "email": "test@example.com",
    "first_name": "first_name",
    "last_name": "last_name",
}
USER2 = {
    "email": "user2@example.com",
    "first_name": "first_name2",
    "last_name": "last_name2",
}
FILES = [("image_file", ""), ("image_file", "")]
BIN_FILE = BytesIO("test".encode("utf-8"))
PASSAGE = {
    "beauty_title": "string",
    "title": "string",
    "other_titles": "string",
    "connect": "string",
}
PASSAGE_WITH_USER = PASSAGE | {"user_id": 1}
COORDS = {"latitude": 0, "longitude": 0, "height": 0}
