Set your credentials in the file credentials.txt
# Run the code in terminal:
```sh
source run.sh
```
and your app should be up and working.

\*if you are on MacOS\Linux and run into an issue with importing Kaleido, 
with the cloned parent folder as current directory:
```sh
cd ./GStorevenv/lib/python3.11/site-packages/kaleido/executable
vi kaleido
```
and replace the file contents with

> DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
> cd "$DIR"
> ./bin/kaleido "$@"

(Quotes around _$DIR_ and _$@_ to work with folders with spaces in their names)

\*if you get ssl error approve the ssl certificates locally