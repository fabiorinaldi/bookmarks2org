# bookmarks2org
Converts firefox bookmarks to org-mode format, modified from:
http://rexim.me/firefox-bookmarks-to-org-mode.html 

## USAGE:

   1. cat BOOKMARKS.json | bookmarks-to-org.py > BOOKMARKS.org

      Converts the entire json file into an org mode file
   
   2. cat BOOKMARKS.json arg1 ... argN | bookmarks-to-org.py > BOOKMARKS.org

      Checks if any of the provided arguments matches the name of a
      folder in the json file. Folders that match will be
      converted (with all items they contain). Args that do not
      match any folder name will be ignored.

## Updates 2018, Fabio Rinaldi

- changed the structure of the recursive loop to make it more easily
  modifiable
- added a default folder title, which will be used if none is
  provided in the json file
- the script now accepts command-line arguments. If none are provided,
  it converts the entire json file. If there are arguments, they will
  be treated as folder titles to be matched in the json file. Only
  folders which have an exact match will be converted, all the rest
  discarded. 
