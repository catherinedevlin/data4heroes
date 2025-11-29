import pandas as pd 

URL = 'http://localhost:8000/ohio-supers.html'

frames = pd.read_html(URL)
for (n, df) in enumerate(frames):
    label = f" Frame {n} "
    print(f"{label:=^60}")
    print(df.head(3))
