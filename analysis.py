import pandas as pd
df = pd.read_csv("scores_2026.csv")
# df = pd.read_csv("scores_2026_cp949.csv", encoding="cp949")



df.shape                     # (114, 5)
df["점수"].isna().sum()       # 6      ← 빈 칸이 몇 개인가
df.duplicated().sum()        # 4      ← 완전히 같은 행이 몇 개인가
df["반"].unique()             # ['2반' '1반' '1반 ']      ← 세 개?
df["과목"].unique()           # ['수학' '프로그래밍' '영어' '프로그래밍 ']
df["점수"].describe()         # max 999.0  min -5.0      ← 점수인데?

print(df.shape)
print(df["점수"].isna().sum())
print(df.duplicated().sum())
print(df["반"].unique())
print(df["과목"].unique())
print(df["점수"].describe())

#-------------------------------------------------
import pandas as pd

def 정제(df):
    cleaned = df.dropna(subset=["점수"]).drop_duplicates().copy()
    cleaned["반"] = cleaned["반"].str.strip()
    cleaned["과목"] = cleaned["과목"].str.strip()
    cleaned = cleaned[cleaned["점수"].between(0, 100)]
    return cleaned

def 반별평균(df):
    return df.groupby("반")["점수"].mean()