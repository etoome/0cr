"""
Game related functions
"""

from flask import Blueprint, jsonify, request
from .db import get_db, get_user_from_key, get_game, generate_string, generate_int, get_date
from cnn import cnn, cnn_chinese
from .chinese import ChineseInt

from random import random, choice
from base64 import b64decode
import cv2


bp = Blueprint('game', __name__, url_prefix='/game')

@bp.route('/new', methods=['POST'])
def new_game():
    """
    Initiaties a new game by creating a token that will be associated to the user secret and returns it.
    Will also return the first char  to guess
    """

    db = get_db()
    key = request.get_json().get('key')

    if key is None:
        return {'error': "Key is required"}, 401

    if (game := get_game(key=key)) is not None:
        return {
            'token': game['token'],
            'char': game['char'],
            # TODO: Add field in case there's already a score
        }

    token = generate_string(10)
    char = str(generate_int(9))

    db.execute(
        "INSERT INTO game (key, token, char) VALUES (?, ?, ?)", (key, token, char)
    )
    db.commit()

    return {
        'token': token,
        'char': char,
    }

@bp.route('/play', methods=['POST'])
def game_play():

    db = get_db()
    json = request.get_json()
    token = json.get('token')
    image = json.get('image')

    if token is None:
        return {'error': "Token is required"}, 401

    if image is None:
        return {'error': 'image is requires'}, 401

    game = db.execute(
        "SELECT * FROM game WHERE token=?", (token,)
    ).fetchone()

    if game is None:
        return {'error': 'Unkown token'}, 404

    write_image(image[22:], f"instance/{token}.png")
    preprocess_image(f"instance/{token}.png")

    solution = game['char']

    try:
        solution = str(ChineseInt[solution].value)
        guess = cnn_chinese.guess_image(f"instance/{token}.png")
    except KeyError: # arabic character
        guess = cnn.guess_image(f"instance/{token}.png")

    if str(guess) == solution:
        correct = True
    else:
        correct = False

    if not correct:
        db.execute(
            "DELETE FROM game WHERE token=?", (token,)
        )
        if game['score'] >= biggest_score(game['key']):
            db.execute(
                "UPDATE user SET score=?, day=? WHERE key=?", (game['score'], get_date(), game['key'])
            )
            
        db.commit()

        return {
            'success': False,
            'score': game['score'],
        }

    next_char = generate_next_char(game['score']+1)
    db.execute(
        "UPDATE game SET score=score+1, char=? WHERE token=?", (next_char, token)
    )
    db.commit()

    return {
        'success': True,
        'score': game['score']+1,
        'char': next_char,
    }

def write_image(base64_image, filepath):
    """
    Converts an image in base 64 to a file that will be located at the given path
    Code found at: https://stackoverflow.com/a/34116876
    """

    imgdata = b64decode(base64_image)
    with open(filepath, 'wb') as f:
        f.write(imgdata)

def preprocess_image(imagepath):
    """
    Adds a white background
    https://stackoverflow.com/a/53737420
    Then invert colors to have the black background and white writing
    """
    #load image with alpha channel.  use IMREAD_UNCHANGED to ensure loading of alpha channel
    image = cv2.imread(imagepath, cv2.IMREAD_UNCHANGED)

    #make mask of where the transparent bits are
    trans_mask = image[:,:,3] == 0

    #replace areas of transparency with white and not transparent
    image[trans_mask] = [255, 255, 255, 255]

    #new image without alpha channel...
    blank_bg = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
    invert_im = cv2.bitwise_not(blank_bg)

    cv2.imwrite(imagepath, invert_im)

def generate_next_char(score):
    """
    Based on the user `score` will return a chinese int or an arabiac int as the next thing to play
    """
    percentage = score * 10
    r = random() * 100

    if percentage > r:
        res = choice(list(ChineseInt)).name
    else:
        res = generate_int(9)

    return res

def biggest_score(user_key):
  """
  Gets a user key and returns his biggest score
  Returns 0 if no entries
  """
  db = get_db()
  user = db.execute(
      "SELECT score FROM user WHERE key=?", (user_key,)
  ).fetchone()

  if user is None:
      return 0

  return user['score']
