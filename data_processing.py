import pandas as pd
import numpy as np
from datetime import datetime
import re



def unixtime_to_dt64(ut):
    if type(ut) == pd.Timestamp:
        return ut.to_numpy()
    else:
        ut = int(ut)
        dt = datetime.utcfromtimestamp(ut)
        return np.datetime64(dt)


def change_avatar(avatar_link, win=True):
    if win:
        head, sep, tail = avatar_link.partition('Transparent')
        new_sep = "Circle"
        avatar_link = head + new_sep + tail
        avatar_link = re.sub('&eyeType=(.*)&eyebrowType', "&eyeType=Happy&eyebrowType", avatar_link)
        avatar_link = re.sub('&mouthType=(.*)&skinColor', "&mouthType=Smile&skinColor", avatar_link)
        avatar_link = re.sub('&eyebrowType=(.*)&facialHairColor', "&eyebrowType=RaisedExcitedNatural&facialHairColor", avatar_link)
        return avatar_link
    else:
        # avatar_link = re.sub('&topType=(.*)&accessoriesType', "&topType=ShortHairDreads02&accessoriesType", avatar_link)
        avatar_link = re.sub('&eyeType=(.*)&eyebrowType', "&eyeType=Cry&eyebrowType", avatar_link)
        avatar_link = re.sub('&eyebrowType=(.*)&facialHairColor', "&eyebrowType=SadConcernedNatural&facialHairColor", avatar_link)
        avatar_link = re.sub('accessoriesType=(.*)&hairColor', "accessoriesType=Blank&avatarStyle", avatar_link)
        avatar_link = re.sub('&mouthType=(.*)&skinColor', "&mouthType=Sad&skinColor", avatar_link)
        return avatar_link


if __name__ == "__main__":
    link_list = [
        "https://getavataaars.com/?accessoriesType=Round&avatarStyle=Transparent&clotheType=GraphicShirt&eyeType=Dizzy&eyebrowType=AngryNatural&facialHairColor=Platinum&facialHairType=BeardLight&hatColor=Red&mouthType=Concerned&skinColor=Tanned&topType=ShortHairFrizzle",
        "https://getavataaars.com/?accessoriesType=Round&avatarStyle=Transparent&clotheColor=Blue01&clotheType=Hoodie&eyeType=Happy&eyebrowType=AngryNatural&facialHairColor=Auburn&facialHairType=BeardLight&graphicType=Bat&hairColor=Platinum&hatColor=Gray02&mouthType=Twinkle&skinColor=Pale&topType=ShortHairDreads02",
        "https://getavataaars.com/?accessoriesType=Blank&avatarStyle=Transparent&clotheColor=PastelGreen&clotheType=ShirtCrewNeck&eyeType=Cry&eyebrowType=RaisedExcited&facialHairColor=Black&facialHairType=MoustacheFancy&graphicType=Bat&hairColor=Red&hatColor=Pink&mouthType=Sad&skinColor=Black&topType=ShortHairDreads02"]
    for i in link_list:
        print(change_avatar(i, win=False))