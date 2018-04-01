Used command-line
-----------------
    ::

        $ mkdir relevefactures2csv
        $ cd relevefactures2csv
        $ python3 -m venv myvenv
        $ cd myvenv
        $ . bin/activate
        $ pip install --upgrade pip
        $ cd ..
        $ git init
        $ cd myvenv
        $ git config --global user.name "Yevgueny KASSINE"
        $ git config --global user.email ykassine@geekadomicile.com
        $ mkdir csv
        $ vim ../.gitignore
        # amend with :
        #    *.pyc
        #    *~
        #    __pycache__
        #    db.sqlite3
        #    .DS_Store
        #    csv/
        #    myvenv
        $ git add --all
        $ git status
        $ git remote add origin https://github.com/geekadomicile/relevefactures2csv.git
        $ git commit -am "Init"
        $ git push -u origin master

