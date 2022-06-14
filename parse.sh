for FILE in ./data/html/*
do
    python3 ./src/parser/file_to_txt.py "${FILE}"
done