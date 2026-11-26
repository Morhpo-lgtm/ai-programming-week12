'''[역할]  너는 파이썬 데이터 처리를 돕는 조교다.

[목표]  아래 명세대로 CSV를 정제하는 함수 정제(df)를 만들어라.

[데이터]
  파일: scores_2026.csv, 114행 5열 (학번 이름 반 과목 점수)
  점수는 0 이상 100 이하의 정수여야 한다.
  반과 과목 값의 앞뒤에 공백이 섞여 있다.

[처리 규칙]  ← 명세서 ③④⑤ 칸 + 데이터 특성을 옮깁니다
  1) 점수가 비어 있는 행은 삭제한다.
  2) 모든 열이 완전히 같은 행은 하나만 남긴다.
  3) 반과 과목의 앞뒤 공백을 제거한다.
  4) 점수가 0~100 밖인 행은 삭제한다.

[제약]  pandas만 사용. 각 단계 뒤 남은 행 수를 print 할 것.
'''

import pandas as pd


def 정제(df):
    """명세에 따라 성적 데이터를 정제한 복사본을 반환한다."""
    cleaned = df.copy()

    # 점수가 비어 있는 행을 삭제한다.
    cleaned = cleaned.dropna(subset=["점수"])
    print(len(cleaned))

    # 모든 열이 같은 중복 행을 하나만 남긴다.
    cleaned = cleaned.drop_duplicates()
    print(len(cleaned))

    # 반과 과목의 앞뒤 공백을 제거한다.
    cleaned["반"] = cleaned["반"].str.strip()
    cleaned["과목"] = cleaned["과목"].str.strip()
    print(len(cleaned))

    # 점수가 0부터 100 사이가 아닌 행을 삭제한다.
    cleaned = cleaned[cleaned["점수"].between(0, 100)]
    print(len(cleaned))
    print("*"*30)
    df.groupby("반")["점수"].sum().sum()   # 7484.0
    df["점수"].sum()                        # 7484.0    ← 같아야 합니다
    print(df.groupby("반")["점수"].sum().sum())
    df.groupby("반")["점수"].count().sum()  # 100
    len(df)       
    print(df.groupby("반")["점수"].count().sum())                          
    '''# ① 필터링
    정제된 df에서 과목이 '수학'인 행만 남기는 코드를 한 줄로 써라.
    그리고 남은 행 수를 print 하라.
    '''
    df = df[df["과목"] == "수학"]
    print(len(df))
    print("-"*30)
    '''# ② 그룹화
    정제된 df를 '반'으로 묶어 점수 평균을 내는 코드를 써라.
    그다음 '과목'과 '반' 두 기준으로 묶는 코드도 따로 써라.
    '''
    # '반'으로 묶어 점수 평균
    avg_by_class = cleaned.groupby("반")["점수"].mean()
    # '과목'과 '반'으로 묶어 점수 평균
    avg_by_subject_and_class = cleaned.groupby(["과목", "반"])["점수"].mean()
    print(avg_by_class)
    print(avg_by_subject_and_class)
    print("-"*30)
    '''# ③ 통계
    '반'으로 묶어 개수 · 평균 · 중앙값 · 최댓값을 한 표로 내는
    코드를 써라. 소수 둘째 자리까지 반올림하라.
    '''
    stats_by_class = cleaned.groupby("반")["점수"].agg(["count", "mean", "median", "max"]).round(2)
    print(stats_by_class)
    
    df[(df["반"]=="1반") & (df["과목"]=="수학")]["점수"]
    # len(df[(df["반"]=="1반") & (df["과목"]=="수학")]["점수"])
    print(df[(df["반"]=="1반") & (df["과목"]=="수학")]["점수"])
    return cleaned





# def 정제(df):
#     print("시작       ", len(df))          # 114
#     df = df.dropna(subset=["점수"])
#     print("빈 칸 제거 ", len(df))          # 108
#     df = df.drop_duplicates()
#     print("중복 제거  ", len(df))          # 104
#     df["반"]   = df["반"].str.strip()
#     df["과목"] = df["과목"].str.strip()
#     df = df[(df["점수"] >= 0) & (df["점수"] <= 100)]
#     print("범위 밖 제거", len(df))         # 100
#     return df


if __name__ == "__main__":
    scores = pd.read_csv("scores_2026.csv")
    정제(scores)



# test_analysis.py
import pandas as pd
from analysis import 정제, 반별평균

본  = 정제(pd.read_csv("scores_2026.csv"))
미니 = 정제(pd.read_csv("mini.csv"))
def test_정제하면_100행이_남는다():           # ① 행 수 보존
    assert len(본) == 100

def test_반은_두_종류만_남는다():             # ① 행 수 보존
    assert sorted(본["반"].unique()) == ["1반", "2반"]

def test_그룹합이_전체합과_같다():             # ② 합계 일치
    assert 본.groupby("반")["점수"].sum().sum() == 본["점수"].sum()

def test_손계산과_일치한다():                 # ③ 손계산 대조
    assert 반별평균(미니)["1반"] == 80.0
