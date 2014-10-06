#!/usr/bin/python

import unittest
import subprocess
from time import sleep
import urllib2
import json
import os

def send_test_data(json_data):
    req = urllib2.Request("http://localhost:8080/generateSentence",
                          data=json_data,
                          headers={"Content-Type":"application/json"})
    return urllib2.urlopen(req).read()

class TestCake(unittest.TestCase):
    def test(self):
        self.assertEqual(send_test_data(open("fixtures/cake.json","r").read()), "John baked a cake from some ingredients.")
        
class TestIngredients(unittest.TestCase):
    def test(self):
        self.assertEqual(send_test_data(open("fixtures/ingredients.json","r").read()), "The ingredients were flour, sugar, butter and eggs.")

class TestTense(unittest.TestCase):
    def test(self):
        sentence = {}
        sentence["subject"] = "John"
        sentence["verb"] = "kick"
        sentence["object"] = "Dave"

        sentence["features"] = [{"tense":"past"}]
        self.assertEqual(send_test_data(json.dumps({"sentence":sentence})), "John kicked Dave.")

        sentence["features"] = [{"tense":"present"}]
        self.assertEqual(send_test_data(json.dumps({"sentence":sentence})), "John kicks Dave.")
        
        sentence["features"] = [{"tense":"future"}]
        self.assertEqual(send_test_data(json.dumps({"sentence":sentence})), "John will kick Dave.")

if __name__=="__main__":
    print "Starting up nlgserv..."
    nlgserv = subprocess.Popen(["./nlgserv.py"],
                               stdin=subprocess.PIPE,
                               stdout=open(os.path.devnull, "w"),
                               stderr=open(os.path.devnull, "w"),
                               preexec_fn=os.setsid)
    sleep(10)
    print "Commencing testing..."
    unittest.main(exit=False)
    print "Shutting down nlgserv..."
    os.killpg(nlgserv.pid, subprocess.signal.SIGTERM)
    nlgserv.wait()
