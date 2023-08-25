from flask import Flask
from threading import Thread
import json

def check_repeat(token):
  f = open("token.json")
  tokens = json.load(f)
  for i in range(len(tokens['id'])):
    if token == tokens['id'][i]:
      print("Repeat token found")
      return True
    
  return False

def write_to_token(token):

  if check_repeat(token):
    return False
    
  try:
    f = open("token.json")
    tokens = json.load(f)
    tokens['id'].append(token)
    
    json_object = json.dumps(tokens, indent=4)
    
    with open("token.json", "w") as f:
      f.write(json_object)
      
    return True
  except:
    return False

app = Flask('')


@app.route('/')
def home():
  return "Hello. I am alive!"


@app.route('/addToken/<token>')
def addToken(token):

  if token == None:
    return "Invalid token"

  if write_to_token(token):
    return "Successfully add token"
  else:
    return "Error when adding tokens"


def run():
  app.run(host='0.0.0.0', port=8000)


def keep_alive():
  t = Thread(target=run)
  t.start()
