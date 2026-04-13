try:
    import scrython, argparse, re, os
    from requests import get
except ModuleNotFoundError as err:
    err = str(err)
    print("ModuleNotFoundError: " + err)
    print("You can try running 'pip install "+ err.split()[-1][1:] + " to install the package")
    quit()

# Regex patterns
InitialNumReg = re.compile(r"[0-9]*\s?")
SetInfoReg = re.compile(r"[(]\w*[)]\s\d*")
SanitizeReg = re.compile(r'[<>:"/\\|?*]')

# Set up defaults for variables
ImageDir = "CardImages"
LogFile = "ScryfallDownload.log"
Version="1.0"
VDate = "4/13/2026"

# Object for handling cmd arguments
parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, \
    description='Utility for reading a file containing MTG deck information and pulling the respective card images from Scryfall.\nThe import file should contain a card list in the same format as the Moxfield export feature.', \
    epilog="Author\tCarter Moore\nVersion\t"+Version+"\t"+VDate+"\nCredit to Nanda Scott for the Scrython module (https://github.com/NandaScott/Scrython)")

# Set up arguments
parser.add_argument('filename', type=ascii, help='The file containing the card information')
parser.add_argument('-d', '--dir', type=ascii, help='Optional: The directory the images will be saved to')
parser.add_argument('-l', '--logfile', type=ascii, help='Optional: Name of the logfile')

# Handle arguments
args = parser.parse_args()
if not args.dir is None:
    ImageDir = args.dir.replace("'", "")
if not args.logfile is None:
    LogFile = args.logfile.replace("'", "")
ImportFile = args.filename.replace("'", "")

def matchToString(match):
    if match is None:
        return None
    return match.group()

def createCardPath(RelDir, CardName):
    return os.path.join(os.getcwd(),RelDir, SanitizeReg.sub("",CardName) + ".png")

def dlSingleSidedCard(card):
    try:
        url = card.image_uris['png']
        response = get(url)
        with open(createCardPath(ImageDir, CardName)), "wb") as img:
            img.write(response.content)
        l.write("\tSuccessfully imported!\n")
    except: # Log failure
        if card.image_uris['png'] is None:
            l.write("\tFailed to import face %r.\n" % (face.name))
            l.write("\t\tUnable to find image url!\n")
        else:
            l.write("\tFailed to import card. Image URL:\n")
            l.write("\t"+url+"\n")
        return -1
    return 0

# Begin
if not os.path.exists(ImageDir):
    os.mkdir(ImageDir)
print("Fetching card images...")

with open(ImportFile, "r", encoding="utf-8") as f:
    with open(LogFile, "w", encoding="utf-8") as l:
        while True:
            CardInfo = f.readline()
            if len(CardInfo) == 0:
                break # EOF, we're done
            # Break down card info into its respective parts using regex
            NumCards = matchToString(InitialNumReg.match(CardInfo)).strip()
            CardInfo = InitialNumReg.sub("", CardInfo, 1)
            SetInfo = SetInfoReg.search(CardInfo)
            Set = matchToString(SetInfo).split()[0]
            CollectorNum = matchToString(SetInfo).split()[1]
            CardName = SetInfoReg.sub("", CardInfo).strip() # We've stripped out all additional info, leaving only the card name
            l.write("Card Name: %r, Set: %r, Collector Number: %r, Number of Cards: %r\n" % (CardName, Set, CollectorNum, NumCards))
            # Let's get started
            card = scrython.cards.ByCodeNumber(code=Set.strip("()"), number=CollectorNum)
            if card.card_faces: # More than one face for card, handle
                for face in card.card_faces:
                    try:
                        url = face.image_uris['png']
                        response = get(url)
                        with open(createCardPath(ImageDir, face.name), "wb") as img:
                            img.write(response.content)
                        l.write("\tSuccessfully imported face %r!\n" % (face.name))
                    except: # Handle failure
                        if face.image_uris is None:
                            if card.image_uris['png'] is None:
                                l.write("\tFailed to import face %r.\n" % (face.name))
                                l.write("\t\tUnable to find image url!\n")
                            else: # Not actually a double-sided card
                                dlSingleSidedCard(card)
                            break
                        else:
                            l.write("\tFailed to import face %r.\n" % (face.name))
                            l.write("\t\tImage URL: "+url+"\n")
                        continue
            else:
                dlSingleSidedCard(card)

print("Finished!")
