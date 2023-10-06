from io import BytesIO

USER = {
    'email': 'test@example.com',
    'first_name': 'first_name',
    'last_name': 'last_name',
    'hashed_password': '$2b$12$Sy/AU..XdUWwlzuCWTNWAOdF2s8k2FvrB6G/Cw69lNNUxpyfoP6sa',
}
USER2 = {
    'email': 'user2@example.com',
    'first_name': 'first_name2',
    'last_name': 'last_name2',
}
FILES = [('image_file', ''), ('image_file', '')]
BIN_FILE = BytesIO('test'.encode('utf-8'))
PASSAGE = {
    'beauty_title': 'string',
    'title': 'string',
    'other_titles': 'string',
    'connect': 'string',
}
COORDS = {'latitude': 0, 'longitude': 0, 'height': 0}
