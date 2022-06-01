import urllib.request
import json
from bs4 import BeautifulSoup
from binaryninja import PluginCommand
from binaryninjaui import *
def main(bv):

    ctx = UIContext.activeContext()
    h = ctx.contentActionHandler()
    a = h.actionContext()
    token_state = a.token
    #for name, type in bv.types.items():
    try:
        name = str(token_state.token).lower()
        try:
            function_name=str(token_state.token).lower()
            found_target = urllib.request.urlopen("https://docs.microsoft.com/api/search?search="+function_name+"%20function&locale=en-us&scoringprofile=semantic-captions&facet=category&facet=products&$filter=category%20eq%20%27Documentation%27&$top=1&expandScope=true")
            data = json.load(found_target)
            found_info = str(urllib.request.urlopen(data["results"][0]["url"]).read())
            soup = BeautifulSoup(found_info,features="html.parser")
            my_code=soup.find_all("code", class_="lang-cpp")
            for code in my_code:
                cleanResult = code.text
                while "  " in cleanResult:
                    cleanResult = cleanResult.replace("  "," ")
                cleanResult = cleanResult.replace("\\t","")
                while "\\r\\r" in cleanResult:
                    cleanResult = cleanResult.replace("\\r\\r","\\r")
                while "\\n\\n" in cleanResult:
                    cleanResult = cleanResult.replace("\\n\\n","\\n")
                cleanResult = cleanResult.replace("\\n","")
                print(cleanResult)
                a.function.set_comment_at(a.address,cleanResult)
                break; # only get the first result (I assume the top result is the best returned from the MSDN search algo) can remove if you want to see all results
        except:
            print("error")
    except:
        print("couldn't find info on "+str(name))
    


PluginCommand.register('MSDN_Helper', 'MSDN helper', main)

